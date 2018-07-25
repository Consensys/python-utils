"""
    consensys_utils.flask.extensions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Declares flask extensions

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

__all__ = [
    'initialize_extensions',
]


def initialize_health_extension(app):
    """Initialize healthcheck extension

    :param app: Flask application
    :type app: :class:`flask.Flask`
    """
    if 'health' in app.config:  # pragma: no branch
        from .health import health
        health.init_app(app)


def initialize_swagger_extension(app):
    """Initialize Swagger extension

    :param app: Flask application
    :type app: :class:`flask.Flask`
    """
    if 'SWAGGER' in app.config:  # pragma: no branch
        from .swagger import swagger
        swagger.init_app(app)


DEFAULT_EXTENSION_INITIATORS = {
    'health': initialize_health_extension,
    'swagger': initialize_swagger_extension,
}


def initialize_extensions(app, extension_initiators=None):
    """Initialize extensions on a Flask application

    By default it applies

    - ``health``: :meth:`initialize_health_extension`
    - ``swagger``: :meth:`initialize_swagger_extension`

    Example: Overriding an extension

    .. doctest::
        >>> from flask import Flask
        >>> from flasgger import Swagger

        >>> app = Flask(__name__)

        >>> swag = Swagger(template={'version': '0.3.4-dev'})

        >>> my_extension_initiators = {'swagger': swag.init_app}

        >>> initialize_extensions(app, my_extension_initiators)

    :param app: Flask application
    :type app: :class:`flask.Flask`
    :param extensions: Dictionary listing extensions
    :type extensions: dict
    """

    extension_initiators = extension_initiators or {}

    # Set default extensions initiator
    for extension, initiator in DEFAULT_EXTENSION_INITIATORS.items():
        extension_initiators.setdefault(extension, initiator)

    # Initialize extensions
    for initialize_extension in extension_initiators.values():
        initialize_extension(app)
