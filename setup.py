#!/bin/env python

import collections
import io
import json
import re
import os
from urllib.request import urlopen
from http.client import HTTPException
from socket import timeout
from urllib.error import URLError

from setuptools import setup


def update_databases():
    """update database files from gitlab"""
    _adv = None
    _def = None
    try:
        with urlopen("https://gitlab.manjaro.org/fhdk//raw/master/share/advanced.json") as response:
            _adv = json.loads(response.read().decode("utf8"), object_pairs_hook=collections.OrderedDict)
        with urlopen("https://gitlab.manjaro.org/fhdk//raw/master/share/default.json") as response:
            _def = json.loads(response.read().decode("utf8"), object_pairs_hook=collections.OrderedDict)
    except (HTTPException, json.JSONDecodeError, URLError, timeout):
        pass
    if _adv:
        with open("share/advanced.json", "w") as outfile:
            json.dump(apps, outfile, sort_keys=True, indent=2)
    if _def:
        with open("share/default.json", "w") as outfile:
            json.dump(apps, outfile, sort_keys=True, indent=2)


def read(*names, **kwargs):
    """read"""
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    """find version"""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open('README.md') as readme_file:
    README = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    CHANGELOG = changelog_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

update_databases()

setup(
    name='application-utility',
    version=find_version("application_utility", "__init__.py"),
    description="Package that provides all mirrors for Manjaro Linux.",
    long_description=README + '\n\n' + CHANGELOG,
    author="fhdk, papajoke",
    author_email='fh@manjaro.org',
    url='https://github.com/manjaro/',
    packages=['application_utility',
              'application_utility.browser',
              'application_utility.translation',
              'application_utility.constants'],
    package_dir={'application_utility': 'application_utility'},
    data_files=[('share/applications', ['desktop/application-utility.desktop']),
                ('share/application-utility', ['share/advanced.json',
                                               'share/default.json',
                                               'share/preferences.json'])
                ],
    scripts=["scripts/manjaro-application-utility"],
    install_requires=requirements,
    license="GPL3",
    zip_safe=False,
    keywords='',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End User/Desktop',
        'License :: OSI Approved :: GPL3 License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Environment :: GUI'
    ]
)
