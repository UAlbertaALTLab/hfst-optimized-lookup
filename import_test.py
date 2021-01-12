import pytest

from hfst_optimized_lookup import TransducerFile

TEST_FST = "crk-descriptive-analyzer.hfstol"


@pytest.fixture
def fst():
    print("creating fst")
    return TransducerFile(TEST_FST)


def test_symbol_count():
    # If this returned a non-number, we’d get a TypeError here.
    assert TransducerFile(TEST_FST).symbol_count() > 0


def test_subsequent_lookups(fst):
    assert fst.lookup("itwêwina") == ["itwêwin+N+I+Pl"]
    assert fst.lookup("nikî-nipân") == ["PV/ki+nipâw+V+AI+Ind+1Sg"]


def test_multiple_analyses(fst):
    assert fst.lookup("môswa") == ["môswa+N+A+Sg", "môswa+N+A+Obv"]


@pytest.mark.skip("not yet implemented")
def test_limit(fst):
    assert fst.lookup("môswa", limit=1) == ["môswa+N+A+Sg"]


@pytest.mark.skip("not yet implemented")
def test_tag_lookup1(fst):
    assert fst.lookup_tags("môswa") == [
        ["môswa", "+N", "+A", "+Sg"],
        ["môswa", "+N", "+A", "+Obv"],
    ]


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
