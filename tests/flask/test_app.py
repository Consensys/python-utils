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

from consensys_utils.flask.app import BaseFlaskFactory, FlaskFactory
from ..helpers import set_env_vars


@pytest.fixture(scope='session')
def logging_config_file(files_dir):
    _logging_config_file = os.path.join(files_dir, 'logging.yml')

    reset_env_vars = set_env_vars([('LOGGING_CONFIG_PATH', _logging_config_file)])

    yield _logging_config_file

    reset_env_vars()


@pytest.fixture(scope='session')
def config_file(files_dir, logging_config_file):
    yield os.path.join(files_dir, 'config.yml')


def test_factory(config_file):
    factory = BaseFlaskFactory('test-name')
    assert factory.import_name == 'test-name'
    assert factory(config_path=config_file).import_name == 'test-name'

    factory = BaseFlaskFactory(default_config={}, import_name='test-name')
    assert factory.import_name == 'test-name'
    assert factory(config_file).import_name == 'test-name'

    factory = BaseFlaskFactory('test-name')
    assert factory.import_name == 'test-name'
    assert factory(config_file, import_name='test-name2').import_name == 'test-name2'

    # Test factory does not reload same app given same config
    app = factory(config={'param-test': 'value-test'})
    assert app == factory(config={'param-test': 'value-test'})

    # Test factory reload when expected
    factory.config_path = config_file
    app2 = factory()
    assert app2 != app
    assert app2 == factory()
    assert app2 != factory(config={'param-test': 'value-test'})


@pytest.fixture(scope='session')
def factory():
    yield FlaskFactory(__name__)


@pytest.fixture(scope='function')
def app(factory, config_file):
    _app = factory(config_path=config_file)

    @_app.route('/')
    def test():
        current_app.logger.debug('Test Message')
        return jsonify({'data': 'test'})

    yield _app


def test_app(client, caplog):
    # Test healthcheck extension is on
    assert client.get('/test-healthcheck').status_code == 200

    # Test swagger extension is on
    assert client.get('/test-swagger.json').status_code == 200

    # Test custom logging is on
    with caplog.at_level(logging.DEBUG, logger='app'):
        client.get('/')
    assert caplog.records[0].name == 'app'
