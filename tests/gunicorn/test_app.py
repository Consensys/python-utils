"""
    tests.gunicorn.test_app
    ~~~~~~~~~~~~~~~~~~~~~~~

    Test custom Gunicorn application

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os
from types import SimpleNamespace

import pytest

from consensys_utils.gunicorn.app import WSGIApplication


@pytest.fixture(scope='session')
def gunicorn_config_file(files_dir):
    yield os.path.join(files_dir, 'gconf.py')


def test_app(logging_config_file, gunicorn_config_file):
    def loader():
        return SimpleNamespace(config={
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
        })

    app = WSGIApplication(loader=loader)

    assert app.cfg.address == [('', 8080)]
    assert app.cfg.wsgi['request_id']['REQUEST_ID_HEADER'] == 'Test-Request-ID'
    assert app.cfg.worker_class_str == 'async'
