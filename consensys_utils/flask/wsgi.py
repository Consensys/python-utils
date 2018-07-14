"""
    consensys_utils.flask.wsgi
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement helpers to apply WSGI middlewares on flask application

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""


def apply_request_id_middleware(app):
    if 'wsgi' in app.config and 'request_id' in app.config['wsgi']:  # pragma: no branch
        from ..wsgi import RequestIDMiddleware
        app.wsgi_app = RequestIDMiddleware(app.wsgi_app, config=app.config['wsgi']['request_id'])


DEFAULT_MIDDLEWARE_APPLIERS = {
    'request_id': apply_request_id_middleware,
}


def apply_middlewares(app, middleware_appliers=None):
    """Apply WSGI middlewares to a Flasks application

    :param app: Flask application
    :type app: :class:`flask.Flask`
    :param middlewares: WSGI middleware listing middlewares to apply
    :type middlewares: dict
    """
    middleware_appliers = middleware_appliers or {}

    # Set default middlewares
    for middleware, applier in DEFAULT_MIDDLEWARE_APPLIERS.items():
        middleware_appliers.setdefault(middleware, applier)

    # Apply middlewares
    for apply_middleware in middleware_appliers.values():
        apply_middleware(app)
