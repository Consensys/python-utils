"""
    tests.flask.test_cli
    ~~~~~~~~~~~~~~~~~~~~

    Test Flask CLI resources

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os
from unittest.mock import MagicMock

import click
import pytest
import werkzeug.serving
from click.testing import CliRunner
from flask import current_app
from flask.cli import with_appcontext

import consensys_utils.gunicorn
from consensys_utils.flask import Flask
from consensys_utils.flask.cli import ScriptInfo, FlaskGroup
from ..helpers import set_env_vars


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(scope='function')
def factory():
    reset_env_vars = set_env_vars([('CONFIG_FILE', None)])

    _mock_factory = MagicMock(return_value=Flask('test-app'))

    yield _mock_factory

    reset_env_vars()


@pytest.fixture(scope='function')
def script_info(factory):
    yield ScriptInfo(factory)


def test_script_info(script_info, factory):
    reset_env_vars = set_env_vars([('FLASK_DEBUG', '1')])

    app = script_info.load_app()
    assert app.import_name == 'test-app'
    factory.assert_called_once()

    reset_env_vars()


def test_flask_group(runner, factory):
    cli = FlaskGroup(app_factory=factory)
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'run' in result.output
    assert 'shell' in result.output
    assert 'routes' in result.output


def test_run_command_development(runner, factory, monkeypatch):
    run_simple_mock = MagicMock()
    monkeypatch.setattr(werkzeug.serving, 'run_simple', run_simple_mock)

    cli = FlaskGroup(app_factory=factory)

    reset_env_vars = set_env_vars([('FLASK_ENV', 'development')])

    # Test with no arg
    result = runner.invoke(cli, ('run',))
    assert result.exit_code == 0
    run_simple_mock.assert_called_once()

    # Test with reload arg
    result = runner.invoke(cli, ('run', '--reload'))
    assert result.exit_code == 0

    # Test with debugger arg
    result = runner.invoke(cli, ('run', '--debugger'))
    assert result.exit_code == 0

    # Test with eager-loading arg
    result = runner.invoke(cli, ('run', '--eager-loading'))
    assert result.exit_code == 0

    reset_env_vars()


def test_run_command__production(runner, factory, monkeypatch):
    run_mock = MagicMock()
    monkeypatch.setattr(consensys_utils.gunicorn.WSGIApplication, 'run', run_mock)

    cli = FlaskGroup(app_factory=factory)

    # Test in production mode
    reset_env_vars = set_env_vars([('FLASK_ENV', 'production')])
    result = runner.invoke(cli, ('run',))

    assert result.exit_code == 0
    run_mock.assert_called_once()

    reset_env_vars()


@pytest.fixture(scope='session')
def config_path(files_dir):
    yield os.path.join(files_dir, 'config-test.yml')


def test_flask_group_with_config(runner, config_path, monkeypatch):
    run_mock = MagicMock()
    monkeypatch.setattr(consensys_utils.gunicorn.WSGIApplication, 'run', run_mock)

    mock_create_app = MagicMock()
    mock_factory = MagicMock(create_app=mock_create_app, config_path=None)
    cli = FlaskGroup(app_factory=mock_factory)

    # Ensure --config option is listed in command helpers
    result = runner.invoke(cli, ('run', '--help'))
    assert result.exit_code == 0
    assert '--config' in result.output

    # Test in production mode
    reset_env_vars = set_env_vars([('FLASK_ENV', 'production')])
    result = runner.invoke(cli, ('run', '--config', config_path))

    assert result.exit_code == 0
    assert mock_factory.config_path == config_path

    reset_env_vars()


def test_flask_group_app_cli(runner, config_path):
    app = Flask('test-app')

    @app.cli.command('test')
    @with_appcontext
    def test_command():
        click.echo('Test Command on %s' % current_app.import_name)

    # Declare FlaskGroup CLI
    mock_factory = MagicMock(return_value=app)
    cli = FlaskGroup(app_factory=mock_factory)

    # Test command
    result = runner.invoke(cli, ('test', '--config', config_path))
    assert mock_factory.config_path == config_path
    assert result.exit_code == 0
    assert result.output == 'Test Command on test-app\n'

    # Ensure --config option is listed in command factory helpers
    result = runner.invoke(cli, ('test', '--help'))
    assert result.exit_code == 0
    assert '--config' in result.output
