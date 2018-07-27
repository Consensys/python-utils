"""
    tests.gunicorn.test_schema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test Gunicorn Configuration schema

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import pytest
from consensys_utils.gunicorn.config import Config
from gunicorn.workers.gthread import ThreadWorker

from consensys_utils.config.schema.gunicorn import GunicornConfigSchema
from consensys_utils.gunicorn.logging import Logger


@pytest.fixture(scope='function')
def gunicorn_config():
    yield Config()


def test_gunicorn_config_schema_default(gunicorn_config):
    loaded_config = GunicornConfigSchema().load({})

    for k, v in loaded_config.items():
        gunicorn_config.set(k, v)

    assert gunicorn_config.logger_class == Logger


def test_gunicorn_config_schema_custom(gunicorn_config):
    raw_config = {
        'debugging': {
            'reload': True,
        },
        'server-socket': {
            'bind': [
                '127.0.2.1:8080',
            ],
        },
        'worker-processes': {
            'worker_class': 'gthread',
        },
    }

    loaded_config = GunicornConfigSchema().load(raw_config)

    for k, v in loaded_config.items():
        gunicorn_config.set(k, v)

    assert gunicorn_config.address == [('127.0.2.1', 8080)]
    assert gunicorn_config.worker_class == ThreadWorker
