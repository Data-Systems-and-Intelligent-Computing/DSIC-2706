"""Compatibility import for the single, real representation extractor.

The historical package contained a separately initialized toy convolutional
network for R1/R2. It was not the PANNs or BirdNET checkpoint used by the
research protocol. Keep this import path for older callers, but always use
the audited implementation in :mod:`src.embeddings`.
"""

from src.embeddings import AudioRepresentationExtractor

__all__ = ["AudioRepresentationExtractor"]
