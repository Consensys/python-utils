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
    if 'health' in app.config:  # pragma: no branch
        from .health import health
        health.init_app(app)


def initialize_swagger_extension(app):
    if 'SWAGGER' in app.config:  # pragma: no branch
        from .swagger import swagger
        swagger.init_app(app)


DEFAULT_EXTENSION_INITIATORS = {
    'health': initialize_health_extension,
    'swagger': initialize_swagger_extension,
}


def initialize_extensions(app, extension_initiators=None):
    """Initialize extensions on a Flask application

    :param app: Flask application
    :type app: :class:`flask.Flask`
    :param extensions: Dictionary listing extensions
    :ype extensions: dict
    """

    extension_initiators = extension_initiators or {}

    # Set default extensions initiator
    for extension, initiator in DEFAULT_EXTENSION_INITIATORS.items():
        extension_initiators.setdefault(extension, initiator)

    # Initialize extensions
    for initialize_extension in extension_initiators.values():
        initialize_extension(app)
