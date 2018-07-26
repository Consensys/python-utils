"""
    tests.gunicorn.test_logging
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test Gunicorn logging features

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import datetime
import logging
from types import SimpleNamespace

import pytest

from consensys_utils.gunicorn.config import Config
from consensys_utils.gunicorn.logging import Logger, RequestIDLogger


@pytest.fixture(scope='function')
def cfg(logging_config_file):
    _cfg = Config()
    _cfg.set('logging', {'LOGGING_CONFIG_PATH': logging_config_file})

    yield _cfg


@pytest.fixture(scope='function')
def logger(cfg):

    yield Logger(cfg)


def test_logger(logger):

    assert logger.access_log.handlers[0].name == 'test'


@pytest.fixture(scope='function')
def request_id_logger(cfg):
    cfg.set('wsgi', {'request_id': {'REQUEST_ID_HEADER': 'Test-Request-ID'}})

    yield RequestIDLogger(cfg)


def test_request_id_logger(request_id_logger, caplog):

    response = SimpleNamespace(
        status='200', response_length=1024,
        headers=(('Content-Type', 'application/json'),), sent=1024,
    )
    request = SimpleNamespace(headers=(('Accept', 'application/json'),))
    environ = {
        'REQUEST_METHOD': 'GET', 'RAW_URI': '/my/path?foo=bar',
        'PATH_INFO': '/my/path', 'QUERY_STRING': 'foo=bar',
        'SERVER_PROTOCOL': 'HTTP/1.1', 'HTTP_TEST_REQUEST_ID': 'abcde',
    }
    request_time = datetime.timedelta(seconds=1)

    # Test atoms
    safe_atoms = request_id_logger.atoms(response, request, environ, request_time)
    assert request_id_logger.request_id_atom in safe_atoms and safe_atoms[request_id_logger.request_id_atom] == 'abcde'

    # Test logger id
    with caplog.at_level(logging.DEBUG, logger='gunicorn.access'):
        request_id_logger.access(response, request, environ, request_time)
    assert caplog.records[0].id == 'abcde'
