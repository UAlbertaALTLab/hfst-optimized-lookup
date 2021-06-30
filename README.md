hfst-optimized-lookup
=====================

Installable package versions of [hfst-optimized-lookup][], originally
built for [itwêwina][].

[itwêwina]: https://itwewina.altlab.app
[hfst-optimized-lookup]: https://github.com/hfst/hfst/blob/master/tools/src/hfst-optimized-lookup.cc

Languages currently supported:
  - [python](python)
  - [NodeJS](node)

[hfst] is a great toolkit with all sorts of functionality, and is
indispensable for building FSTs, but for various applications that only
want to do unweighted hfstol lookups, this package may be easier to use.

[hfst]: https://github.com/hfst/hfst

The `hfst-optimized-lookup` binary is actually a standalone C++ program
that doesn’t `#include` or link against any other code in hfst, which makes
it much easier to repackage.

Among other benefits, this package can return lists of individual symbols,
including Multichar_Symbols, so that you don’t have to guess or try to
parse out which parts of the analysis are tags.

Development notes
-----------------

### Canonical C++ file locations

We’ve edited the `hfst-optimized-lookup` code to add library-friendly
functionality. The canonical versions of our `hfst-optimized-lookup.cc` and
`hfst-optimized-lookup.h` are in this directory, and the `Makefile`s copy
that file into language-specific directories. Some sort of link might be
nicer, to avoid confusion where you edit C++ code while debugging and then
have to remember to copy those changes to the repository root directory for
git to seem them; but releasing packages requires that the C++ files be
included, and that’s far easier with actual files.

### Top-level `Pipfile`

The `Pipfile` is at the top level, instead of in the `python` directory,
because `./mini-lfs-client.py` needs `requests` which implicitly comes from
the `Pipfile`.

Acknowledgements
----------------

Thank you to:

  - The authors of the [Helsinki Finite-State Technology][hfst] library and
    application suite

[hfst]: https://github.com/hfst/hfst
