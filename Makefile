SHELL = /bin/bash -eu
.DELETE_ON_ERROR:
.SECONDARY:
.SUFFIXES:

.PHONY: all test python clean
all: test python

python:
	$(MAKE) -C python

test:: crk-relaxed-analyzer-for-dictionary.hfstol
	$(MAKE) -C python test
clean::
	$(MAKE) -C python clean

%.hfstol:
	./mini-lfs-client.py UAlbertaALTLab cree-intelligent-dictionary \
		src/crkeng/resources/fst/$@

test:: hfst-optimized-lookup crk-relaxed-analyzer-for-dictionary.hfstol
	echo atim | ./hfst-optimized-lookup -f crk-relaxed-analyzer-for-dictionary.hfstol
clean::
	rm -f crk-relaxed-analyzer-for-dictionary.hfstol

# Make an executable out of our code, so that we can test if it still behaves
# on the command line as hfst-optimized-lookup should
hfst-optimized-lookup: hfst-optimized-lookup.cc hfst-optimized-lookup.h
	g++ -W -Wall -Werror -o $@ $<

clean::
	rm -f hfst-optimized-lookup
