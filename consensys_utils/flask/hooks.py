"""
    consensys_utils.flask.hooks
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement helpers to set hooks on flask application

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from flask import request


def set_request_id_hook(app):
    """Set a hook to inject request ID

    It basis on application config to get the request header from which to retrieve request ID

    :param app: Flask application
    :type app: :class:`flask.Flask`
    """
    if 'wsgi' in app.config and 'request_id' in app.config['wsgi']:  # pragma: no branch
        @app.before_request
        def set_request_id():
            """Set request id"""
            request.id = request.headers.get(app.config['wsgi']['request_id']['REQUEST_ID_HEADER']) or '-'


DEFAULT_HOOK_SETTERS = [
    set_request_id_hook,
]


def set_hooks(app, hook_setters=None):
    """Set hooks on a Flask application

    Example: Adding a hook

    .. doctest::
        >>> from flask import Flask, request, current_app

        >>> app = Flask(__name__)

        >>> def set_log_request_hook(app):
        ...     @app.before_request
        ...     def log_request():
        ...         current_app.logger.debug(request)

        >>> my_hook_setters = [set_log_request_hook]

        >>> set_hooks(app, my_hook_setters)

    :param app: Flask application
    :type app: :class:`flask.Flask`
    :param hook_setters: Hooks to set on the application.
        Expects a list of functions that takes a :class:`flask.Flask` as argument
    :type hook_setters: list
    """

    hook_setters = hook_setters or []

    # Set hooks
    for set_hook in hook_setters:
        set_hook(app)
