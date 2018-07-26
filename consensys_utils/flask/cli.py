"""
    consensys_utils.flask.cli
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Flask application CLI commands

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import os

import click
from flask.cli import CertParamType, _validate_key, get_debug_flag, \
    get_env, DispatchingApp, call_factory, AppGroup, get_load_dotenv, load_dotenv


class ScriptInfo:
    """Object that helps to load Flask applications in a CLI when using the application factory pattern

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

        self._loaded_app = None

    def load_app(self):
        """Loads the Flask app (if not yet loaded).

        Calling this multiple times will just result in the already loaded app to
        be returned.
        """
        if self._loaded_app is not None:
            return self._loaded_app

        app = call_factory(self, self.create_app, arguments=(self.config_path,))

        debug = get_debug_flag()

        # Update the app's debug flag through the descriptor so that other
        # values repopulate as well.
        if debug is not None:  # pragma: no branch
            app.debug = debug

        self._loaded_app = app

        return app


pass_script_info = click.make_pass_decorator(ScriptInfo, ensure=True)


@click.command('run', short_help='Runs application it bases on')
@click.option('--config', '-c', default=None,
              help='Application .yml configuration file')
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
def run_command(info, config, host, port, reload, debugger, eager_loading,
                with_threads, cert):
    info.config_path = config

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


class FlaskGroup(AppGroup):
    """Special subclass of the :class:`AppGroup` that supports ConsenSys-Utils custom commands

    :param create_app: An optional callback that is passed the script info and
        returns the loaded app.
    :param load_dotenv: Load the nearest :file:`.env` and :file:`.flaskenv`
        files to set environment variables. Will also change the working
        directory to the directory containing the first file found.
    """

    def __init__(self, create_app=None, load_dotenv=True, **extra):
        params = list(extra.pop('params', None) or ())

        super().__init__(params=params, **extra)
        self.create_app = create_app
        self.load_dotenv = load_dotenv

        self.add_command(run_command)

    def main(self, *args, **kwargs):
        os.environ['FLASK_RUN_FROM_CLI'] = 'true'

        if get_load_dotenv(self.load_dotenv):  # pragma: no branch
            load_dotenv()

        obj = kwargs.get('obj')
        if obj is None:  # pragma: no branch
            kwargs['obj'] = ScriptInfo(create_app=self.create_app)

        kwargs.setdefault('auto_envvar_prefix', 'FLASK')

        return super().main(*args, **kwargs)
