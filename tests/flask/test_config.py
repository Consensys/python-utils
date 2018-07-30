"""
    tests.flask.test_config
    ~~~~~~~~~~~~~~~~~~~~~~~

    Test Flask configuration features

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import pytest

from consensys_utils.flask import Flask
from consensys_utils.flask.config import set_app_config


@pytest.fixture(scope='function')
def app():
    _app = Flask(__name__)

    set_app_config(_app)
    set_app_config(_app, config={'param': 'test-value'})

    yield _app


def test_config(config):
    assert 'param' in config and config['param'] == 'test-value'
