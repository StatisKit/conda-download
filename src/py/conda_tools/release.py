import uuid
import networkx

from collections import defaultdict
from conda_build.metadata import MetaData
from conda_build.config import get_or_merge_config
from conda_build import api as conda_build

from .tools import list_packages
from .download import main as download

def main(directory, channel_urls=[], config=None):

    config = get_or_merge_config(config, channel_urls=channel_urls)

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
    for package in networkx.topological_sort(graph):
        identifier = graph.node[package]["identifier"]
        package = packages[identifier]
        config.compute_build_id(package.name())
        conda_build.build(package, config=config, notest=True)
        outputs[identifier] = conda_build.get_output_file_path(package, config=config)
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
