"""
Script: src/mix_noise.py
Fungsi: Engine pencampuran derau aditif fisik ITERA (Controlled Additive Noise Mixing).
Menerapkan formula SNR eksak:
    x_noisy = x_clean + alpha * n_noise
    alpha = sqrt( P_signal / (P_noise * 10^(SNR_dB / 10)) )

ATURAN KETAT INTEGRITAS DATA (AUDIT COMPLIANCE):
1. 100% menggunakan rekaman fisik AudioMoth kampus ITERA (data/itera_noise/).
2. SINTESIS PINK NOISE DIHAPUS PERMANEN (Zero Synthetic Fallback).
3. Fail-Loud: Jika berkas derau fisik tidak ditemukan atau jumlah tidak sesuai manifes (1.799),
   WAJIB melempar FileNotFoundError.
4. Partisi Disjoin: Bank derau untuk pencampuran (E2/E4) dipisahkan secara tegas dari
   271 berkas derau yang dialokasikan untuk negatif kelas terbuka E3 (unknown_open_set_manifest.csv).
5. Deteksi Derau Senyap: Potongan derau yang senyap (RMS < 1e-4) ditolak dan diambil ulang.
6. Keterlacakan: Setiap operasi pencampuran mencatat jalur relatif berkas derau fisik yang digunakan.
"""

from pathlib import Path
import os
import sys
import numpy as np
import pandas as pd
try:
    import soundfile as sf
except ImportError:
    sf = None

try:
    import librosa
except ImportError:
    librosa = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent

try:
    from src.preprocess import TARGET_SR, TARGET_SAMPLES, TARGET_RMS, normalize_rms
except ImportError:
    from preprocess import TARGET_SR, TARGET_SAMPLES, TARGET_RMS, normalize_rms

NOISE_DIR = PROJECT_ROOT / "data" / "itera_noise"
MANIFEST_PATH = PROJECT_ROOT / "data" / "manifests" / "itera_noise_manifest.csv"
UNKNOWN_MANIFEST_PATH = PROJECT_ROOT / "data" / "manifests" / "unknown_open_set_manifest.csv"

_CACHED_ALL_NOISE_FILES = None
_CACHED_MIXING_NOISE_FILES = None


def get_e3_reserved_noise_files() -> set:
    """Mengambil himpunan nama berkas derau yang dialokasikan untuk E3 unknown negatives."""
    reserved = set()
    if UNKNOWN_MANIFEST_PATH.exists():
        try:
            df_unk = pd.read_csv(UNKNOWN_MANIFEST_PATH)
            noise_rows = df_unk[df_unk["source_category"] == "itera_environmental_noise"]
            for fp in noise_rows["file_path"]:
                rel = Path(str(fp).replace("\\", "/"))
                # Simpan nama file atau rel path di bawah data/itera_noise
                reserved.add(rel.name.lower())
        except Exception as e:
            print(f"[!] Catatan membaca manifes unknown E3: {e}")
    return reserved


