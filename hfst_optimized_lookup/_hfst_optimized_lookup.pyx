# NOTE: this is compiled to a module called ._hfstol
import os

from libc.stdlib cimport malloc, free
from libc.string cimport strdup
from libcpp.string cimport string as std_string
from libcpp.vector cimport vector

from ._types import Analysis

### String utilities
# These would go into a separate .pyx file if I could get that to compile

# This was tricky to figure out. If a param is declared as `char *`, then Cython
# will only accept `bytes` objects, causing no end of trouble for callers. But:
# “If no type is specified for a parameter or return value, it is assumed to be
# a Python object.” So not specifying a type means we get strings as
# `PyObject`s, which we can call `encode()` on to get `bytes` and pass them to
# the underlying `const char*`-taking function.
cdef bytes_from_cstring(s):
    if not isinstance(s, str):
        raise Exception("Passed non-string")
    return s.encode('UTF-8')


### Now, the definitions for the C++ code


cdef extern from "hfst-optimized-lookup.h":
    cdef cppclass TransducerFile:
        # docs on `except +`: “Without this declaration, C++ exceptions
        # originating from the constructor will not be handled by Cython.”
        TransducerFile(const char* path) except +
        int symbol_count() except +
        vector[vector[std_string]] lookup(const char* input_string) except +


cdef class PyTransducerFile:
    cdef TransducerFile* c_tf # pointer to the C++ instance we're wrapping

    def __cinit__(self, path):
        path = os.fspath(path)
        self.c_tf = new TransducerFile(bytes_from_cstring(path))

    def symbol_count(self):
        return self.c_tf.symbol_count()

    def lookup_symbols(self, string):
        cdef vector[vector[std_string]] results = self.c_tf.lookup(bytes_from_cstring(string))
        return [[x.decode('UTF-8') for x in y] for y in results]

    def lookup(self, string):
        return [''.join(x) for x in self.lookup_symbols(string)]

    def lookup_lemma_with_affixes(self, surface_form):
        raw_analyses =  self.lookup_symbols(surface_form)
        return [_parse_analysis(a) for a in raw_analyses]

    def bulk_lookup(self, words):
        ret = {}
        for w in words:
            ret[w] = set(self.lookup(w))
        return ret

    def __dealloc__(self):
        del self.c_tf


def _parse_analysis(letters_and_tags):
    prefix_tags = []
    lemma_chars = []
    suffix_tags = []
    affixes = prefix_tags

    for symbol in letters_and_tags:
        if len(symbol) == 1:
            affixes = suffix_tags
            lemma_chars.append(symbol)
        else:
            assert len(symbol) > 1
            affixes.append(symbol)

    return Analysis(tuple(prefix_tags), "".join(lemma_chars), tuple(suffix_tags))
