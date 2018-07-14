"""
    tests.conftest
    ~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os

import pytest

TEST_DIR = os.path.dirname(__file__)


@pytest.fixture(scope='session')
def test_dir():
    yield TEST_DIR


@pytest.fixture(scope='session')
def files_dir(test_dir):
    yield os.path.join(test_dir, 'files')
