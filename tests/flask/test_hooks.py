"""
    tests.flask.test_hooks
    ~~~~~~~~~~~~~~~~~~~~~~

    Test Flask hooks features

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

from unittest.mock import MagicMock

import pytest
from flask import Flask

from consensys_utils.flask.hooks import set_hooks


@pytest.fixture(scope='function')
def app():
    _app = Flask(__name__)

    yield _app


def test_set_hooks(client):
    mock_hook = MagicMock()

    def set_mock_hook(app):
        @app.before_request
        def test():
            mock_hook()

    hook_setters = [set_mock_hook]

    set_hooks(client.application, hook_setters=hook_setters)

    # Test hook has been correctly set

    client.get('/')
    assert len(mock_hook.call_args_list) == 1
