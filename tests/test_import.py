"""
    tests.test_import
    ~~~~~~~~~~~~~~~~~

    Test import

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import consensys_utils


def _test_version(module):
    assert hasattr(module, '__version__')


def _test_all(module):
    assert hasattr(module, '__all__')


def test_import():
    _test_version(consensys_utils)
    _test_all(consensys_utils)
