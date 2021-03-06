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
import networkx

import os

from collections import defaultdict
# from conda.base.context import sys_rc_path
# from conda.common.serialize import yaml_dump, yaml_load
from conda_build.metadata import MetaData
from conda_build.config import get_or_merge_config
from conda_build import api as conda_build

from .tools import list_packages
from .download import main as download

def main(directory, channel_urls=[], inspect_conda_bld_directory=True, config=None):

    download(directory, test=False, config=config)

    # if os.path.exists(sys_rc_path):
    #     with open(sys_rc_path, 'r') as filehandler:
    #         old_rc_config = yaml_load(filehandler) or None
    # else:
    #     old_rc_config = None
    # with open(sys_rc_path, 'w') as filehandler:
    #     yaml_dump(dict(channels = ["file:///"]),filehandler)

    packages = list_packages(directory, channel_urls=channel_urls, config=config)
    graph = networkx.DiGraph()
    for index, package in enumerate(packages):
        graph.add_node(package.meta['package']['name'], identifier=index)
    for package in packages:
        for dependency in package.meta.get("requirements", {}).get("build", []):
            dependency = dependency.split()[0]
            if graph.has_node(dependency):
                graph.add_edge(dependency, package.meta['package']['name'])
        for dependency in package.meta.get("requirements", {}).get("run", []):
            dependency = dependency.split()[0]
            if graph.has_node(dependency):
                graph.add_edge(dependency, package.meta['package']['name'])
    if not networkx.is_directed_acyclic_graph(graph):
        raise ValueError()
    outputs = [0] * len(packages)

    for package in networkx.topological_sort(graph):
        identifier = graph.node[package]["identifier"]
        package = packages[identifier]
        local_config = get_or_merge_config(config, channel_urls=channel_urls)
        local_config.compute_build_id(package.name())
        output_file_path = conda_build.get_output_file_path(package, config=local_config)
        if isinstance(output_file_path, list):
            output_file_path = output_file_path.pop()
        output_file_path = str(output_file_path)
        if not inspect_conda_bld_directory or not os.path.exists(output_file_path):
            conda_build.build(package, config=local_config, notest=True)
        outputs[identifier] = output_file_path

    download(directory, config=config)
    graph = networkx.DiGraph()
    for index, package in enumerate(packages):
        graph.add_node(package.meta['package']['name'], identifier=index)
    for package in packages:
        for dependency in package.meta.get("requirements", {}).get("run", []):
            dependency = dependency.split()[0]
            if graph.has_node(dependency):
                graph.add_edge(dependency, package.meta['package']['name'])
        for dependency in package.meta.get("test", {}).get("requirements", []):
            dependency = dependency.split()[0]
            if graph.has_node(dependency):
                graph.add_edge(dependency, package.meta['package']['name'])
    if not networkx.is_directed_acyclic_graph(graph):
        raise ValueError()
    for package in networkx.topological_sort(graph):
        identifier = graph.node[package]["identifier"]
        local_config = get_or_merge_config(config, channel_urls=channel_urls)
        local_config.compute_build_id(packages[identifier].name())
        conda_build.test(outputs[identifier], config=local_config)

    # if old_rc_config:
    #     with open(sys_rc_path, 'w') as filehandler:
    #         yaml_dump(old_rc_config, filehandler)
    # else:
    #     os.remove(sys_rc_path)