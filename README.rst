.. Copyright [2017-2018] UMR MISTEA INRA, UMR LEPSE INRA,                ..
..                       UMR AGAP CIRAD, EPI Virtual Plants Inria        ..
..                                                                       ..
.. This file is part of the StatisKit project. More information can be   ..
.. found at                                                              ..
..                                                                       ..
..     http://statiskit.rtfd.io                                          ..
..                                                                       ..
.. The Apache Software Foundation (ASF) licenses this file to you under  ..
.. the Apache License, Version 2.0 (the "License"); you may not use this ..
.. file except in compliance with the License. You should have received  ..
.. a copy of the Apache License, Version 2.0 along with this file; see   ..
.. the file LICENSE. If not, you may obtain a copy of the License at     ..
..                                                                       ..
..     http://www.apache.org/licenses/LICENSE-2.0                        ..
..                                                                       ..
.. Unless required by applicable law or agreed to in writing, software   ..
.. distributed under the License is distributed on an "AS IS" BASIS,     ..
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or       ..
.. mplied. See the License for the specific language governing           ..
.. permissions and limitations under the License.                        ..

.. image:: https://img.shields.io/badge/License-Apache%202.0-yellow.svg
   :target: https://opensource.org/licenses/Apache-2.0
   
.. image:: https://travis-ci.org/StatisKit/conda-tools.svg?branch=master
   :target: https://travis-ci.org/StatisKit/conda-tools
  
.. image:: https://ci.appveyor.com/api/projects/status/uwqs5ft5c5ehcmj4/branch/master
   :target: https://ci.appveyor.com/project/pfernique/conda-tools-7kn1b/branch/master
   
**conda-tools**: Tools for easing the usage of Conda for developers
===================================================================

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
