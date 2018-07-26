"""
    tests.gunicorn.test_config
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test Gunicorn configuration features

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

from consensys_utils.gunicorn.config import Config


def test_config():
    cfg = Config()
    assert 'wsgi' in cfg.settings
    assert 'logging' in cfg.settings
