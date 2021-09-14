import os

from libcpp.string cimport string as std_string
from libcpp.vector cimport vector

from .TransducerFile cimport TransducerFile as CppTransducerFile
from hfst_optimized_lookup._types import Analysis


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

cdef public noop():
    """This public function only exists so that Cython creates a header file.

    That’s needed to get a PyInit__hfst_optimized_lookup declaration
    when embedding.
    """

cdef class TransducerFile:
    """
    TransducerFile(path)

    Load an ``.hfstol`` transducer file.

    >>> analyzer = TransducerFile("path/to/fst.hfst")

    Examples usage of an English analyzer:

    >>> analyzer.lookup("bank")
    ['bank+Noun+Sg', 'bank+Verb']
    >>> analyzer.lookup_lemma_with_affixes("bank")
    [Analysis(prefixes=(), lemma="bank", suffixes=("+Noun", "+Sg"), Analysis(prefixes=(), lemma="bank", suffixes=("+Verb",)]
    >>> analyzer.lookup_symbols("bank")
    [['bank', '+Noun', '+Sg'], ['bank', '+Verb']]

    Example usage of an English generator:

    >>> generator.bulk_lookup(["cactus+Noun+Sg", "octopus+Noun+Pl"])
    {"cactus+Noun+Sg", set(["cactuses, cacti"]), "octopus+Noun+Pl": set(["octopuses", "octopi", "octopodes"])}

    :param path: the path to the .hfstol file
    :type path: str or os.PathLike
    """

    cdef CppTransducerFile* c_tf # pointer to the C++ instance we're wrapping

    def __cinit__(self, path):
        path = os.fspath(path)
        self.c_tf = new CppTransducerFile(bytes_from_cstring(path))

    def symbol_count(self):
        """
        symbol_count() -> int

        Returns the number of symbols in the sigma (the symbol table).

        :rtype: int
        """
        return self.c_tf.symbol_count()

    def lookup_symbols(self, string):
        """
        lookup_symbols(string)

        Transduce the input string. The result is a list of tranductions. Each
        tranduction is a list of symbols returned in the model; that is, the symbols are
        not concatenated into a single string.

        :param str string: The string to lookup.
        :return:
        :rtype: list[list[str]]
        """
        cdef vector[vector[std_string]] results = self.c_tf.lookup(bytes_from_cstring(string))
        return [[x.decode('UTF-8') for x in y] for y in results]

    def lookup(self, string):
        """
        lookup(string)

        Lookup the input string, returning a list of tranductions.  This is
        most similar to using ``hfst-optimized-lookup`` on the command line.

        :param str string: The string to lookup.
        :return: list of analyses as concatenated strings, or an empty list if the input
            cannot be analyzed.
        :rtype: list[str]
        """
        return [''.join(x) for x in self.lookup_symbols(string)]

    def lookup_lemma_with_affixes(self, surface_form):
        """
        lookup_lemma_with_affixes(string)

        .. versionadded:: 0.10.0

        Analyze the input string, returning a list
        of :py:class:`hfst_optimized_lookup.Analysis` objects.

        .. note::
            this method assumes an analyzer in which all multicharacter symbols
            represent affixes, and all lexical symbols are contiguous.


        :param str string: The string to lookup.
        :return: list of analyses as :py:class:`hfst_optimized_lookup.Analysis`
            objects, or an empty list if there are no analyses.
        :rtype: list of :py:class:`hfst_optimized_lookup.Analysis`
        """
        raw_analyses =  self.lookup_symbols(surface_form)
        return [_parse_analysis(a) for a in raw_analyses]

    def bulk_lookup(self, words):
        """
        bulk_lookup(words)

        Like ``lookup()`` but applied to multiple inputs. Useful for generating multiple
        surface forms.

        :param words: list of words to lookup
        :type words: list[str]
        :return: a dictionary mapping words in the input to a set of its tranductions
        :rtype: dict[str, set[str]]
        """
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

    # Where should the multicharacter symbols go?  Initially, they are appended prefix
    # tags, but as soon as one "lemma" symbol is seen, the tags should be appeneded to
    # the suffix tags.
    tag_destination = prefix_tags

    for symbol in letters_and_tags:
        if len(symbol) == 1:
            lemma_chars.append(symbol)
            tag_destination = suffix_tags
        else:
            assert len(symbol) > 1
            tag_destination.append(symbol)

    return Analysis(tuple(prefix_tags), "".join(lemma_chars), tuple(suffix_tags))
