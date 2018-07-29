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


def create_app(config_path=None):
    return Flask('test-app')


@pytest.fixture(scope='function')
def script_info():
    yield ScriptInfo(create_app)


def test_script_info(script_info):
    reset_env_vars = set_env_vars([('FLASK_DEBUG', '1')])
    app = script_info.load_app()
    assert app.debug

    # Test the same app is returned when re-loading
    set_env_vars([('FLASK_DEBUG', '0')])
    assert script_info.load_app() == app
    assert app.debug

    reset_env_vars()


def test_flask_group(runner):
    cli = FlaskGroup(create_app=create_app)
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'run' in result.output
    assert 'shell' in result.output
    assert 'routes' in result.output


def test_run_command_development(runner, monkeypatch):
    run_simple_mock = MagicMock()
    monkeypatch.setattr(werkzeug.serving, 'run_simple', run_simple_mock)

    cli = FlaskGroup(create_app=create_app)

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


def test_run_command__production(runner, monkeypatch):
    run_mock = MagicMock()
    monkeypatch.setattr(consensys_utils.gunicorn.WSGIApplication, 'run', run_mock)

    cli = FlaskGroup(create_app=create_app)

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
    cli = FlaskGroup(create_app=mock_create_app)

    # Ensure --config option is listed in command helpers
    result = runner.invoke(cli, ('run', '--help'))
    assert result.exit_code == 0
    assert '--config' in result.output

    # Test in production mode
    reset_env_vars = set_env_vars([('FLASK_ENV', 'production')])
    result = runner.invoke(cli, ('run', '--config', config_path))
    assert result.exit_code == 0
    mock_create_app.assert_called_with(config_path)

    reset_env_vars()


def test_flask_group_app_cli(runner, config_path):
    app = Flask('test-app')

    @app.cli.command('test')
    @with_appcontext
    def test_command():
        click.echo('Test Command on %s' % current_app.import_name)

    # Declare FlaskGroup CLI
    mock_create_app = MagicMock(return_value=app)
    cli = FlaskGroup(create_app=mock_create_app)

    # Test command
    result = runner.invoke(cli, ('test', '--config', config_path))
    mock_create_app.assert_called_with(config_path)
    assert result.exit_code == 0
    assert result.output == 'Test Command on test-app\n'

    # Ensure --config option is listed in command helpers
    result = runner.invoke(cli, ('test', '--help'))
    assert result.exit_code == 0
    assert '--config' in result.output
