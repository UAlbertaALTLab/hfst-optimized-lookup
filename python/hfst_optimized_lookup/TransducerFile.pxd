"""
Exposes the TransducerFile class in hfst-optimized-lookup.h to Python.
"""

from libcpp.string cimport string as std_string
from libcpp.vector cimport vector

cdef extern from "hfst-optimized-lookup.h":
    cdef cppclass TransducerFile:
        # docs on `except +`: “Without this declaration, C++ exceptions
        # originating from the constructor will not be handled by Cython.”
        TransducerFile(const char* path) except +
        int symbol_count() except +
        vector[vector[std_string]] lookup(const char* input_string) except +
