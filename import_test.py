from pathlib import Path

import pytest

import hfst_optimized_lookup
from hfst_optimized_lookup import TransducerFile

TEST_FST = "crk-relaxed-analyzer-for-dictionary.hfstol"


# scope="session" reuses the FST for all tests that use this fixture
@pytest.fixture(scope="session")
def fst():
    return TransducerFile(TEST_FST)


def test_has_version():
    assert type(hfst_optimized_lookup.__version__) == str


def test_symbol_count():
    # If this returned a non-number, we’d get a TypeError here.
    assert TransducerFile(TEST_FST).symbol_count() > 0


def test_subsequent_lookups(fst: TransducerFile):
    assert fst.lookup("itwêwina") == ["itwêwin+N+I+Pl"]
    assert fst.lookup("nikî-nipân") == ["PV/ki+nipâw+V+AI+Ind+1Sg"]


def test_multiple_analyses(fst: TransducerFile):
    assert fst.lookup("môswa") == ["môswa+N+A+Sg", "môswa+N+A+Obv"]


EXPECTED_BULK_LOOKUP_RESULT_1 = {
    "itwêwina": set(["itwêwin+N+I+Pl"]),
    "nikî-nipân": set(["PV/ki+nipâw+V+AI+Ind+1Sg"]),
    "môswa": set(["môswa+N+A+Sg", "môswa+N+A+Obv"]),
}


def test_bulk_lookup(fst: TransducerFile):
    assert (
        fst.bulk_lookup(EXPECTED_BULK_LOOKUP_RESULT_1.keys())
        == EXPECTED_BULK_LOOKUP_RESULT_1
    )


def test_bulk_lookup_with_iterator(fst: TransducerFile):
    assert (
        fst.bulk_lookup(w for w in EXPECTED_BULK_LOOKUP_RESULT_1.keys())
        == EXPECTED_BULK_LOOKUP_RESULT_1
    )


def test_create_from_path_obj():
    fst = TransducerFile(Path(TEST_FST))
    assert fst.lookup("itwêwina") == ["itwêwin+N+I+Pl"]


@pytest.mark.skip("not yet implemented")
def test_limit(fst):
    assert fst.lookup("môswa", limit=1) == ["môswa+N+A+Sg"]


@pytest.mark.skip("not yet implemented")
@pytest.mark.parametrize(
    ("surface", "deep"),
    [
        [
            "môswa",
            [
                ["môswa", "+N", "+A", "+Sg"],
                ["môswa", "+N", "+A", "+Obv"],
            ],
        ],
        ["nikî-nipân", ["PV/ki+", "nipâw", "+V", "+AI", "+Ind", "+1Sg"]],
    ],
)
def test_symbol_lookup1(fst, surface, deep):  #: TransducerFile
    assert fst.lookup_symbols(surface) == deep


def test_raises_exception_on_missing_file():
    with pytest.raises(Exception) as exception_info:
        TransducerFile("/does-not-exist.hfstol")

    exception_messages = " ".join(exception_info.value.args)
    assert "Transducer not found" in exception_messages
    assert "‘/does-not-exist.hfstol’" in exception_messages


def test_raises_exception_on_invalid_file():
    with pytest.raises(Exception) as exception_info:
        # The python test file is not a valid transducer.
        TransducerFile(__file__)

    exception_messages = " ".join(exception_info.value.args)
    assert "wrong or corrupt file?" in exception_messages


if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
