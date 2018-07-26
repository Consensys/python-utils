"""
    tests.flask.test_app
    ~~~~~~~~~~~~~~~~~~~~

    Test Flask app creation features

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import logging
import os

import pytest
from flask import current_app, jsonify

from consensys_utils.flask import FlaskFactory
from ..helpers import set_env_vars


@pytest.fixture(scope='session')
def config_file(files_dir):
    yield os.path.join(files_dir, 'config.yml')


@pytest.fixture(scope='session')
def logging_config_file(files_dir):
    yield os.path.join(files_dir, 'logging.yml')


@pytest.fixture(scope='session')
def create_app():
    yield FlaskFactory()


@pytest.fixture(scope='function')
def app(create_app, config_file, logging_config_file):
    reset_env_vars = set_env_vars([('LOGGING_CONFIG_PATH', logging_config_file)])

    _app = create_app(__name__, config_path=config_file)

    @_app.route('/')
    def test():
        current_app.logger.debug('Test Message')
        return jsonify({'data': 'test'})

    yield _app

    reset_env_vars()


def test_factory(client, caplog):
    # Test healthcheck extension is on
    assert client.get('/test-healthcheck').status_code == 200

    # Test swagger extension is on
    assert client.get('/test-swagger.json').status_code == 200

    # Test custom logging is on
    with caplog.at_level(logging.DEBUG, logger='app'):
        client.get('/')
    assert caplog.records[0].name == 'app'
