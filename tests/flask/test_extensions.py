"""
    tests.flask.test_extensions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test Flask extensions

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import pytest
from flask import Flask

from consensys_utils.flask.extensions import initialize_health_extension, initialize_swagger_extension, \
    initialize_extensions
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


def test_initialize_extensions_default(client, config):
    config['health'] = {'ENDPOINT_URL': '/test-healthcheck'}

    initialize_extensions(client.application)

    assert client.get('/test-healthcheck').status_code == 200


def test_initialize_extensions_custom(client, config):
    config['SWAGGER'] = {'specs': [{'route': '/test-swagger-custom', 'endpoint': 'test-swagger'}]}

    # Declare custom swagger extension
    swagger = Swagger()

    initialize_extensions(client.application, extension_initiators={'swagger': swagger.init_app})

    assert hasattr(client.application, 'swag')
    assert client.application.swag == swagger
    assert client.get('/test-swagger-custom').status_code == 200
