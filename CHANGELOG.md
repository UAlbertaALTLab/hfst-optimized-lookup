# hfst-optimized-lookup changelog

## Unreleased

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
