from ._types import Analysis
try:
    from ._hfst_optimized_lookup import TransducerFile
except ModuleNotFoundError:
    from _hfst_optimized_lookup import TransducerFile

__all__ = ["TransducerFile", "Analysis"]

__version__ = "0.0.12.dev0"
