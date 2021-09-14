from pathlib import Path

from ._types import Analysis

try:
    from ._hfst_optimized_lookup import TransducerFile
except ModuleNotFoundError:
    from _hfst_optimized_lookup import TransducerFile

__all__ = ["TransducerFile", "Analysis"]

__version__ = (Path(__file__).parent / "VERSION").read_text().strip()
