"""
    consensys_utils.flask.app
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements a WSGI application object.

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import flask

from .blueprints import register_blueprints
from .config import set_app_config
from .extensions import initialize_extensions, DEFAULT_EXTENSIONS
from .hooks import set_hooks, DEFAULT_HOOK_SETTERS
from .logging import create_logger
from .wsgi import apply_middlewares, DEFAULT_MIDDLEWARES
from ..config import DEFAULT_FLASK_CONFIG_LOADER


class Flask(flask.Flask):
    """ConsenSys-Utils Flask class

    It applies a light overriding on top of :class`flask.Flask` to enable

    - usage of a logger that can be configured from .yml file

    .. _`cfg-loader`: https://cfg-loader.readthedocs.io/en/stable/

    """

    @flask.helpers.locked_cached_property
    def logger(self):
        return create_logger(self)


class BaseFlaskFactory:
    """A factory to create Flask application


    .. doctest::
        >>> from consensys_utils.flask.app import BaseFlaskFactory

        >>> app_factory = BaseFlaskFactory(__name__)

    When creating an application a :class:`FlaskFactory` accomplishes next steps

    #. Initialize Flask application

        By default it creates a :class:`consensys_utils.flask.Flask` application

    #. Set application configuration by using a .yml configuration loader

        You can refer to :meth:`consensys_utils.flask.config.set_app_config` for more information

    #. Apply WSGI middlewares on the application

        You can refer to :meth:`consensys_utils.flask.wsgi.apply_middlewares` for more information

    #. Initialize extensions on the application

        You can refer to :meth:`consensys_utils.flask.extensions.initialize_extensions` for more information

    #. Set hooks on the application

        You can refer to :meth:`consensys_utils.flask.hooks.set_hooks` for more information

    #. Register blueprints on the application

        You can refer to :meth:`consensys_utils.flask.blueprints.register_blueprints` for more information

    It is possible to override default behavior by creating a new class that inherits from :class:`FlaskFactory`

    Example: Adding default hooks

    .. doctest::
        >>> from flask import request

        >>> def set_foo_request_id_hook(app):
        ...     @app.before_request
        ...     def set_request_id():
        ...         request.id = 'foo'

        >>> class CustomFlaskFactory(BaseFlaskFactory):
        ...     default_hook_setters = [set_foo_request_id_hook]


        >>> app_factory = CustomFlaskFactory(__name__)

    :param import_name: The name of the application package
    :type import_name: str
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
    default_middlewares = []

    # Default Flask extensions to initialize
    default_extensions = []

    # Default hooks to set on the application
    default_hook_setters = []

    # Default blueprints to register on the application
    default_blueprints = []

    def __init__(self, import_name=None,
                 yaml_config_loader=DEFAULT_FLASK_CONFIG_LOADER, default_config=None, config_path=None,
                 middlewares=None, extensions=None, hook_setters=None, blueprints=None,
                 **flask_kwargs):
        self.import_name = flask_kwargs.pop('import_name', import_name)
        self.flask_kwargs = flask_kwargs

        self.yaml_config_loader = yaml_config_loader
        self.default_config = default_config or {}
        self.config_path = config_path

        self.middlewares = self.default_middlewares + (middlewares or [])
        self.extensions = self.default_extensions + (extensions or [])
        self.hook_setters = self.default_hook_setters + (hook_setters or [])
        self.blueprints = self.default_blueprints + (blueprints or [])

        self._config = None
        self._app = None

    def init(self, **kwargs):
        """Instantiate Flask application

        :param kwargs: Keyword arguments to provide to the Flask application
        :type kwargs: dict
        """

        # Declare Flask application
        kwargs.update(self.flask_kwargs)
        kwargs.setdefault('import_name', self.import_name)
        self._app = self.flask_class(**kwargs)

        return self._app

    def load_config(self, config_path=None):
        """Load configuration

        :param config_path: Configuration path
        :type config_path: str
        """
        config = self.default_config.copy()
        config.update(self.yaml_config_loader.load(config_path or self.config_path))
        return config

    def set_config(self, config=None):
        """Set application config

        :param raw_config: Optional application config
        :type raw_config: dict
        """

        self._config = self.default_config.copy()
        self._config.update(config or {})

        # Set application configuration
        set_app_config(self._app, config=self._config)

    def apply_middlewares(self):
        """Apply middlewares on application"""

        apply_middlewares(self._app, self.middlewares)

    def initialize_extensions(self):
        """Initialize extensions on application"""

        initialize_extensions(self._app, self.extensions)

    def set_hooks(self):
        """Set hooks on application"""

        set_hooks(self._app, self.hook_setters)

    def register_blueprints(self):
        """Register blueprints on application"""

        register_blueprints(self._app, self.blueprints)

    def create_app(self, config_path=None, config=None, **kwargs):
        """Create an application

        :param config_path: .yml configuration path
        :type config_path: str
        :param config: Optional application config
        :type config: dict
        :param kwargs: Keyword arguments to provide to :attr:`flask_class` when
            instantiating the application object
        :type kwargs dict:
        """

        # Load configuration
        config = config or self.load_config(config_path)
        if config == self._config:
            return self._app

        # Declare new Flask application
        self.init(**kwargs)

        # Set configuration
        self.set_config(config)

        # Apply middlewares
        self.apply_middlewares()

        # Initialize extensions
        self.initialize_extensions()

        # Set hooks
        self.set_hooks()

        # Register blueprints
        self.register_blueprints()

        return self._app

    def __call__(self, *args, **kwargs):
        return self.create_app(*args, **kwargs)


class FlaskFactory(BaseFlaskFactory):
    """ConsenSys Flask factory. It inherits from :meth:`BaseFlaskFactory`

    By default it applies

    **Middlewares**

    - :meth:`consensys_utils.flask.wsgi.apply_request_id_middleware`: A middleware to inject a custom Request ID header

    **Extensions**

    - :meth:`consensys_utils.flask.extensions.initialize_health_extension`: A Flask extension for health check
    - :meth:`consensys_utils.flask.extensions.initialize_swagger_extension`: A Flask extension to add swagger

    **Hooks**

    - :meth:`consensys_utils.flask.hooks.set_request_id_hook`: Hook injecting Request ID header on``flask.request``

    """

    # Default WSGI middleware to apply
    default_middlewares = DEFAULT_MIDDLEWARES

    # Default Flask extensions to initialize
    default_extensions = DEFAULT_EXTENSIONS

    # Default hooks to set on the application
    default_hook_setters = DEFAULT_HOOK_SETTERS
