"""
    tests.flask.test_logging
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test Flask logging features

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import logging
import os

import pytest
from flask import current_app, jsonify

from consensys_utils.flask import Flask
from consensys_utils.flask.hooks import set_request_id_hook


@pytest.fixture(scope='session')
def logging_config_file(files_dir):
    yield os.path.join(files_dir, 'logging.yml')


@pytest.fixture(scope='function')
def app():
    _app = Flask(__name__)

    @_app.route('/')
    def test():
        current_app.logger.debug('Test Message')
        return jsonify({'data': 'test'})

    yield _app


def test_default_logging(client, caplog):
    with caplog.at_level(logging.DEBUG, logger='flask.app'):
        client.get('/')
    assert caplog.records[0].name == 'flask.app'


def test_request_id_logging_filter(client, config, caplog, logging_config_file):
    # Set logging config
    config['logging'] = {'LOGGING_CONFIG_PATH': logging_config_file}
    config['wsgi'] = {'request_id': {'REQUEST_ID_HEADER': 'Test-Request-ID'}}

    # Set request_id hook
    set_request_id_hook(client.application)
    with caplog.at_level(logging.DEBUG, logger='app'):
        client.get('/')
    assert caplog.records[0].name == 'app'
    assert caplog.records[0].id == '-'
