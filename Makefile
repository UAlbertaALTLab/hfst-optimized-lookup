SHELL = /bin/bash -eu
.DELETE_ON_ERROR:
.SECONDARY:
.SUFFIXES:

.PHONY: all test test-standalone python node clean
all: test python node

test:: crk-relaxed-analyzer-for-dictionary.hfstol test-standalone

python: crk-relaxed-analyzer-for-dictionary.hfstol
	$(MAKE) -C python
test::
	$(MAKE) -C python test
clean::
	$(MAKE) -C python clean

node: crk-relaxed-analyzer-for-dictionary.hfstol
	$(MAKE) -C node
test::
	$(MAKE) -C node test
clean::
	$(MAKE) -C node clean

%.hfstol:
	./mini-lfs-client.py UAlbertaALTLab cree-intelligent-dictionary \
		src/crkeng/resources/fst/$@

test:: test-standalone

test-standalone: hfst-optimized-lookup crk-relaxed-analyzer-for-dictionary.hfstol
	echo atim \
		| ./hfst-optimized-lookup \
			-f crk-relaxed-analyzer-for-dictionary.hfstol \
		| grep atimêw+V+TA+Imp+Imm+2Sg+3SgO
clean::
	rm -f crk-relaxed-analyzer-for-dictionary.hfstol

# Make an executable out of our code, so that we can test if it still behaves
# on the command line as hfst-optimized-lookup should
hfst-optimized-lookup: hfst-optimized-lookup.cc hfst-optimized-lookup.h
	g++ -W -Wall -Werror -o $@ $<

clean::
	rm -f hfst-optimized-lookup
