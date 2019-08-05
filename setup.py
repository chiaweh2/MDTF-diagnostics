#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import glob
import subprocess

# Run commands to set up conda environments post-install
# see https://stackoverflow.com/a/36902139
def _post_install():
    envs_to_create = glob.glob('var_code/util/conda_*.yml')
    envs_to_create = ['echo Creating conda env from '+env+'\n' \
            +'conda env create --force -q -f '+ env for env in envs_to_create]
    command_str = '\n'.join(envs_to_create)
    command_str = 'source $(conda info --root)/etc/profile.d/conda.sh\n' \
        + command_str
    process = subprocess.Popen('/usr/bin/env bash', 
        stdin=subprocess.PIPE, shell=True)
    process.communicate(command_str)

class PostDevelopCommand(develop):
    """Post-installation for development mode, same as install for now."""
    def run(self):
        _post_install()
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        _post_install()
        install.run(self)


with open("README.md", 'r') as f:
    long_description = f.read()
packages = find_packages()
setup(
    name='MDTF-diagnostics',
    version='2.1',
    description='Process-oriented diagnostics for weather and climate simulations',
    license='LGPLv3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='MDTF Collaboration',
    author_email='thomas.jackson@noaa.gov',
    url="https://github.com/NOAA-GFDL/MDTF-diagnostics",
    classifiers=[
            # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7'
    ],
    scripts=[
        'mdtf.py'
    ],
    packages=packages,
    cmdclass={ # hook for post-install commands
        'develop': PostDevelopCommand,
        'install': PostInstallCommand
    }
    #   install_requires=[...] #external packages as dependencies
)