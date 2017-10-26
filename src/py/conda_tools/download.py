import uuid

from collections import defaultdict

from conda_build.metadata import MetaData
from conda_build import api as conda_build
from conda_build.config import get_or_merge_config

from .tools import list_packages

def download(directory, run=True, build=True, test=True, use_local=True, channel_urls=[], config=None):

    config = get_or_merge_config(config, channel_urls=channel_urls)

    metapackage = 'conda-tools-' + uuid.uuid4().hex
    version = "0.0.0"
    build_number = 0
    entry_points = ()
    build_string=None
    home=None
    license_name=None
    summary=None

    packages = list_packages(directory)
    dependencies = set()
    if run:
        dependencies.update(*[package[0].meta.get("requirements", {}).get("run", []) for package in packages])
    if build:
        dependencies.update(*[package[0].meta.get("requirements", {}).get("build", []) for package in packages])
    if test:
        dependencies.update(*[package[0].meta.get("test", {}).get("requires", []) for package in packages])
    dependencies = list(dependencies)

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
    d['test']['requirements'] = dependencies
    d['test']['commands'] = ['ls [unix]', 'dir [win]']
    d = dict(d)
    m = MetaData.fromdict(d, config=config)
    config.compute_build_id(m.name())

    return conda_build.build(m, config=config, need_source_download=False)