"""Gambar ulang ilustrasi teori BAB II menggunakan sinyal sintetis dan vektor."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, Rectangle
from scipy import signal


OUTPUT = Path(__file__).resolve().parents[2] / "paper" / "figures" / "bab2"
INK = "#202733"
BLUE = "#196493"
NAVY = "#48608d"
GOLD = "#ad6824"
RED = "#b33234"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
})


def save(fig, name):
    fig.savefig(OUTPUT / name, dpi=320, facecolor="white", bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)


def drawing(size):
    fig, ax = plt.subplots(figsize=size)
    ax.set_position((0, 0, 1, 1))
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.set_axis_off()
    return fig, ax


def arrow(ax, start, end, *, color=GOLD, style="-|>", width=1.3):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, color=color,
                                mutation_scale=14, linewidth=width,
                                shrinkA=0, shrinkB=0))


def draw_stft():
    """Adaptasi bentuk Gambar 1 Jeon dkk. (2020)."""
    fig, ax = drawing((8, 7.2))
    rng = np.random.default_rng(20261117)
    frame_length, hop = 256, 128
    samples = np.arange(frame_length + 3 * hop)
    x0, x1 = 0.29, 0.93
    x = x0 + (x1 - x0) * samples / samples[-1]
    wave = (0.55 * signal.chirp(samples, 0.035, samples[-1], 0.14)
            + 0.38 * np.sin(2 * np.pi * 0.23 * samples)
            + 0.21 * rng.normal(size=len(samples)))
    window = signal.windows.hann(frame_length)

    ax.text(0.02, 0.91, "Sinyal", va="center", fontsize=17, weight="bold")
    ax.plot(x, 0.91 + 0.044 * wave, color=BLUE, linewidth=0.75)
    ax.text(0.02, 0.735, "Jendela", va="center", fontsize=17, weight="bold")
    ax.hlines(0.689, x0, x1, color=INK, linewidth=1)
    for start in range(0, 4 * hop, hop):
        ax.plot(x[start:start + frame_length], 0.689 + 0.094 * window,
                color=INK, linewidth=1.5)

    arrow(ax, (x0, 0.805), (x[frame_length - 1], 0.805), color=RED, style="<|-|>")
    ax.text((x0 + x[frame_length - 1]) / 2, 0.825, "Panjang jendela $L$",
            ha="center", fontsize=13)
    for start, end, offset, label in [(x0, x[hop], -0.015, "Langkah\n$H$"),
                                      (x[hop], x[frame_length - 1], 0.02, "Tumpang tindih\n$L-H$")]:
        arrow(ax, (start, 0.67), (end, 0.67), color=RED, style="<|-|>")
        ax.text((start + end) / 2 + offset, 0.651, label, ha="center", va="top", fontsize=12)

    ax.text(0.02, 0.475, "Segmentasi dan\npembobotan", va="center", fontsize=17, weight="bold")
    frames = []
    for index, base in enumerate((0.537, 0.449, 0.355)):
        start = index * hop
        frame = wave[start:start + frame_length] * window
        frames.append(frame)
        ax.plot(x[start:start + frame_length], base + 0.034 * frame,
                color=BLUE, linewidth=0.75)

    arrow(ax, (0.55, 0.322), (0.55, 0.239), color=INK, width=1.8)
    ax.text(0.515, 0.277, "FFT", ha="right", va="center", fontsize=17, weight="bold")
    for index, (frame, start) in enumerate(zip(frames, (0.29, 0.515, 0.74)), start=1):
        bins = np.abs(np.fft.rfft(frame))
        bins /= bins.max()
        length = 0.187
        ax.text(start + length / 2, 0.212, f"Keluaran FFT {index}", ha="center", fontsize=13)
        ax.hlines(0.055, start, start + length, color=INK, linewidth=0.7)
        ax.plot(np.linspace(start, start + length, len(bins)), 0.055 + 0.123 * bins,
                color=BLUE, linewidth=0.95)
    save(fig, "stft_adaptasi_jeon_2020.png")


def noise_examples():
    """Hasilkan dua campuran dengan posisi kejadian dan derau dasar yang sama."""
    rate, duration = 32_000, 60
    rng = np.random.default_rng(20261117)
    time = np.arange(rate * duration) / rate
    rumble = (0.65 + 2.3 * np.exp(-((time - 21.3) / 0.25) ** 2)) * np.sin(2 * np.pi * 130 * time)
    background = (0.058 * rumble + 0.012 * rng.normal(size=len(time))).astype(np.float32)
    levels = (0, 35)
    mixtures = [background.copy() for _ in levels]
    for index in range(30):
        start = round(rate * (2 * index + rng.uniform(0.22, 0.8)))
        size = round(rate * rng.uniform(0.13, 0.26))
        stop = start + size
        event_time = np.arange(size) / rate
        begin = rng.uniform(2_500, 5_000)
        end = begin + rng.uniform(-1_100, 1_650)
        call = signal.chirp(event_time, begin, size / rate, end)
        call += 0.32 * signal.chirp(event_time, 2 * begin, size / rate, 2 * end)
        call *= signal.windows.tukey(size, alpha=0.65)
        background_power = np.mean(np.square(background[start:stop], dtype=np.float64))
        call_power = np.mean(call ** 2)
        for mixture, level in zip(mixtures, levels):
            scaled = call * np.sqrt((background_power / call_power) * 10 ** (level / 10))
            measured = 10 * np.log10(np.mean(scaled ** 2) / background_power)
            assert np.isclose(measured, level)
            mixture[start:stop] += scaled
    return time, rate, levels, mixtures


def draw_snr():
    """Adaptasi panel A–D pada Gambar 5 Chen dkk. (2023)."""
    time, rate, levels, mixtures = noise_examples()
    fig, panels = plt.subplots(2, 2, figsize=(9.4, 5.25))
    fig.subplots_adjust(left=0.095, right=0.967, top=0.94, bottom=0.15, wspace=0.33, hspace=0.69)
    intensity = LinearSegmentedColormap.from_list(
        "spektrum", ["#22427b", "#1971ab", "#1b9f9b", "#83cc75", "#f4de53"],
    )
    for column, (level, mixture) in enumerate(zip(levels, mixtures)):
        wave_ax, spec_ax = panels[:, column]
        block = 240
        waves = mixture.reshape(-1, block)
        centers = time[block // 2::block]
        wave_ax.fill_between(centers, waves.min(axis=1), waves.max(axis=1),
                             color=BLUE, linewidth=0.22, alpha=0.88)
        limit = np.max(np.abs(mixture)) * 1.1
        wave_ax.set(ylim=(-limit, limit), ylabel="Amplitudo", xlabel="Waktu (detik)", title=f"SNR = {level} dB")
        wave_ax.axhline(0, color=INK, linewidth=0.5, alpha=0.4, zorder=0)

        freq, centers, spectrum = signal.stft(mixture, fs=rate, window="hann", nperseg=1024,
                                              noverlap=704, boundary=None, padded=False)
        kept = freq <= 12_000
        freq = freq[kept] / 1_000
        power = np.abs(spectrum[kept]) ** 2
        strongest_bin = np.unravel_index(power.argmax(), power.shape)
        relative_db = 10 * np.log10(np.maximum(power / power.max(), 1e-7))
        spec_ax.imshow(relative_db, origin="lower", aspect="auto", interpolation="nearest",
                       extent=(0, 60, freq[0], freq[-1]), cmap=intensity, vmin=-68, vmax=0)
        f_index, t_index = strongest_bin
        spec_ax.scatter(centers[t_index], freq[f_index], s=34, color="#e23432",
                        edgecolor="white", linewidth=0.85, clip_on=False, zorder=3)
        spec_ax.set(ylabel="Frekuensi (kHz)", xlabel="Waktu (detik)", yticks=[0, 4, 8, 12])

        for ax, letter in [(wave_ax, "AB"[column]), (spec_ax, "CD"[column])]:
            ax.set(xlim=(0, 60), xticks=[0, 20, 40, 60])
            ax.text(-0.18, 1.10, letter, transform=ax.transAxes, va="bottom", fontsize=13, weight="bold")
            ax.tick_params(labelsize=10)
            for spine in ax.spines.values():
                spine.set_color("#89919b")
                spine.set_linewidth(0.65)
    fig.text(0.53, 0.035, "Sinyal sintetis · Titik merah menandai daya spektral tertinggi pada setiap panel.",
             ha="center", fontsize=10)
    save(fig, "gelombang_spektrogram_snr_adaptasi_chen_2023.png")


def draw_mfcc():
    """Adaptasi susunan kotak dan cabang pada Gambar 5 Peng dkk. (2025)."""
    fig, ax = drawing((9.8, 4.4))

    def box(bounds, label, color=NAVY):
        x, y, width, height = bounds
        ax.add_patch(Rectangle((x, y), width, height, facecolor="white", edgecolor=color, linewidth=1.35))
        ax.text(x + width / 2, y + height / 2, label, ha="center", va="center", fontsize=13)

    ax.add_patch(Rectangle((0.196, 0.055), 0.255, 0.897, fill=False, edgecolor=NAVY,
                           linestyle=(0, (5, 3)), linewidth=1.55))
    box((0.025, 0.802, 0.137, 0.107), "Masukan WAV")
    for y, label in zip((0.802, 0.572, 0.342, 0.112),
                        ("Pengurangan derau", "Pre-emphasis", "Pembagian frame", "Fungsi jendela")):
        box((0.224, y, 0.198, 0.107), label, INK)
    for y, label, color in zip((0.802, 0.572, 0.342, 0.112),
                               ("STFT", "Bank filter mel", "Transformasi logaritmik", "DCT"),
                               (NAVY, "#685892", "#9b5874", "#99603c")):
        box((0.526, y, 0.273, 0.107), label, color)
    box((0.872, 0.342, 0.106, 0.107), "FBank")
    box((0.872, 0.112, 0.106, 0.107), "MFCC")

    arrow(ax, (0.162, 0.8555), (0.224, 0.8555))
    for x in (0.323, 0.6625):
        for top, bottom in zip((0.802, 0.572, 0.342), (0.679, 0.449, 0.219)):
            arrow(ax, (x, top), (x, bottom))
    ax.plot([0.422, 0.483, 0.483], [0.1655, 0.1655, 0.8555], color=GOLD, linewidth=1.3)
    arrow(ax, (0.483, 0.8555), (0.526, 0.8555))
    for y in (0.3955, 0.1655):
        arrow(ax, (0.799, y), (0.872, y))
    save(fig, "ekstraksi_mfcc_fbank_adaptasi_peng_2025.png")


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    draw_stft()
    draw_snr()
    draw_mfcc()
