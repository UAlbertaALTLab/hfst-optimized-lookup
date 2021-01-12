A pip-installable library version of [hfst-optimized-lookup][], originally
built for [itwêwina][].

    $ pip install hfst-optimized-lookup

    >>> import hfst_optimized_lookup
    >>> fst = hfst_optimized_lookup.TransducerFile('crk-descriptive-analyzer.hfstol')
    >>> fst.lookup('atim')
    ['atimêw+V+TA+Imp+Imm+2Sg+3SgO+Err/Frag', 'atim+N+A+Sg', 'atimêw+V+TA+Imp+Imm+2Sg+3SgO']


[itwêwina]: https://itwewina.dev
[hfst-optimized-lookup]: https://github.com/hfst/hfst/blob/master/tools/src/hfst-optimized-lookup.cc

## Acknowledgements

  - The authors of the [Helsinki Finite-State Technology][hfst] library and
    application suite

[hfst]: https://github.com/hfst/hfst

### Releasing

  - Increment version in `setup.py`
  - `python3 setup.py sdist`
  - `python3 -m twine upload dist/hfst-optimized-lookup-$VERSION.tar.gz`
