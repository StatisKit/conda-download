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
    license_name=None
    summary=None

    packages = list_packages(directory, config=config)
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
    dependencies = [dependency for dependency in dependencies if not dependency in packages]

    metapackage = 'conda-tools-' + uuid.uuid4().hex
    d = defaultdict(dict)
    d['package']['name'] = metapackage
    d['package']['version'] = version
    d['build']['number'] = build_number
    d['build']['entry_points'] = entry_points
    d['build']['string'] = build_string
    d['requirements']['run'] = dependencies
    d['about']['home'] = home
    d['about']['license'] = license_name
    d['about']['summary'] = summary
    d['test']['commands'] = ['ls [unix]', 'dir [win]']
    d = dict(d)
    m = MetaData.fromdict(d, config=config)
    config.compute_build_id(m.name())
    conda_build.build(m, config=config, need_source_download=False)