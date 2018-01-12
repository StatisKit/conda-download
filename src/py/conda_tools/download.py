## Copyright [2017-2018] UMR MISTEA INRA, UMR LEPSE INRA,                ##
##                       UMR AGAP CIRAD, EPI Virtual Plants Inria        ##
##                                                                       ##
## This file is part of the StatisKit project. More information can be   ##
## found at                                                              ##
##                                                                       ##
##     http://statiskit.rtfd.io                                          ##
##                                                                       ##
## The Apache Software Foundation (ASF) licenses this file to you under  ##
## the Apache License, Version 2.0 (the "License"); you may not use this ##
## file except in compliance with the License. You should have received  ##
## a copy of the Apache License, Version 2.0 along with this file; see   ##
## the file LICENSE. If not, you may obtain a copy of the License at     ##
##                                                                       ##
##     http://www.apache.org/licenses/LICENSE-2.0                        ##
##                                                                       ##
## Unless required by applicable law or agreed to in writing, software   ##
## distributed under the License is distributed on an "AS IS" BASIS,     ##
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or       ##
## mplied. See the License for the specific language governing           ##
## permissions and limitations under the License.                        ##

import uuid

from collections import defaultdict
from conda_build.metadata import MetaData
from conda_build.config import get_or_merge_config
from conda_build import api as conda_build

from .tools import list_packages

def main(directory, run=True, build=True, test=True, use_local=True, channel_urls=[], config=None):

    config = get_or_merge_config(config, channel_urls=channel_urls)

    metapackage = 'conda-tools-' + uuid.uuid4().hex
    version = "0.1.0"
    build_number = 0
    entry_points = ()
    build_string=None
    home=None
    license=None
    summary=None

    packages = list_packages(directory, channel_urls=channel_urls, config=config)
    dependencies = set()
    if run:
        for package in packages:
            for dependency in package.meta.get("requirements", {}).get("run", []):
                dependencies.add(dependency.split()[0])
    if build:
        for package in packages:
            for dependency in package.meta.get("requirements", {}).get("run", []):
                dependencies.add(dependency.split()[0])
    if test:
        for package in packages:
            for dependency in package.meta.get("test", {}).get("requires", []):
                dependencies.add(dependency.split()[0])
    packages = {package.meta['package']['name'] for package in packages}
    import pdb
    pdb.set_trace()
    dependencies = [dependency for dependency in dependencies if not dependency in packages]

    metapackage = 'conda-tools-' + uuid.uuid4().hex
    metadata = defaultdict(dict)
    metadata['package']['name'] = metapackage
    metadata['package']['version'] = version
    metadata['build']['number'] = build_number
    metadata['build']['entry_points'] = entry_points
    metadata['build']['string'] = build_string
    metadata['requirements']['run'] = dependencies
    metadata['about']['home'] = home
    metadata['about']['license'] = license
    metadata['about']['summary'] = summary
    metadata['test']['commands'] = ['ls [unix]', 'dir [win]']
    metadata = dict(metadata)
    metadata = MetaData.fromdict(metadata, config=config)
    config.compute_build_id(metadata.name())
    conda_build.build(metadata, channel_urls=channel_urls, config=config, need_source_download=False)