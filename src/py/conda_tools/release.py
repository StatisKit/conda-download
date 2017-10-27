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

    config = get_or_merge_config(config, channel_urls=channel_urls)
    download(directory, run=False, test=False, config=config)

    # if os.path.exists(sys_rc_path):
    #     with open(sys_rc_path, 'r') as filehandler:
    #         old_rc_config = yaml_load(filehandler) or None
    # else:
    #     old_rc_config = None
    # with open(sys_rc_path, 'w') as filehandler:
    #     yaml_dump(dict(channels = ["file:///"]),filehandler)

    packages = list_packages(directory, config=config)
    graph = networkx.DiGraph()
    for index, package in enumerate(packages):
        graph.add_node(package.meta['package']['name'], identifier=index)
    for package in packages:
        for dependency in package.meta.get("requirements", {}).get("build", []):
            dependency = dependency.split()[0]
            if graph.has_node(dependency):
                graph.add_edge(dependency, package.meta['package']['name'])
    if not networkx.is_directed_acyclic_graph(graph):
        raise ValueError()
    outputs = [0] * len(packages)
    print(list(networkx.topological_sort(graph)))
    for package in networkx.topological_sort(graph):
        identifier = graph.node[package]["identifier"]
        package = packages[identifier]
        config.compute_build_id(package.name())
        output_file_path = conda_build.get_output_file_path(package, config=config)
        if not inspect_conda_bld_directory or not os.path.exists(output_file_path):
            conda_build.build(package, config=config, notest=True)
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
        config.compute_build_id(packages[identifier].name())
        conda_build.test(outputs[identifier], config=config)

    # if old_rc_config:
    #     with open(sys_rc_path, 'w') as filehandler:
    #         yaml_dump(old_rc_config, filehandler)
    # else:
    #     os.remove(sys_rc_path)