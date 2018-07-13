"""
    tests.config.test_loader
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for config loader

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import os

import pytest
from cfg_loader import ConfigSchema
from marshmallow import fields

from consensys_utils.config.loader import create_yaml_config_loader, CONFIG_FILE_ENV_VAR
from ..helpers import set_env_vars


class ConfigSchemaTest(ConfigSchema):
    param1 = fields.Str()


@pytest.fixture(scope='function')
def yaml_config_loader(config_files_dir):
    _yaml_config_loader = create_yaml_config_loader(ConfigSchemaTest,
                                                    default_config_path=os.path.join(config_files_dir,
                                                                                     'config_test_default.yml'))

    yield _yaml_config_loader


def test_yaml_config_loader(config_files_dir, yaml_config_loader):
    assert yaml_config_loader.load(os.path.join(config_files_dir, 'config_test.yml')) == {
        'param1': 'value',
    }


@pytest.fixture(scope='function')
def yaml_config_loader_default(yaml_config_loader):
    # Ensure environment variable is unset
    reset_env_vars = set_env_vars([(CONFIG_FILE_ENV_VAR, None)])

    yield yaml_config_loader

    reset_env_vars()


def test_yaml_config_loader_default(yaml_config_loader_default):
    assert yaml_config_loader_default.load() == {
        'param1': 'value-default',
    }


@pytest.fixture(scope='function')
def yaml_config_loader_env_var(yaml_config_loader, config_files_dir):
    # Set environment variable
    reset_env_vars = set_env_vars([(CONFIG_FILE_ENV_VAR, os.path.join(config_files_dir, 'config_test_env_var.yml'))])

    yield yaml_config_loader

    reset_env_vars()


def test_yaml_config_loader_env_var(yaml_config_loader_env_var):
    assert yaml_config_loader_env_var.load() == {
        'param1': 'value-env-var',
    }
