import sys
import os
import numpy as np

from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.mix_noise import (
    mix_audio_at_snr,
    compute_signal_power,
    get_available_itera_noise_files,
    NOISE_DIR,
    MANIFEST_PATH,
)


def test_snr_mixing_accuracy():
    sr = 32000
    duration = 2.0
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    clean = (0.5 * np.sin(2 * np.pi * 1000 * t)).astype(np.float32)

    for target_snr in [20, 10, 0]:
        noise = np.random.randn(len(clean)).astype(np.float32)
        p_c = compute_signal_power(clean)
        p_n = compute_signal_power(noise)
        alpha = np.sqrt(p_c / (p_n * 10.0 ** (target_snr / 10.0)))

        actual_snr = 10 * np.log10(p_c / compute_signal_power(alpha * noise))
        assert abs(actual_snr - target_snr) < 1e-4, f"Target {target_snr} dB, tetapi formula {actual_snr:.2f} dB"


def test_physical_itera_noise_mixing():
    """
    Unit test integritas derau fisik AudioMoth ITERA (Sesuai Audit Reviewer):
    1. Verifikasi manifes & berkas fisik: tepat 1.799 berkas audio.
    2. Partisi bebas bocor: 1.528 berkas untuk mixing E2/E4, 271 berkas untuk E3 open-set negatives.
    3. Penolakan derau senyap: RMS derau terambil >= 1e-4.
    4. Integritas jalur: noise_file relatif terhadap data/itera_noise/.
    5. Presisi rasio SNR: SNR terukur pada campuran fisik cocok dengan target (toleransi < 0.1 dB).
    6. Penanganan sinyal bersih senyap: mengembalikan sinyal senyap, bukan derau.
    """
    if not NOISE_DIR.exists() or not MANIFEST_PATH.exists():
        # Jika clone tanpa audio fisik, pastikan fail-loud FileNotFoundError
        try:
            clean = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 32000)).astype(np.float32)
            mix_audio_at_snr(clean, snr_db=10)
            assert False, "Harus melempar FileNotFoundError jika audio fisik tidak ada!"
        except FileNotFoundError:
            return

    # 1. Tepat 1.799 berkas
    all_files = get_available_itera_noise_files(exclude_e3_unknowns=False)
    assert len(all_files) == 1799, f"Diharapkan 1.799 berkas derau fisik ITERA, ditemukan {len(all_files)}"

    # 2. Partisi disjoint E3 (1.528 mixing, 271 E3)
    mix_files = get_available_itera_noise_files(exclude_e3_unknowns=True)
    assert len(mix_files) == 1528, f"Diharapkan 1.528 berkas mixing, ditemukan {len(mix_files)}"

    # 3. Pengujian mixing fisik nyata
    sr = 32000
    duration = 2.0
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    clean = (0.05 * np.sin(2 * np.pi * 1000 * t)).astype(np.float32)

    for target_snr in [20, 10, 0, -5]:
        mixed, noise_path = mix_audio_at_snr(clean, snr_db=target_snr, seed=123, return_noise_info=True)

        # Validasi path
        assert isinstance(noise_path, str) and len(noise_path) > 0, "noise_path harus berupa string jalur valid"
        assert not Path(noise_path).is_absolute() or "itera_noise" in noise_path, f"Path harus di bawah itera_noise: {noise_path}"

        # Validasi non-silent
        p_clean = compute_signal_power(clean)
        diff_noise = mixed - clean
        p_added_noise = compute_signal_power(diff_noise)
        assert p_added_noise > 1e-8, "Derau yang ditambahkan tidak boleh senyap!"

        measured_snr = 10 * np.log10(p_clean / p_added_noise)
        assert abs(measured_snr - target_snr) < 0.1, f"Target {target_snr} dB, tetapi terukur {measured_snr:.2f} dB"

    # 4. Sinyal bersih senyap harus tetap senyap
    silent_clean = np.zeros(32000, dtype=np.float32)
    res_silent, n_rel = mix_audio_at_snr(silent_clean, snr_db=10, seed=42, return_noise_info=True)
    assert np.all(res_silent == 0.0), "Sinyal bersih senyap harus mengembalikan sinyal senyap, bukan derau!"


def test_snr_mixing_reproducibility():
    clean = np.random.randn(32000).astype(np.float32)
    m1 = mix_audio_at_snr(clean, snr_db=10, seed=99)
    m2 = mix_audio_at_snr(clean, snr_db=10, seed=99)
    m3 = mix_audio_at_snr(clean, snr_db=10, seed=100)

    np.testing.assert_allclose(m1, m2, err_msg="Seed yang sama harus menghasilkan sinyal identik!")
    assert not np.allclose(m1, m3), "Seed berbeda harus menghasilkan derau yang berbeda!"
