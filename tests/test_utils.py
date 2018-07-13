"""
    tests.test_utils
    ~~~~~~~~~~~~~~~~

    Test utility functions

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import pytest

from consensys_utils.utils import import_optional_module


def test_import_optional_module_missing():
    with pytest.raises(ImportError) as e:
        import_optional_module('missing_module')
    assert str(e.value) == "To use '{}' make sure to have 'missing_module' installed".format(__name__)
