SHELL = /bin/bash -eu
.DELETE_ON_ERROR:
.SECONDARY:
.SUFFIXES:

EXT_SUFFIX := $(shell python -c 'import sysconfig; print(sysconfig.get_config_var("EXT_SUFFIX"))')

SONAME = hfst_optimized_lookup/_hfst_optimized_lookup$(EXT_SUFFIX)

.PHONY: test
test: $(SONAME)
	pytest --mypy -s --doctest-glob=README.md

.PHONY: docs
docs: $(SONAME)
	pipenv run $(MAKE) -C docs html

.PHONY: all
all: test

hfst_optimized_lookup/hfst-optimized-lookup.cc: ../hfst-optimized-lookup.cc
	cp $< $@
hfst_optimized_lookup/hfst-optimized-lookup.h: ../hfst-optimized-lookup.h
	cp $< $@

# If any files are out of date, let setup.py handle it
$(SONAME): \
    setup.py \
    hfst_optimized_lookup/TransducerFile.pxd \
    hfst_optimized_lookup/_hfst_optimized_lookup.pyx \
    hfst_optimized_lookup/hfst-optimized-lookup.cc \
    hfst_optimized_lookup/hfst-optimized-lookup.h \

	pipenv run python setup.py build_ext --inplace

black:
	black .

clean::
	rm -f hfst-optimized-lookup

clean::
	rm -f $(SONAME) hfst_optimized_lookup/_hfst_optimized_lookup.cpp
	rm -rf build
