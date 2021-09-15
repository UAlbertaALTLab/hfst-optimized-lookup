# hfst-optimized-lookup changelog

## Unreleased

## v0.0.13 2021-09-15

  - Add a public no-op function so that cython will generate a header file
    for embedding

  - Rename some internal C macro `#ifdef` names to reduce collisions.
    `DEBUG` is now `OL_DEBUG`, and `BUILD_MAIN` is now `BUILD_HFSTOL_MAIN``

## v0.0.12 2021-08-17

  - Move `__version__` to a separate `VERSION` file to work around an
    import cycle issue sometimes seen with pip/pipenv

  - Now that the same repo also contains node bindings, start tagging
    python releases as `python-vX.Y.Z` instead of plain `vX.Y.Z`

## v0.0.11 2021-05-13

  - Important bug fix: when encountering an input symbol which was not in
    the FST, e.g., `v` in Cree, `lookup()` would return analyses for the
    input up to that point, e.g., `avocado` → `a` → `['å+Ipc+Interj']`. An
    empty list is now returned instead for invalid inputs.

  - Check in release script

## v0.0.10 2021-02-04

  - Added: `TransducerFile.lookup_lemma_with_affixes()` which returns
    a list of `Analyses(prefixes=(...,), lemma="", suffixes=(...,))`.
    This is to facilitate development with the Plains Cree FST and other
    FSTs built by ALTLab.

## v0.0.9 2021-02-03

  - Fixed: missing typings for `TransducerFile.lookup_symbols()`

## v0.0.8 2021-02-02

  - new `lookup_symbols()` method returns symbols as list elements; no more
    need for client heuristics to guess whether or not a substring came
    from Multichar_Symbols
  - GitHub actions now used for tests
  - Added `__version__` constant

## v0.0.7 2021-01-14

  - Add `bulk_lookup` method

## v0.0.6 2021-01-14

  - Add typings for package

## v0.0.5 2021-01-12

  - Accept pathlib objects by calling os.fspath

## v0.0.4 2021-01-12

  - Work around libstdc++/libc++ build confusion

## v0.0.3 2021-01-12

  - Initial release of python wrapper, based on upstream [hfst-v3.15.4]

[hfst-v3.15.4]: https://github.com/hfst/hfst/tree/v3.15.4
