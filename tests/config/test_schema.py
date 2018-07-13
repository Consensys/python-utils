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
