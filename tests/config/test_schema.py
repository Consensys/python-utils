"""
    tests.config.test_schema
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for config schema

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import os

import pytest
from cfg_loader.exceptions import ValidationError

from consensys_utils.config.schema.gunicorn import GunicornConfigSchema
from consensys_utils.config.schema.logging import LoggingConfigSchema


def test_logging_schema(config_files_dir):
    schema = LoggingConfigSchema()
    raw_config = {
        'LOGGING_CONFIG_PATH': os.path.join(config_files_dir, 'logging.yml'),
    }
    assert schema.load(raw_config) == raw_config


def test_logging_schema_invalid(config_files_dir):
    schema = LoggingConfigSchema()
    raw_config = {
        'LOGGING_CONFIG_PATH': os.path.join(config_files_dir, 'unknown.yml'),
    }
    with pytest.raises(ValidationError):
        schema.load(raw_config)


def test_gunicorn_schema():
    schema = GunicornConfigSchema()
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
            'worker_class': 'tornado',
        },
    }

    loaded_config = schema.load(raw_config)
    assert loaded_config['logger_class'] == 'consensys_utils.gunicorn.logging.Logger'
    assert loaded_config['reload']
    assert loaded_config['worker_class'] == 'tornado'
    assert loaded_config['bind'] == ['127.0.2.1:8080']
