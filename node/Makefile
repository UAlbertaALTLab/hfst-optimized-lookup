SHELL = /bin/bash -eu
.DELETE_ON_ERROR:
.SECONDARY:
.SUFFIXES:

.PHONY: all bootstrap build build-js build-c++ test

all: test

bootstrap:
	if ! [ -d node_modules ] || [ package.json -nt node_modules/.yarn-integrity ]; then \
		yarn; \
	fi
clean::
	rm -rf node_modules

build: build-js build-c++

build-js: bootstrap
	npx --no-install tsc
clean::
	rm -rf index.js index.d.ts

build-c++: bootstrap build-js
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
