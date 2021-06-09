SHELL = /bin/bash -eu
.DELETE_ON_ERROR:
.SECONDARY:
.SUFFIXES:

.PHONY: all bootstrap build test

all: test

bootstrap:
	if ! [ -d node_modules ]; then \
		yarn; \
	fi
clean::
	rm -rf node_modules

build: bootstrap
	npx node-gyp build
clean::
	rm -rf build

test: build
	npx mocha

bootstrap: hfst-optimized-lookup.cc hfst-optimized-lookup.h

hfst-optimized-lookup.cc: ../hfst-optimized-lookup.cc
	cp $< $@
hfst-optimized-lookup.h: ../hfst-optimized-lookup.h
	cp $< $@

clean::
	rm -f hfst-optimized-lookup.cc hfst-optimized-lookup.h
