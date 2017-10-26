.. image:: https://img.shields.io/badge/License-Apache%202.0-yellow.svg
   :target: https://opensource.org/licenses/Apache-2.0
   
.. image:: https://travis-ci.org/StatisKit/conda-download.svg?branch=master
   :target: https://travis-ci.org/StatisKit/conda-download
  
.. image:: https://ci.appveyor.com/api/projects/status/py9mtxkvd2am4w1b/branch/master
   :target: https://ci.appveyor.com/api/projects/status/py9mtxkvd2am4w1b/branch/master


**conda-tools**: Multiple tools for easing the usage of Conda for developers
============================================================================

**conda-tools** contains tools for:

1. Downloading **Conda** dependencies of recipes.
   This allows to:

   * easily build your own recipes in offline mode,
   * ensure reproducibility of scripts using **Conda** builds or installs.
     
2. Buildind a multiple **Conda** recipes.
   This allows to:
   
   * easily build recipes for a release.
   
     
Installation
------------

conda install -n root conda-tools

Download recipe dependencies
----------------------------

You can easily download all dependencies of conda recipes

.. code-block:: console

    conda download . --build --run

Or equivalently

.. code-block:: console

    conda download .

If you want to download only:

* :code:`build` dependencies use,

  .. code-block:: console

    conda download . --no-run

* :code:`run` dependencies use,

  .. code-block:: console

    conda download . --no-build

To specify custom channels, use the :code:`--channels` option

.. code-block:: console

    conda download . --channels statiskit conda-forge default
