"""
    tests.flask.test_config
    ~~~~~~~~~~~~~~~~~~~~~~~

    Test Flask configuration features

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os

import pytest
from cfg_loader import ConfigSchema
from marshmallow import fields

from consensys_utils.config import create_yaml_config_loader
from consensys_utils.flask import Flask
from consensys_utils.flask.config import set_app_config


@pytest.fixture(scope='session')
def config_file(files_dir):
    yield os.path.join(files_dir, 'config-test.yml')


class ConfigSchemaTest(ConfigSchema):
    """Config schema for test"""

    param = fields.Str()


yaml_config_loader_test = create_yaml_config_loader(ConfigSchemaTest)


@pytest.fixture(scope='function')
def app(config_file):
    _app = Flask(__name__)

    set_app_config(_app)
    set_app_config(_app, yaml_config_loader=yaml_config_loader_test, config_path=config_file)
    set_app_config(_app, config={'param2': 'test-value2'})

    yield _app


def test_config(config):
    assert 'param' in config and config['param'] == 'test-value'
    assert 'param2' in config and config['param2'] == 'test-value2'
