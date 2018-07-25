"""
    consensys_utils.flask.app
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements a WSGI application object.

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import flask

from .blueprints import register_blueprints
from .config import Config, set_app_config
from .extensions import initialize_extensions
from .hooks import set_hooks
from .logging import create_logger
from .wsgi import apply_middlewares
from ..config import DEFAULT_FLASK_CONFIG_LOADER


class Flask(flask.Flask):
    """Flask class

    ConsenSys utils applies a light class overload on top of Flask to enable

    - usage of :module:`cfg_loader` features for configuration loading
    - usage of a logger that can be configured from .yml file
    """

    config_class = Config

    @flask.helpers.locked_cached_property
    def logger(self):
        return create_logger(self)


def create_app(import_name, *args,
               config=None, yaml_config_loader=DEFAULT_FLASK_CONFIG_LOADER, config_path=None,
               middleware_appliers=None, extension_initiators=None, hook_setters=None,
               blueprint_registers=None, command_adders=None,
               flask_class=Flask, **kwargs):
    """Create a Flask application

    :param import_name: The name of the application package
    :type import_name: str
    :param config: Optional application config
    :type config: dict
    :param yaml_config_loader: Optional config loader
    :type yaml_config_loader: :class:`cfg_loader.loader.YamlConfigLoader`
    :param config_path: Configuration path
    :type config_path: str
    :param middleware_appliers: Middlewares to apply on the application
    :type middleware_appliers: dict
    :param extension_initiators: Extensions to initiate on the application
    :type extension_initiators: dict
    :param hook_setters: Hooks to set on the application
    :type hook_setters: dict
    :param blueprint_registers: Blueprints to register on the application
    :type blueprint_registers: dict
    :param flask_class: Flask class to use to instantiate the application
    :type flask_class: Subclass of :class:`Flask`
    """

    # Declare Flask application
    app = flask_class(import_name, *args, **kwargs)

    # Set application configuration
    set_app_config(app,
                   config=config,
                   yaml_config_loader=yaml_config_loader,
                   config_path=config_path)
    app.logger.info("Application configured for {env}...".format(env=app.config.get('ENV')))

    # Apply middlewares
    apply_middlewares(app, middleware_appliers=middleware_appliers)

    # Initialize extensions
    initialize_extensions(app, extension_initiators=extension_initiators)

    # Set hooks
    set_hooks(app, hook_setters=hook_setters)

    # Register blueprints
    register_blueprints(app, blueprint_registers=blueprint_registers)

    return app
