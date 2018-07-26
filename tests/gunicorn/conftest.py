"""
    tests.gunicorn.conftest
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os

import pytest


@pytest.fixture(scope='session')
def files_dir(test_dir):
    yield os.path.join(test_dir, 'gunicorn', 'files')


@pytest.fixture(scope='session')
def logging_config_file(files_dir):
    yield os.path.join(files_dir, 'logging.yml')
