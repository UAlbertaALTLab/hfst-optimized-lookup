.. hfst-optimized-lookup documentation master file, created by
   sphinx-quickstart on Mon Feb  8 13:50:23 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

hfst-optimized-lookup for Python
================================

A pip-installable library version of hfst-optimized-lookup_, originally
built for itwêwina_.

.. _itwêwina: https://itwewina.dev/
.. _hfst-optimized-lookup: https://github.com/hfst/hfst/blob/master/tools/src/hfst-optimized-lookup.cc

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Install
-------

.. code-block:: bash

    pip install hfst-optimized-lookup

Usage
-----

.. code-block:: python

    from hfst_optimized_lookup import TransducerFile

    fst = TransducerFile("path/to/transducer.hfstol")

    # Now you can .lookup() in the FST to your heart's content!

See :py:class:`hfst_optimized_lookup._hfst_optimized_lookup.PyTransducerFile` for further usage.

API Documentation
=================

.. autoclass:: hfst_optimized_lookup._hfst_optimized_lookup.PyTransducerFile
   :members:

.. automodule:: hfst_optimized_lookup
   :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

