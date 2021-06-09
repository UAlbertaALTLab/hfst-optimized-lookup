SHELL = /bin/bash -eu
.DELETE_ON_ERROR:
.SECONDARY:
.SUFFIXES:

.PHONY: all bootstrap build test

all: bootstrap build test

bootstrap:
	if ! [ -d node_modules ]; then \
		yarn; \
	fi

build:
	npx node-gyp build

test: build
	npx mocha

bootstrap: hfst-optimized-lookup.cc hfst-optimized-lookup.h

hfst-optimized-lookup.cc: ../hfst-optimized-lookup.cc
	cp $< $@
hfst-optimized-lookup.h: ../hfst-optimized-lookup.h
	cp $< $@
