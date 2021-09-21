hfst-optimized-lookup
=====================

[![PyPI version](https://img.shields.io/pypi/v/hfst-optimized-lookup)](https://pypi.org/project/hfst-optimized-lookup/)
[![Documentation](https://github.com/UAlbertaALTLab/hfst-optimized-lookup/actions/workflows/test.yml/badge.svg)](https://github.com/UAlbertaALTLab/hfst-optimized-lookup/actions)
[![Documentation](https://github.com/UAlbertaALTLab/hfst-optimized-lookup/actions/workflows/build-docs.yml/badge.svg)](https://ualbertaaltlab.github.io/hfst-optimized-lookup/)

A pip-installable library version of [hfst-optimized-lookup][], originally
built for [itwêwina][].

Install
-------

    pip install hfst-optimized-lookup

This requires that the machine running `pip` have a working C++ compiler. If
enough people ask for us to upload [binary ‘wheels’] so that you don’t need a
compiler at install time, we could start doing so.

[binary ‘wheels’]: https://packaging.python.org/guides/distributing-packages-using-setuptools/#wheels
### Usage

> [Full API Documentation](https://ualbertaaltlab.github.io/hfst-optimized-lookup/api.html)

Import the library:

    >>> import hfst_optimized_lookup

Then load an FST!

    >>> fst = hfst_optimized_lookup.TransducerFile('../crk-relaxed-analyzer-for-dictionary.hfstol')

> Hint: Download `crk-relaxed-analyzer-for-dictionary.hfstol` by cloning
> https://github.com/UAlbertaALTLab/cree-intelligent-dictionary/tree/main/src/crkeng/resources/fst
> to follow along! The file itself is stored in Git LFS so is tricky to
> link to directly.

Do an ordinary lookup, to get a list of _concatenated analyses_ for a wordform:

    >>> fst.lookup('atim')
    ['atim+N+A+Sg', 'atimêw+V+TA+Imp+Imm+2Sg+3SgO']

Or get each _parsed analysis_ from the wordform

    >>> analysis = fst.lookup_lemma_with_affixes('atim')[0]
    >>> analysis.lemma
    'atim'
    >>> analysis.suffixes
    ('+N', '+A', '+Sg')

You can also lookup the analyses with symbols separated:

    >>> fst.lookup_symbols('atim')
    [['a', 't', 'i', 'm', '+N', '+A', '+Sg'], ['a', 't', 'i', 'm', 'ê', 'w', '+V', '+TA', '+Imp', '+Imm', '+2Sg', '+3SgO']]


[itwêwina]: https://itwewina.altlab.app
[hfst-optimized-lookup]: https://github.com/hfst/hfst/blob/master/tools/src/hfst-optimized-lookup.cc

## Releasing

Run `./release.py --help` for details of the release process.

A typical release is:

 1. Make sure the “Unreleased” section of `CHANGELOG.md` is up-to-date

 2. Run the script:

        ./release.py --release-timezone=America/Edmonton --push --release
