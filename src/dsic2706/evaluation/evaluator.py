"""Compatibility import for the canonical evaluation pipeline.

The previous package pipeline diverged from ``src.evaluate`` and could use
placeholder deep representations. There is now one implementation path.
"""

from src.evaluate import run_experiment_for_representation

__all__ = ["run_experiment_for_representation"]
