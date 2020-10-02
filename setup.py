#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

with open('LICENSE', 'r') as f:
    license = f.read()
with open('README.md', 'r') as f:
    readme_desc = f.read()

# Package meta-data.
NAME = 'SmallDevops'
DESCRIPTION = 'free script for continuous integration (CI).'
URL = 'https://github.com/0pb/smalldevops'
AUTHOR = '0pb'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.0.0'

REQUIRED = []

EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

about = {}
if VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=readme_desc,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="GNU V3",
    classifiers=["Intended Audience :: Developers",
               "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
               "Operating System :: POSIX :: Linux",
               "Programming Language :: Python",
               "Programming Language :: Python :: 3",
               "Topic :: Software Development :: Testing"],
)




class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        # self.status('Uploading the package to PyPI via Twine…')
        # os.system('twine upload dist/*')

        # self.status('Pushing git tags…')
        # os.system('git tag v{0}'.format(about['__version__']))
        # os.system('git push --tags')

        sys.exit()
