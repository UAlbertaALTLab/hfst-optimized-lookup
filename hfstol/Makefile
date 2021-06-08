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

hfst-optimized-lookup.cc: ../hfst_optimized_lookup/hfst-optimized-lookup.cc
	cp $< $@
hfst-optimized-lookup.h: ../hfst_optimized_lookup/hfst-optimized-lookup.h
	cp $< $@
