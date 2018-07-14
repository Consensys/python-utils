"""
    tests.flask.test_wsgi
    ~~~~~~~~~~~~~~~~~~~~~

    Test WSGI features

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

from unittest.mock import MagicMock

import pytest
from flask import Flask, request

from consensys_utils.flask.hooks import set_request_id_hook
from consensys_utils.flask.wsgi import apply_request_id_middleware, apply_middlewares


@pytest.fixture(scope='session')
def app():
    _app = Flask(__name__)

    # Set wsgi config
    _app.config['wsgi'] = {'request_id': {'REQUEST_ID_HEADER': 'test-header'}}

    # Apply request id middleware
    apply_request_id_middleware(_app)

    # Set hook to retrieve request id header in flask request object
    set_request_id_hook(_app)

    yield _app


def test_request_id_middleware(client):
    client.get('/')
    assert request.id and isinstance(request.id, str) and request.id != '-'

    headers = [('test-header', 'abcde1234')]
    client.get('/', headers=headers)

    assert request.id == 'abcde1234'


def test_apply_middlewares(client):
    apply_middleware_mock = MagicMock()

    apply_middlewares(client.application, middleware_appliers={'mock': apply_middleware_mock})
    assert apply_middleware_mock.call_args_list[0][0][0] == client.application

    apply_middlewares(client.application, middleware_appliers={'request_id': apply_middleware_mock})
    assert apply_middleware_mock.call_args_list[1][0][0] == client.application