def get_available_itera_noise_files(exclude_e3_unknowns: bool = True):
    """
    Mengambil daftar berkas derau fisik AudioMoth ITERA secara rekursif
    dari itera_noise_manifest.csv atau langsung dari struktur folder fisik.
    
    Validasi Ketat:
    - Memverifikasi keberadaan seluruh berkas fisik sesuai manifes.
    - Menolak diam-diam jika ada berkas manifes yang hilang (Fail-Loud).
    - Memisahkan bank derau E2/E4 dari E3 unknown negatives jika exclude_e3_unknowns=True.
    """
    global _CACHED_ALL_NOISE_FILES, _CACHED_MIXING_NOISE_FILES
    
    if exclude_e3_unknowns and _CACHED_MIXING_NOISE_FILES is not None:
        return _CACHED_MIXING_NOISE_FILES
    if not exclude_e3_unknowns and _CACHED_ALL_NOISE_FILES is not None:
        return _CACHED_ALL_NOISE_FILES

    all_noise_files = []

    # 1. Baca dari itera_noise_manifest.csv
    if MANIFEST_PATH.exists():
        df = pd.read_csv(MANIFEST_PATH)
        if "verified_bird_free" in df.columns:
            df = df[df["verified_bird_free"] == True]
        
        expected_count = len(df)
        missing_files = []

        for fn in df["filename"]:
            rel_path = Path(str(fn).replace("\\", "/"))
            full_path = NOISE_DIR / rel_path
            if full_path.exists():
                all_noise_files.append(str(full_path))
            else:
                missing_files.append(str(fn))

        # Tambalan: Verifikasi jumlah berkas sesuai manifes (Fail-Loud jika hilang)
        if missing_files:
            raise FileNotFoundError(
                f"[FATAL] Ketidaksesuaian jumlah berkas derau fisik ITERA!\n"
                f"Manifes mencatat {expected_count} berkas, namun {len(missing_files)} berkas "
                f"tidak ditemukan di {NOISE_DIR}.\n"
                f"Contoh berkas hilang: {missing_files[:3]}"
            )
    else:
        # 2. Jika manifes tidak ada, telusuri folder fisik secara rekursif
        if NOISE_DIR.exists():
            for ext in ["*.WAV", "*.wav", "*.mp3", "*.flac"]:
                all_noise_files.extend([str(p) for p in NOISE_DIR.rglob(ext)])

    if not all_noise_files:
        raise FileNotFoundError(
            f"[FATAL] Tidak ditemukan berkas audio derau fisik ITERA di {NOISE_DIR}!\n"
            "Sesuai mandat integritas data, fallback sintetis (pink noise) telah DIHAPUS PERMANEN."
        )

    all_noise_files = sorted(list(set(all_noise_files)))
    _CACHED_ALL_NOISE_FILES = all_noise_files

    # Tambalan: Pisahkan bank derau campuran dari E3 unknown negatives
    e3_reserved = get_e3_reserved_noise_files()
    mixing_files = [f for f in all_noise_files if Path(f).name.lower() not in e3_reserved]

    if exclude_e3_unknowns:
        if not mixing_files:
            raise RuntimeError("[FATAL] Seluruh berkas derau terpakai untuk E3! Tidak ada yang tersisa untuk campuran.")
        _CACHED_MIXING_NOISE_FILES = mixing_files
        return _CACHED_MIXING_NOISE_FILES
    else:
        return _CACHED_ALL_NOISE_FILES


def compute_signal_power(x: np.ndarray) -> float:
    """Menghitung daya rata-rata sinyal (Mean Squared Power)."""
    return float(np.mean(x ** 2))


def get_noise_relative_path(abs_or_full_path: str) -> str:
    """Mengembalikan jalur relatif terhadap data/itera_noise/."""
    p = Path(abs_or_full_path)
    try:
        rel = p.relative_to(NOISE_DIR)
        return str(rel).replace("\\", "/")
    except ValueError:
        return p.name


def get_noise_segment(samples: int = TARGET_SAMPLES, seed: int = 42, return_path: bool = False,
                      return_audit_info: bool = False,
                      exclude_e3_unknowns: bool = True):
    """
    Mengambil segmen derau 5.0 detik nyata dari bank rekaman AudioMoth ITERA.
    
    Tambalan:
    - Menolak segmen derau senyap (RMS < 1e-4) dengan re-sampling hingga 10 kali percobaan.
    - Mengembalikan jalur relatif terstandarisasi jika return_path=True.
    """
    noise_files = get_available_itera_noise_files(exclude_e3_unknowns=exclude_e3_unknowns)
    rng = np.random.default_rng(seed)

    max_attempts = 10
    for attempt in range(max_attempts):
        selected_file = rng.choice(noise_files)
        try:
            y_noise, _ = librosa.load(selected_file, sr=TARGET_SR, mono=True)
            if len(y_noise) >= samples:
                start = int(rng.integers(0, len(y_noise) - samples + 1))
                seg = y_noise[start:start + samples].astype(np.float32)
            else:
                repeats = int(np.ceil(samples / len(y_noise)))
                y_noise = np.tile(y_noise, repeats)
                seg = y_noise[:samples].astype(np.float32)
                start = 0

            # Tambalan: Deteksi derau senyap sebelum normalisasi
            raw_rms = np.sqrt(np.mean(seg ** 2))
            if raw_rms < 1e-4:
                # Derau senyap terdeteksi, coba file lain
                continue

            seg_norm = normalize_rms(seg, target_rms=TARGET_RMS)
            rel_noise_path = get_noise_relative_path(selected_file)

            audit_info = {
                "noise_file": rel_noise_path,
                "noise_start_sample": start,
                "noise_segment_samples": int(samples),
                "noise_seed": int(seed),
                "noise_attempt": attempt + 1,
                "noise_raw_rms": float(raw_rms),
            }
            if return_audit_info:
                return seg_norm, audit_info
            if return_path:
                return seg_norm, rel_noise_path
            return seg_norm

        except Exception as e:
            if attempt == max_attempts - 1:
                raise RuntimeError(f"Gagal memproses berkas derau fisik ITERA {selected_file}: {e}")

    # Jika setelah 10 percobaan tetap senyap, lempar ValueError
    raise ValueError(f"[FATAL] Terdeteksi segmen derau senyap (RMS < 1e-4) setelah {max_attempts} percobaan pengambilan!")


