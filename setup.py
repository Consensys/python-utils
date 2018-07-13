"""
    ConsenSys-Utils
    ~~~~~~~~~~~~~~~

    A set of utility resources used on a daily basis by ConsenSys France Engineering team

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os

from setuptools import setup, find_packages


def read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except FileNotFoundError:
        return ''


config_dep = [
    'cfg-loader>=0.2.0',
]

all_dep = config_dep

setup(
    name='ConsenSys-Utils',
    version='0.1.0-dev',
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
        'all': all_dep,
    },
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests'
)
