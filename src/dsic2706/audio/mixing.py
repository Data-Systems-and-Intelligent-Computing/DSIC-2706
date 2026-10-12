"""Compatibility wrappers for the audited ITERA noise mixer.

Older package callers used ``return_noise_path``. The canonical mixer uses
``return_noise_info`` and can additionally return a complete audit record.
"""

from src.mix_noise import (
    compute_signal_power,
    get_available_itera_noise_files,
    get_e3_reserved_noise_files,
    get_noise_segment,
    mix_audio_at_snr as _mix_audio_at_snr,
)


def calculate_rms(y):
    return compute_signal_power(y) ** 0.5


def get_available_noise_files(exclude_e3_unknowns: bool = True):
    return get_available_itera_noise_files(exclude_e3_unknowns=exclude_e3_unknowns)


def load_itera_noise_segment(duration_samples, seed: int = 42, return_path: bool = False,
                             exclude_e3_unknowns: bool = True):
    return get_noise_segment(
        samples=duration_samples,
        seed=seed,
        return_path=return_path,
        exclude_e3_unknowns=exclude_e3_unknowns,
    )


def mix_audio_at_snr(signal, snr_db, noise=None, seed: int = 42,
                     return_noise_path: bool = False, exclude_e3_unknowns: bool = True):
    if noise is not None:
        raise ValueError("Compatibility mixer no longer accepts an untracked noise array; use src.mix_noise explicitly.")
    return _mix_audio_at_snr(
        signal,
        snr_db=snr_db,
        seed=seed,
        return_noise_info=return_noise_path,
        exclude_e3_unknowns=exclude_e3_unknowns,
    )
