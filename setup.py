"""
    ConsenSys-Utils
    ~~~~~~~~~~~~~~~

    A set of utility resources used on a daily basis by ConsenSys France Engineering team

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os
import re

from setuptools import setup, find_packages


def read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except FileNotFoundError:
        return ''


def find_version(file):
    """Attempts to find the version number in a file.

    Raises RuntimeError if not found.

    :param file: File where to find version
    :type file: str
    """
    version = ''
    with open(file, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


config_dep = [
    'cfg-loader>=0.2.2',
]

flask_dep = [
    'flask>=1.0.0',
    'flask-restful>=0.3.6',
    'flasgger>=0.8.0',
    'healthcheck>=1.3.0',
    'gunicorn>=19.9.0',
]

setup(
    name='ConsenSys-Utils',
    version=find_version('consensys_utils/__init__.py'),
    license=read('LICENSE'),
    url='https://github.com/ConsenSys/consensys-utils',
    author='Nicolas Maurice',
    author_email='nicolas.maurice@consensys.net',
    maintainer='ConsenSys France',
    description='A set of utility resources used on a daily basis by ConsenSys France Engineering team',
    long_description=read('README.rst'),
    packages=find_packages(),
    extras_require={
        'dev': [
            'flake8',
            'autoflake',
            'autopep8',
            'coverage',
            'pytest>=3',
            'pytest-flask',
            'tox',
            'sphinx',
            'sphinx_rtd_theme',
        ],
        'doc': [
            'sphinx',
            'sphinx_rtd_theme',
        ],
        'config': config_dep,
        'flask': config_dep + flask_dep,
        'all': config_dep + flask_dep,
    },
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests'
)
