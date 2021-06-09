from pathlib import Path

import pytest

import hfst_optimized_lookup
from hfst_optimized_lookup import TransducerFile, Analysis

TEST_FST = "../crk-relaxed-analyzer-for-dictionary.hfstol"


# scope="session" reuses the FST for all tests that use this fixture
@pytest.fixture(scope="session")
def fst() -> TransducerFile:
    return TransducerFile(TEST_FST)


def test_has_version() -> None:
    assert isinstance(hfst_optimized_lookup.__version__, str)


def test_symbol_count() -> None:
    # If this returned a non-number, we’d get a TypeError here.
    assert TransducerFile(TEST_FST).symbol_count() > 0


def test_subsequent_lookups(fst: TransducerFile) -> None:
    assert fst.lookup("itwêwina") == ["itwêwin+N+I+Pl"]
    assert fst.lookup("nikî-nipân") == ["PV/ki+nipâw+V+AI+Ind+1Sg"]


def test_valid_lookup_with_invalid_symbol(fst: TransducerFile) -> None:
    assert fst.lookup("avocado") == []
    assert fst.lookup("navajo") == []


def test_multiple_analyses(fst: TransducerFile) -> None:
    assert fst.lookup("môswa") == ["môswa+N+A+Sg", "môswa+N+A+Obv"]


EXPECTED_BULK_LOOKUP_RESULT_1 = {
    "itwêwina": set(["itwêwin+N+I+Pl"]),
    "nikî-nipân": set(["PV/ki+nipâw+V+AI+Ind+1Sg"]),
    "môswa": set(["môswa+N+A+Sg", "môswa+N+A+Obv"]),
}


def test_bulk_lookup(fst: TransducerFile) -> None:
    assert (
        fst.bulk_lookup(EXPECTED_BULK_LOOKUP_RESULT_1.keys())
        == EXPECTED_BULK_LOOKUP_RESULT_1
    )


def test_bulk_lookup_with_iterator(fst: TransducerFile) -> None:
    assert (
        fst.bulk_lookup(w for w in EXPECTED_BULK_LOOKUP_RESULT_1.keys())
        == EXPECTED_BULK_LOOKUP_RESULT_1
    )


def test_create_from_path_obj() -> None:
    fst = TransducerFile(Path(TEST_FST))
    assert fst.lookup("itwêwina") == ["itwêwin+N+I+Pl"]


@pytest.mark.skip("not yet implemented")
def test_limit(fst: TransducerFile) -> None:
    assert fst.lookup("môswa", limit=1) == ["môswa+N+A+Sg"]  # type: ignore


@pytest.mark.parametrize(
    ("surface", "deep"),
    [
        [
            "môswa",
            [
                ["m", "ô", "s", "w", "a", "+N", "+A", "+Sg"],
                ["m", "ô", "s", "w", "a", "+N", "+A", "+Obv"],
            ],
        ],
        [
            "nikî-nipân",
            [["PV/ki+", "n", "i", "p", "â", "w", "+V", "+AI", "+Ind", "+1Sg"]],
        ],
    ],
)
def test_symbol_lookup1(
    fst: TransducerFile, surface: str, deep: list[list[str]]
) -> None:
    assert fst.lookup_symbols(surface) == deep


@pytest.mark.parametrize(
    ("surface", "example"),
    [
        # VTA with a prefix:
        (
            "ê-mowât",
            Analysis(("PV/e+",), "mowêw", ("+V", "+TA", "+Cnj", "+3Sg", "+4Sg/PlO")),
        ),
        # VAI with prefixes:
        (
            "ê-kî-nitawi-kâh-kîmôci-kotiskâwêyâhk",
            Analysis(
                prefixes=("PV/e+", "PV/ki+", "PV/nitawi+", "RdplS+", "PV/kimoci+"),
                lemma="kotiskâwêw",
                suffixes=("+V", "+AI", "+Cnj", "+12Pl"),
            ),
        ),
        # Ipc:
        (
            # NOTE: assuming relaxed analyzer for dictionary which:
            #  - understands "tansi" is a spelling of "tânisi"
            #  - does NOT output an +Err/Orth tag!
            "tansi",
            Analysis((), "tânisi", ("+Ipc",)),
        ),
        # NA, with possession
        (
            "nitêm",
            Analysis((), "atim", ("+N", "+A", "+Px1Sg", "+Sg")),
        ),
        # NID
        (
            "otâsa",
            Analysis(
                (),
                "mitâs",
                (
                    "+N",
                    "+I",
                    "+D",
                    "+Px3Sg",
                    "+Pl",
                ),
            ),
        ),
        # VAI, no prefixes, unspecified actor:
        (
            "nîminâniwan",
            Analysis((), "nîmiw", ("+V", "+AI", "+Ind", "+X")),
        ),
        # VII, tense prefix
        (
            "kî-kinêpikoskâw",
            Analysis(
                prefixes=("PV/ki+",),
                lemma="kinêpikoskâw",
                suffixes=(
                    "+V",
                    "+II",
                    "+Ind",
                    "+3Sg",
                ),
            ),
        ),
    ],
)
def test_lookup_lemma_with_affixes(
    fst: TransducerFile, surface: str, example: Analysis
) -> None:
    analyses = fst.lookup_lemma_with_affixes(surface)
    assert example in analyses


def test_raises_exception_on_missing_file() -> None:
    with pytest.raises(Exception) as exception_info:
        TransducerFile("/does-not-exist.hfstol")

    exception_messages = " ".join(exception_info.value.args)
    assert "Transducer not found" in exception_messages
    assert "‘/does-not-exist.hfstol’" in exception_messages


def test_raises_exception_on_invalid_file() -> None:
    with pytest.raises(Exception) as exception_info:
        # The python test file is not a valid transducer.
        TransducerFile(__file__)

    exception_messages = " ".join(exception_info.value.args)
    assert "wrong or corrupt file?" in exception_messages


if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
