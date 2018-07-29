"""
    consensys_utils.flask.cli
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Flask application CLI commands

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import click
import flask
from click.decorators import _param_memo
from flask.cli import DispatchingApp, \
    get_debug_flag, get_env, call_factory, \
    shell_command, routes_command, CertParamType, _validate_key, \
    pass_script_info


class ScriptInfo(flask.cli.ScriptInfo):
    """Object that helps to load Flask applications in a CLI when using the application factory pattern is used

    :param create_app: Function that creates Flask application
    :type create_app: func
    :param config_path: Optional .yml configuration file path
    :type config_path: str
    """

    def __init__(self, create_app, config_path=None):
        self.create_app = create_app
        self.config_path = config_path

        # A dictionary
        self.data = {}
        self._loaded_config_path = None
        self._loaded_app = None

    def load_app(self):
        """Loads the Flask app (if not yet loaded).

        Calling this multiple times will just result in the already loaded app to
        be returned.
        """
        if self._loaded_app and self.config_path == self._loaded_config_path:
            return self._loaded_app

        app = call_factory(self, self.create_app, arguments=(self.config_path,))

        debug = get_debug_flag()

        # Update the app's debug flag through the descriptor so that other
        # values repopulate as well.
        if debug is not None:  # pragma: no branch
            app.debug = debug

        self._loaded_app = app
        self._loaded_config_path = self.config_path

        return app


@click.command('run', short_help='Runs application')
@click.option('--host', '-h', default='127.0.0.1',
              help='The interface to bind to (non effective in \'production\' mode).')
@click.option('--port', '-p', default=5000,
              help='The port to bind to (non effective in \'production\' mode)..')
@click.option('--cert', type=CertParamType(),
              help='Specify a certificate file to use HTTPS (non effective in \'production\' mode)..')
@click.option('--key',
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              callback=_validate_key, expose_value=False,
              help='The key file to use when specifying a certificate (non effective in \'production\' mode)..')
@click.option('--reload/--no-reload', default=None,
              help='Enable or disable the reloader. By default the reloader '
                   'is active if debug is enabled (non effecdtive in \'production\' mode).')
@click.option('--debugger/--no-debugger', default=None,
              help='Enable or disable the debugger. By default the debugger '
                   'is active if debug is enabled (non effective in \'production\' mode)..')
@click.option('--eager-loading/--lazy-loader', default=None,
              help='Enable or disable eager loading. By default eager '
                   'loading is enabled if the reloader is disabled (non effective in \'production\' mode)..')
@click.option('--with-threads/--without-threads', default=True,
              help='Enable or disable multithreading (non effective in \'production\' mode)..')
@pass_script_info
def run_command(info, host, port, reload, debugger, eager_loading,
                with_threads, cert):
    env = get_env()
    click.echo(' * Environment: {0}'.format(env))

    if env == 'production':
        from ..gunicorn import WSGIApplication
        app = WSGIApplication(loader=info.load_app)
        app.run()

    else:
        debug = get_debug_flag()

        if reload is None:
            reload = debug

        if debugger is None:
            debugger = debug

        if eager_loading is None:
            eager_loading = not reload

        click.echo(' * Debug mode: {0}'.format('on' if debug else 'off'))

        app = DispatchingApp(info.load_app, use_eager_loading=eager_loading)

        from werkzeug.serving import run_simple
        run_simple(host, port, app, use_reloader=reload, use_debugger=debugger,
                   threaded=with_threads, ssl_context=cert)


config_option = click.Option(
    ['--config'],
    default=None,
    help='Application .yml configuration file',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    is_eager=False
)


def with_config_path(f):
    def invoke_with_config_path(ctx):
        info = ctx.find_object(ScriptInfo)
        if info:  # pragma: no branch
            info.config_path = ctx.params.pop('config', None)
        return f(ctx)

    return invoke_with_config_path


class FlaskGroup(flask.cli.FlaskGroup):
    """Special subclass of the :class:`flask.cli.FlaskGroup` that supports ConsenSys-Utils custom commands

    :class:`FlaskGroup` automatically injects --config option on any command run from a :class:`FlaskGroup` CLI

    :param add_default_commands: if this is True then the default run and
        shell commands wil be added.
    :type add_default_commands: bool
    :param create_app: An optional callback that is passed the script info and
        returns the loaded app.
    """

    def __init__(self, *args, create_app=None, add_default_commands=True, **extra):
        super().__init__(*args, create_app=create_app,
                         add_default_commands=False, **extra)

        if add_default_commands:  # pragma: no branch
            self.add_command(run_command)
            self.add_command(shell_command)
            self.add_command(routes_command)

    @staticmethod
    def add_config_option(cmd):
        if isinstance(cmd, click.Command) and config_option not in cmd.params:  # pragma: no branch
            _param_memo(cmd, config_option)
            cmd.invoke = with_config_path(cmd.invoke)

    def add_command(self, cmd, name=None):
        self.add_config_option(cmd)
        super().add_command(cmd, name)

    def get_command(self, ctx, name):
        rv = super().get_command(ctx, name)
        self.add_config_option(rv)
        return rv

    def list_commands(self, ctx):
        rv = super().list_commands(ctx)
        for cmd in rv:
            click.echo(cmd)
            self.add_config_option(cmd)
        return rv

    def main(self, args=None, **kwargs):
        kwargs['obj'] = kwargs.get('obj') or ScriptInfo(create_app=self.create_app)
        return super().main(args, **kwargs)