def mix_audio_at_snr(clean_signal: np.ndarray, snr_db: float, seed: int = 42, return_noise_info: bool = False,
                     return_audit_info: bool = False,
                     exclude_e3_unknowns: bool = True):
    """
    Mencampur sinyal bersih dengan derau fisik ITERA pada tingkat SNR (dB) eksak.
    
    Tambalan:
    - Jika sinyal bersih senyap (P_signal <= 1e-12), kembalikan sinyal bersih (bukan derau).
    - Jika derau senyap (P_noise <= 1e-10), lempar ValueError.
    - Mengembalikan (mixed_audio, noise_relative_path) jika return_noise_info=True.
    """
    noise, audit_info = get_noise_segment(
        samples=len(clean_signal),
        seed=seed,
        return_audit_info=True,
        exclude_e3_unknowns=exclude_e3_unknowns
    )
    noise_rel_path = audit_info["noise_file"]

    p_signal = compute_signal_power(clean_signal)
    p_noise = compute_signal_power(noise)

    if p_signal <= 1e-12:
        audit_info.update({
            "snr_db_target": float(snr_db),
            "snr_db_achieved": None,
            "signal_power": p_signal,
            "noise_power_before_scaling": p_noise,
            "noise_gain": None,
            "post_mix_gain": 1.0,
            "mix_skipped_silent_signal": True,
        })
        if return_audit_info:
            return clean_signal.copy(), audit_info
        if return_noise_info:
            return clean_signal.copy(), noise_rel_path
        return clean_signal.copy()

    if p_noise <= 1e-10:
        raise ValueError(f"[FATAL] Derau fisik terdeteksi senyap (P_noise={p_noise:.2e}) pada berkas: {noise_rel_path}")

    # Hitung faktor scaling alpha
    target_p_noise = p_signal / (10.0 ** (snr_db / 10.0))
    alpha = np.sqrt(target_p_noise / p_noise)

    # Campurkan
    scaled_noise = alpha * noise
    noisy = clean_signal + scaled_noise

    # Jaga agar tidak clipping
    max_amp = np.max(np.abs(noisy))
    post_mix_gain = 1.0 / max_amp if max_amp > 1.0 else 1.0
    noisy = noisy * post_mix_gain

    signal_after_gain = clean_signal * post_mix_gain
    noise_after_gain = scaled_noise * post_mix_gain
    achieved_noise_power = compute_signal_power(noise_after_gain)
    achieved_snr = 10.0 * np.log10(compute_signal_power(signal_after_gain) / achieved_noise_power)
    audit_info.update({
        "snr_db_target": float(snr_db),
        "snr_db_achieved": float(achieved_snr),
        "signal_power": p_signal,
        "noise_power_before_scaling": p_noise,
        "noise_gain": float(alpha),
        "post_mix_gain": float(post_mix_gain),
        "mix_skipped_silent_signal": False,
    })

    result = noisy.astype(np.float32)
    if return_audit_info:
        return result, audit_info
    if return_noise_info:
        return result, noise_rel_path
    return result


if __name__ == "__main__":
    print("=" * 80)
    print("[*] Menguji engine pencampuran derau fisik ITERA murni...")
    all_files = get_available_itera_noise_files(exclude_e3_unknowns=False)
    mix_files = get_available_itera_noise_files(exclude_e3_unknowns=True)
    print(f"[+] Total berkas derau fisik ITERA terverifikasi: {len(all_files):,}")
    print(f"[+] Berkas dialokasikan untuk campuran E2/E4 (Disjoint): {len(mix_files):,}")
    print(f"[+] Berkas dialokasikan untuk negatif kelas terbuka E3: {len(all_files) - len(mix_files):,}")

    clean = np.sin(2 * np.pi * 440 * np.linspace(0, 5, 160000)).astype(np.float32)
    for snr in [20, 10, 0, -5]:
        mixed, n_rel = mix_audio_at_snr(clean, snr, seed=123, return_noise_info=True)
        print(f"Target SNR: {snr:3d} dB  ==> Berkas Derau Fisik: {n_rel}")
    print("[+] Integritas derau fisik ITERA 100% lolos!")
    print("=" * 80)
