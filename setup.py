# type: ignore
# ^ otherwise `pytest --mypy` complains; see “No stub for setuptools?” at
#   https://github.com/python/typeshed/issues/2171

# setup.py for hfst_optimized_lookup
#
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

import os
import platform
import sys
from distutils.version import LooseVersion
from pathlib import Path
from setuptools import setup, Extension
from sysconfig import get_config_vars


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

# The Python that runs setup.py might have been compiled to target old
# versions of macOS on which the C++ library had a different name.
#
# Normally when building an extension you’d want to use the same compiler
# options as were used to build the current Python, but not if those
# compiler options mean that no C++ header files will be found, resulting
# in the error:
#
#     clang: warning: include path for libstdc++ headers not found; pass '-stdlib=libc++' on the command line to use the libc++ standard library instead [-Wstdlibcxx-not-found]
#     hfst_optimized_lookup/_hfst_optimized_lookup.cpp:644:10: fatal error: 'ios' file not found
#     #include "ios"
#              ^~~~~
#     1 error generated.
#
# Setting MACOSX_DEPLOYMENT_TARGET overrides this; according to the
# clang(1) man page, “If -mmacosx-version-min is unspecified, the default
# deployment target is read from this environment variable.’
#
# You can check what version of macOS your Python targets by running:
#
#     import sysconfig
#     print(sysconfig.get_config_var('MACOSX_DEPLOYMENT_TARGET'))
#
# This next conditional is largely borrowed from
# https://github.com/pandas-dev/pandas/blob/a27244dc1993/setup.py#L427-L447
# (BSD-3-Clause)
#
# Also see
# https://github.com/Homebrew/brew/blob/master/docs/C%2B%2B-Standard-Libraries.md
if sys.platform == "darwin" and "MACOSX_DEPLOYMENT_TARGET" not in os.environ:
    current_system = platform.mac_ver()[0]
    python_target = get_config_vars().get("MACOSX_DEPLOYMENT_TARGET", current_system)
    if (
        LooseVersion(str(python_target)) < "10.9"
        and LooseVersion(current_system) >= "10.9"
    ):
        os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"

setup(
    ext_modules=extensions,
    packages=packages,
    # `include_package_data` is one way of triggering an install of the
    # `py.typed` marker file
    include_package_data=True,
    url="https://github.com/UAlbertaALTLab/hfst-optimized-lookup",
    author="Andrew Neitsch",
    author_email="178162+andrewdotn@users.noreply.github.com",
    description="A pip-installable library version of hfst-optimized-lookup from https://hfst.github.io/",
    # https://packaging.python.org/guides/making-a-pypi-friendly-readme/#including-your-readme-in-your-package-s-metadata
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Text Processing :: Linguistic",
    ],
)
