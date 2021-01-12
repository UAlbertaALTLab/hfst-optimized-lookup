# The intent here is:
#   - When building from a git checkout, run Cython on the `.pyx` file to
#     get a `.cpp` file to go to pypi
#   - When installing from pypi, ready-to-compile C++ files are included,
#     with no need to run Cython or even have it installed
#
# See also:
#  - https://martinsosic.com/development/2016/02/08/wrapping-c-library-as-python-module.html
#  - https://discuss.python.org/t/building-extension-modules-the-2020-way/5950/25
#  - https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#basic-setup-py
#  - https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules

from os import path
from pathlib import Path
from setuptools import setup, Extension


def file1_is_newer_than_file2(file1, file2):
    """Like `file1 -nt file2` in bash; returns true if file2 doesn’t exist.

    Good for file-is-out-of-date checks, as logic reflects make’s default.
    """
    path1 = Path(file1)
    path2 = Path(file2)
    if not path2.exists():
        return True
    if not path1.exists():
        return False
    return path1.stat().st_mtime > path2.stat().st_mtime


# The importable name of the python package, not the PyPI package name
# which has hyphens instead of underscores and goes in `setup(name=)`.
packages = ["hfst_optimized_lookup"]

cython_source_stem = "hfst_optimized_lookup/_hfst_optimized_lookup"

use_cython = file1_is_newer_than_file2(
    f"{cython_source_stem}.pyx", f"{cython_source_stem}.cpp"
)


ext = ".pyx" if use_cython else ".cpp"
sources = [
    f"{cython_source_stem}{ext}",
    "hfst_optimized_lookup/hfst-optimized-lookup.cc",
]

extensions = [
    Extension("hfst_optimized_lookup._hfstol", sources=sources, language="c++")
]

if use_cython:
    from Cython.Build import cythonize

    extensions = cythonize(extensions, language_level=3)

# https://packaging.python.org/guides/making-a-pypi-friendly-readme/#including-your-readme-in-your-package-s-metadata
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hfst-optimized-lookup",
    version="0.0.3",
    ext_modules=extensions,
    packages=packages,
    url="https://github.com/UAlbertaALTLab/hfst-optimized-lookup",
    author="Andrew Neitsch",
    author_email="178162+andrewdotn@users.noreply.github.com",
    description="A pip-installable library version of hfst-optimized-lookup from https://hfst.github.io/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Text Processing :: Linguistic",
    ],
)
