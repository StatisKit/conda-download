import uuid
import subprocess
import os

from collections import defaultdict
from conda_build.metadata import MetaData
from conda_build import api as conda_build
from conda_env import env as conda_env

def main(environment, version='0.1.0', build_number=0, home=None, license=None, summary=None):
    environment = conda_env.from_file(environment)
    metapackage = environment.name + '-' + uuid.uuid4().hex
    subprocess.check_output(['conda', 'env', 'create', '-n', metapackage, '-f=' + environment.filename])
    packages = subprocess.check_output(['conda', 'list', '-n', metapackage, '-e'])
    packages = [package for package in packages.splitlines() if not package.startswith("#")]
    subprocess.check_output(['conda', 'env', 'remove', '-n', metapackage, '-y'])
    metadata = defaultdict(dict)
    metadata['package']['name'] = environment.name
    metadata['package']['version'] = version
    metadata['build']['number'] = build_number
    metadata['requirements']['run'] = packages
    if home is not None:
        metadata['about']['home'] = home
    if license is not None:
        metadata['about']['license'] = license
    if summary is not None:
        metadata['about']['summary'] = summary
    metadata = dict(metadata)
    config = get_or_merge_config(None, channel_urls=environment.channels)
    metadata = MetaData.fromdict(metadata, config=config)
    config.compute_build_id(metadata.name())
    output_file_path = str(conda_build.get_output_file_path(metadata, config=config).pop())
    if not inspect_conda_bld_directory or not os.path.exists(output_file_path):
        conda_build.build(metadata, config=config)
    return output_file_path
