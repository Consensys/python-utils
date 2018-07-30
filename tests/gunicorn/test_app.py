"""
    tests.gunicorn.test_app
    ~~~~~~~~~~~~~~~~~~~~~~~

    Test custom Gunicorn application

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os
from unittest.mock import MagicMock

import pytest
from gunicorn.workers.gthread import ThreadWorker

from consensys_utils.gunicorn.app import WSGIApplication


@pytest.fixture(scope='session')
def gunicorn_config_file(files_dir):
    yield os.path.join(files_dir, 'gconf.py')


def test_wsgi_application(logging_config_file, gunicorn_config_file):
    config = {
        'gunicorn': {
            'bind': ':8080',
            'config': gunicorn_config_file,
        },
        'logging': {
            'LOGGING_CONFIG_PATH': logging_config_file,
        },
        'wsgi': {
            'request_id': {'REQUEST_ID_HEADER': 'Test-Request-ID'},
        }
    }

    # Create a WSGIApplication
    loader_mock = MagicMock(config=config, load_config=lambda: config)
    app = WSGIApplication(loader=loader_mock)

    # Test configuration has been correctly loaded
    assert app.cfg.address == [('', 8080)]
    assert app.cfg.wsgi['request_id']['REQUEST_ID_HEADER'] == 'Test-Request-ID'
    assert app.cfg.worker_class == ThreadWorker

    # Test application loading
    app.load()
    loader_mock.assert_called_once()
