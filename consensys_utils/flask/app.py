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
from .extensions import initialize_extensions, DEFAULT_EXTENSIONS
from .hooks import set_hooks, DEFAULT_HOOK_SETTERS
from .logging import create_logger
from .wsgi import apply_middlewares, DEFAULT_MIDDLEWARES
from ..config import DEFAULT_FLASK_CONFIG_LOADER


class Flask(flask.Flask):
    """ConsenSys-Utils Flask class

    It applies a light overriding on top of :class`flask.Flask` to enable

    - usage of `cfg-loader`_ features for configuration loading
    - usage of a logger that can be configured from .yml file

    .. _`cfg-loader`: https://cfg-loader.readthedocs.io/en/stable/

    """

    config_class = Config

    @flask.helpers.locked_cached_property
    def logger(self):
        return create_logger(self)


class FlaskFactory:
    """A factory to create Flask application


    .. doctest::
        >>> from consensys_utils.flask import FlaskFactory

        >>> create_app = FlaskFactory()

    When creating an application a :class:`FlaskFactory` accomplishes next steps

    #. Initialize Flask application

        By default it creates a :class:`consensys_utils.flask.Flask` application

    #. Set application configuration by using a .yml configuration loader

        You can refer to :meth:`consensys_utils.flask.config.set_app_config` for more information

    #. Apply WSGI middlewares on the application

        By default it applies next middlewares on an application

        - ``request_id``: :meth:`consensys_utils.flask.wsgi.apply_request_id_middleware`

        You can refer to :meth:`consensys_utils.flask.wsgi.apply_middlewares` for more information

    #. Initialize extensions on the application

        By default it applies next extensions on an application

        - ``health``: :meth:`consensys_utils.flask.extensions.initialize_health_extension`
        - ``swagger``: :meth:`consensys_utils.flask.extensions.initialize_swagger_extension`

        You can refer to :meth:`consensys_utils.flask.extensions.initialize_extensions` for more information

    #. Set hooks on the application

        By default it applies next hook on the application

        - ``request_id``: :meth:`consensys_utils.flask.hooks.set_request_id_hook`

        You can refer to :meth:`consensys_utils.flask.hooks.set_hooks` for more information

    #. Register blueprints on the application

        You can refer to :meth:`consensys_utils.flask.blueprints.register_blueprints` for more information

    It is possible to override default behavior by creating a new class that inherits from :class:`FlaskFactory`

    Example: Overriding default hooks

    .. doctest::
        >>> from flask import request

        >>> def set_custom_request_id_hook(app):
        ...     @app.before_request
        ...     def set_request_id():
        ...         request .id = 'foo'

        >>> class CustomFlaskFactory(FlaskFactory):
        ...     default_hook_setters = {'request_id': set_custom_request_id_hook}


        >>> create_app = CustomFlaskFactory()

    :param yaml_config_loader: Optional config loader
    :type yaml_config_loader: :class:`cfg_loader.loader.YamlConfigLoader`
    :param middlewares: Middlewares to apply on the application
        (c.f :meth:`consensys_utils.flask.wsgi.apply_middlewares`)
    :type middlewares: dict
    :param extensions: Extensions to initiate on the application
        (c.f. :meth:`consensys_utils.flask.extensions.initialize_extensions`)
    :type extensions: dict
    :param hook_setters: Hooks to set on the application
        (c.f. :meth:`consensys_utils.flask.hooks.set_hooks`)
    :type hook_setters: dict
    :param blueprints: Blueprints to register on the application
        (c.f. :meth:`consensys_utils.flask.blueprints.register_blueprints`)
    :type blueprints: dict
    """

    # Flask class to use to instantiate applications
    flask_class = Flask

    # Default WSGI middleware to apply
    default_middlewares = DEFAULT_MIDDLEWARES

    # Default Flask extensions to initialize
    default_extensions = DEFAULT_EXTENSIONS

    # Default hooks to set on the application
    default_hook_setters = DEFAULT_HOOK_SETTERS

    # Default blueprints to register on the application
    default_blueprints = {}

    def __init__(self,
                 yaml_config_loader=DEFAULT_FLASK_CONFIG_LOADER,
                 middlewares=None, extensions=None, hook_setters=None, blueprints=None):
        self.yaml_config_loader = yaml_config_loader

        self.middlewares = self.default_middlewares.copy()
        self.middlewares.update(middlewares or {})

        self.extensions = self.default_extensions.copy()
        self.extensions.update(extensions or {})

        self.hook_setters = self.default_hook_setters.copy()
        self.hook_setters.update(hook_setters or {})

        self.blueprints = self.default_blueprints.copy()
        self.blueprints.update(blueprints or {})

        self.app = None

    def init(self, import_name, *args, **kwargs):
        """Instantiate Flask application

        :param import_name: The name of the application package
        :type import_name: str
        """

        # Declare Flask application
        self.app = self.flask_class(import_name, *args, **kwargs)
        return self.app

    def set_config(self, config=None, config_path=None):
        """Set application config

        :param config: Optional application config
        :type config: dict
        :param config_path: Configuration path
        :type config_path: str
        """

        # Set application configuration
        set_app_config(self.app,
                       config=config,
                       yaml_config_loader=self.yaml_config_loader,
                       config_path=config_path)
        self.app.logger.info("Application configured for {env}...".format(env=self.app.config.get('ENV')))

    def apply_middlewares(self):
        """Apply middlewares on application"""

        apply_middlewares(self.app, self.middlewares)

    def initialize_extensions(self):
        """Initialize extensions on application"""

        initialize_extensions(self.app, self.extensions)

    def set_hooks(self):
        """Set hooks on application"""

        set_hooks(self.app, self.hook_setters)

    def register_blueprints(self):
        """Register blueprints on application"""

        register_blueprints(self.app, self.blueprints)

    def create(self, import_name, *args, config=None, config_path=None, **kwargs):
        """Create an application
        register_blueprints
        :param import_name: The name of the application package
        :type import_name: str
        :param config: Optional application config
        :type config: dict
        :param config_path: .yml configuration path
        :type config_path: str
        """

        # Declare Flask application
        self.init(*args, import_name, **kwargs)

        # Set configuration
        self.set_config(config, config_path)

        # Apply middlewares
        self.apply_middlewares()

        # Initialize extensions
        self.initialize_extensions()

        # Set hooks
        self.set_hooks()

        # Register blueprints
        self.register_blueprints()

        return self.app

    def __call__(self, *args, **kwargs):
        return self.create(*args, **kwargs)
