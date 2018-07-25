"""
    tests.flask.test_cli
    ~~~~~~~~~~~~~~~~~~~~

    Test Flask CLI resources

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

from unittest.mock import MagicMock

import pytest
import werkzeug.serving
from click.testing import CliRunner

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


def test_flask_group(runner, monkeypatch):
    run_mock = MagicMock()
    monkeypatch.setattr(consensys_utils.gunicorn.WSGIApplication, 'run', run_mock)

    cli = FlaskGroup(create_app=create_app)

    # Test in production mode
    reset_env_vars = set_env_vars([('FLASK_ENV', 'production')])
    result = runner.invoke(cli, ('run',))

    assert result.exit_code == 0
    run_mock.assert_called_once()

    run_simple_mock = MagicMock()
    monkeypatch.setattr(werkzeug.serving, 'run_simple', run_simple_mock)

    # Test in development mode
    set_env_vars([('FLASK_ENV', 'development')])

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
