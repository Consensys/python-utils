"""
    consensys_utils.flask.wsgi
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement helpers to apply WSGI middlewares on flask application

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""


def apply_request_id_middleware(app):
    """Apply a :meth:`consensys_utils.wsgi.RequestIDMiddleware` on a Flask application

    :param app: Flask application
    :type app: :class:`flask.Flask`
    """
    if 'wsgi' in app.config and 'request_id' in app.config['wsgi']:  # pragma: no branch
        from ..wsgi import RequestIDMiddleware
        app.wsgi_app = RequestIDMiddleware(app.wsgi_app, config=app.config['wsgi']['request_id'])


DEFAULT_MIDDLEWARE_APPLIERS = {
    'request_id': apply_request_id_middleware,
}


def apply_middlewares(app, middleware_appliers=None):
    """Apply WSGI middlewares to a Flasks application

    Example:

    .. doctest::
        >>> from flask import Flask
        >>> import base64

        >>> app = Flask(__name__)

        >>> class AuthMiddleware:
        ...     def __init__(self, wsgi):
        ...         self.wsgi = wsgi
        ...
        ...     @staticmethod
        ...     def is_authenticated(header):
        ...         if not header:
        ...             return False
        ...         _, encoded = header.split(None, 1)
        ...         decoded = base64.b64decode(encoded).decode('UTF-8')
        ...         username, password = decoded.split(':', 1)
        ...         return username == password
        ...
        ...     def __call__(self, environ, start_response):
        ...         if self.is_authenticated(environ.get('HTTP_AUTHORIZATION')):
        ...             return self.wsgi(environ, start_response)
        ...         start_response('401 Authentication Required',
        ...             [('Content-Type', 'text/html'),
        ...              ('WWW-Authenticate', 'Basic realm="Login"')])
        ...         return [b'Login']

        >>> middleware_appliers = {
        ...     'auth': AuthMiddleware,
        ... }
        >>> apply_middlewares(app, middleware_appliers)

    By default it applies

    - ``request_id``: :meth:`apply_request_id_middleware`


    :param app: Flask application
    :type app: :class:`flask.Flask`
    :param middlewares: WSGI middleware to apply on the application.
        Expects a dictionary in which values are either

        - A class taking a wsgi as an argument
        - A function that takes a :class:`flask.Flask` as argument and even eventually apply a middleware on it
    :type middlewares: dict
    """
    middleware_appliers = middleware_appliers or {}

    # Set default middlewares
    for middleware, applier in DEFAULT_MIDDLEWARE_APPLIERS.items():
        middleware_appliers.setdefault(middleware, applier)

    # Apply middlewares
    for apply_middleware in middleware_appliers.values():
        if isinstance(apply_middleware, type):
            app.wsgi_app = apply_middleware(app.wsgi_app)
        else:
            apply_middleware(app)
