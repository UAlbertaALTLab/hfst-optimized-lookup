# hfst-optimized-lookup

A pip-installable library version of [hfst-optimized-lookup][], originally
built for [itwêwina][].

    $ pip install hfst-optimized-lookup

    >>> import hfst_optimized_lookup
    >>> fst = hfst_optimized_lookup.TransducerFile('crk-relaxed-analyzer-for-dictionary.hfstol')
    >>> fst.lookup('atim')
    ['atim+N+A+Sg', 'atimêw+V+TA+Imp+Imm+2Sg+3SgO']
    >>> fst.lookup_symbols('atim')
    [['a', 't', 'i', 'm', '+N', '+A', '+Sg'], ['a', 't', 'i', 'm', 'ê', 'w', '+V', '+TA', '+Imp', '+Imm', '+2Sg', '+3SgO']]

[itwêwina]: https://itwewina.dev
[hfst-optimized-lookup]: https://github.com/hfst/hfst/blob/master/tools/src/hfst-optimized-lookup.cc

[hfst] is a great toolkit with all sorts of functionality, and is
indispensable for building FSTs, but for Python applications that just want
to do hfst lookups, this package may be easier to use.

The `hfst-optimized-lookup` binary is actually a standalone C++ program
that doesn’t include or link against any other code in hfst, which makes it
much easier to repackage as a small Python library.

Among other benefits, this package can return lists of individual symbols,
including Multichar_Symbols, so that you don’t have to guess or try to
parse out which parts of the analysis are tags.

## Acknowledgements

Thank you to:

  - The authors of the [Helsinki Finite-State Technology][hfst] library and
    application suite

[hfst]: https://github.com/hfst/hfst

## Releasing

(The script that automates the following is still a work in progress.)

Prepare release:

  - Remove `.dev0` suffix from `__version__` in
    `hfst_optimized_lookup/__init__.py`
  - Update `CHANGELOG.md`, changing “Unreleased” to release version and
    adding date

Release:

  - run tests
  - `python3 setup.py sdist`
  - Commit, tag, and push
  - `python3 -m twine upload dist/hfst-optimized-lookup-$VERSION.tar.gz`

Prepare for further development

  - Increment `__version__`, adding `.dev0` suffix
  - Add “Unreleased” header in `CHANGELOG.md`
  - Commit and push
