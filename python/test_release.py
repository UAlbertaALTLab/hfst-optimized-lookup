# type: ignore

from datetime import date
from io import StringIO
from textwrap import dedent

import pytest

from release import Changelog, compute_new_versions


def test_compute_new_versions_basic():
    assert compute_new_versions("0.0.1.dev0") == ("0.0.1", "0.0.2.dev0")


def test_compute_new_versions_complicated():
    assert compute_new_versions("0.2.9.dev0") == ("0.2.9", "0.2.10.dev0")


def test_compute_new_versions_error():
    with pytest.raises(Exception, match="not a dev version"):
        compute_new_versions("0.2.9")


TEST_CHANGELOGS = {
    # The life cycle of a changelog:
    #   1. Released version
    "orig": dedent(
        """\
        # Changelog

        ## v0.0.7 2021-01-05

          - Foo
        """
    ),
    #   2. Script adds header to record unreleased changes
    "empty_unreleased_section": dedent(
        """\
        # Changelog

        ## Unreleased

        ## v0.0.7 2021-01-05

          - Foo
        """
    ),
    #  3. Humans fill in
    "populated_unreleased_section": dedent(
        """\
        # Changelog

        ## Unreleased

          - Baz
          - Bar

        ## v0.0.7 2021-01-05

          - Foo
        """
    ),
    #   4. Script updates ‘unreleased’ header
    "released": dedent(
        """\
        # Changelog

        ## v0.0.8 2021-01-06

          - Baz
          - Bar

        ## v0.0.7 2021-01-05

          - Foo
        """
    ),
    # GOTO step 1
}


def test_changelog_add_unreleased():
    file = StringIO(TEST_CHANGELOGS["orig"])
    c = Changelog(file)
    c.add_unreleased_section()
    assert file.getvalue() == TEST_CHANGELOGS["empty_unreleased_section"]


def test_changelog_add_unreleased_dont_duplicate_existing():
    file = StringIO(TEST_CHANGELOGS["empty_unreleased_section"])
    c = Changelog(file)
    c.add_unreleased_section()
    assert file.getvalue() == TEST_CHANGELOGS["empty_unreleased_section"]


def test_changelog_add_unreleased_error_if_no_headings():
    file = StringIO("hello world\n")
    c = Changelog(file)
    with pytest.raises(ValueError, match="could not find existing release header"):
        c.add_unreleased_section()


def test_changelog_prepare_release():
    file = StringIO(TEST_CHANGELOGS["populated_unreleased_section"])
    c = Changelog(file)
    c.prepare_release("0.0.8", date(2021, 1, 6))
    assert file.getvalue() == TEST_CHANGELOGS["released"]


def test_changelog_prepare_release_err_if_changelog_section_would_be_empty():
    file = StringIO(TEST_CHANGELOGS["empty_unreleased_section"])
    c = Changelog(file)
    with pytest.raises(ValueError, match="contents were empty"):
        c.prepare_release("0.0.8", date(2021, 1, 6))
