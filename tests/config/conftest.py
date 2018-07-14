"""
    tests.config.conftest
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os

import pytest


@pytest.fixture(scope='session')
def config_files_dir(test_dir):
    yield os.path.join(test_dir, 'config', 'files')
