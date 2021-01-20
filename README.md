# hfst-optimized-lookup

A pip-installable library version of [hfst-optimized-lookup][], originally
built for [itwêwina][].

    $ pip install hfst-optimized-lookup

    >>> import hfst_optimized_lookup
    >>> fst = hfst_optimized_lookup.TransducerFile('crk-relaxed-analyzer-for-dictionary.hfstol')
    >>> fst.lookup('atim')
    ['atim+N+A+Sg', 'atimêw+V+TA+Imp+Imm+2Sg+3SgO']


[itwêwina]: https://itwewina.dev
[hfst-optimized-lookup]: https://github.com/hfst/hfst/blob/master/tools/src/hfst-optimized-lookup.cc

[hfst] is a great toolkit with all sorts of functionality, and is
indispensable for building FSTs, but for Python applications that just want
to do hfst lookups, this package may be easier to use.

The `hfst-optimized-lookup` binary is actually a standalone C++ program
that doesn’t include or link against any other code in hfst, which makes it
much easier to repackage as a small Python library.

## Acknowledgements

Thank you to:

  - The authors of the [Helsinki Finite-State Technology][hfst] library and
    application suite

[hfst]: https://github.com/hfst/hfst

## Releasing

  - Increment version in `setup.py`
  - `python3 setup.py sdist`
  - `python3 -m twine upload dist/hfst-optimized-lookup-$VERSION.tar.gz`
