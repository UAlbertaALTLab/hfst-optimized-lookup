from typing import NamedTuple, Tuple


class Analysis(NamedTuple):
    prefixes: Tuple[str, ...]
    lemma: str
    suffixes: Tuple[str, ...]
