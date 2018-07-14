"""
    consensys_utils.flask.hooks
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement helpers to set hooks on flask application

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from flask import request


def set_request_id_hook(app):
    # Set hook for request ID (or correlation ID)

    if 'wsgi' in app.config and 'request_id' in app.config['wsgi']:  # pragma: no branch
        @app.before_request
        def set_request_id():
            """Set request id"""
            request.id = request.headers[app.config['wsgi']['request_id']['REQUEST_ID_HEADER']]

    else:
        @app.before_request
        def set_request_id():
            """Set request id"""
            request.id = '-'


DEFAULT_HOOK_SETTERS = {
    'request_id': set_request_id_hook,
}


def set_hooks(app, hook_setters=None):
    """Set hooks on a Flask application

    :param app: Flask application
    :type app: :class:`flask.Flask`
    :param hook_setters: Hooks to set on the application
    :type hook_setters: dict
    """

    hook_setters = hook_setters or {}

    # Set default hooks
    for hook, setter in DEFAULT_HOOK_SETTERS.items():
        hook_setters.setdefault(hook, setter)

    # Set hooks
    for set_hook in hook_setters.values():
        set_hook(app)
