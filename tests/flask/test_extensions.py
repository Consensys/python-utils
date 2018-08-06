"""
    tests.flask.test_extensions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test Flask extensions

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from flask import Flask, jsonify
from flask_web3 import current_web3

from consensys_utils.flask.extensions import initialize_extensions, \
    initialize_health_extension, initialize_swagger_extension, initialize_web3_extension
from consensys_utils.flask.extensions.iterable import FlaskIterable
from consensys_utils.flask.extensions.swagger import Swagger


@pytest.fixture(scope='function')
def app():
    _app = Flask(__name__)

    yield _app


def test_health_extension(client, config):
    # Set config for health
    config['health'] = {'ENDPOINT_URL': '/test-healthcheck'}

    # Initialize extension
    initialize_health_extension(client.application)

    assert client.get('/test-healthcheck').status_code == 200


def test_swagger_extension(client, config):
    # Set config for swagger
    config['SWAGGER'] = {'specs': [{'route': '/test-swagger', 'endpoint': 'test-swagger'}]}

    # Initialize extension
    initialize_swagger_extension(client.application)

    assert hasattr(client.application, 'swag')
    assert client.get('/test-swagger').status_code == 200


def test_web3_extension(client, config):
    # Set config for swagger
    config['web3'] = {'ETHEREUM_PROVIDER': 'test', 'ETHEREUM_ENDPOINT_URI': 'http://localhost:8535'}

    # Initialize extension
    initialize_web3_extension(client.application)

    assert hasattr(client.application, 'web3')

    @client.application.route('/test-web3')
    def test_web3():
        return jsonify(current_web3.eth.blockNumber)

    assert client.get('/test-web3').status_code == 200


def test_iterable_extension(client, config):
    # Test with basic iterator
    iterator = iter(range(3))

    FlaskIterable(iterator, app=client.application)

    assert hasattr(client.application, 'iterator')
    assert hasattr(client.application, '__iter__')
    assert hasattr(client.application, '__next__')

    assert list(client.application) == [0, 1, 2]

    # Test with more advanced iterator
    mock_next = MagicMock()

    class IteratorTest:
        def __init__(self):
            self.meter = 0

        def set_config(self, config):
            self.meter = config['meter']

        def __iter__(self):
            return self

        def __next__(self):
            if self.meter >= 6:
                raise StopIteration
            mock_next(self.meter)
            self.meter += 1

    config['meter'] = 2
    FlaskIterable(IteratorTest, app=client.application)

    assert hasattr(client.application, 'iterator')
    assert hasattr(client.application, '__iter__')
    assert hasattr(client.application, '__next__')

    next(client.application)
    mock_next.assert_called_once_with(2)

    next(client.application)
    mock_next.assert_any_call(3)

    for _ in iter(client.application):
        continue

    mock_next.assert_any_call(4)
    mock_next.assert_any_call(5)


def test_custom_swagger_extension(client, config):
    config['SWAGGER'] = {'specs': [{'route': '/test-swagger', 'endpoint': 'test-swagger'}]}

    swagger = Swagger(template={
        'openapi': '3.0',
        'info': {
            'version': '0.1.0-test',
            'title': 'Test-App',
            'description': 'Test-App API',
        },
        'tags': [
            {'name': 'test', 'description': 'Test'},
        ]
    }, title=None)

    swagger.init_app(client.application)

    assert hasattr(client.application, 'swag')
    assert client.get('/test-swagger').status_code == 200


def test_initialize_extensions(client, config):
    config['SWAGGER'] = {'specs': [{'route': '/test-swagger-custom', 'endpoint': 'test-swagger'}]}

    # Declare custom swagger extension
    swagger = Swagger()

    # Declares a mocked flask extension
    init_app_mock = MagicMock()
    mock_ext = SimpleNamespace(init_app=init_app_mock)

    # Initialize extensions
    extensions = [
        swagger.init_app,
        mock_ext,
    ]

    initialize_extensions(client.application, extensions=extensions)

    assert hasattr(client.application, 'swag')
    assert client.application.swag == swagger
    assert client.get('/test-swagger-custom').status_code == 200
