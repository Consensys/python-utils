"""
    consensys_utils.flask.blueprints
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement helpers to set blueprints on flask application

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from flask import Blueprint


def register_blueprints(app, blueprints=None):
    """Register blueprints on a Flask application

    Example:

    .. doctest::
        >>> from flask import Flask, Blueprint

        >>> app = Flask(__name__)

        >>> my_bp1 = Blueprint('my-bp1', __name__)
        >>> my_bp2 = Blueprint('my-bp2', __name__)

        >>> blueprints = [
        ...     lambda app: app.register_blueprint(my_bp1),
        ...     my_bp2,
        ... ]
        >>> register_blueprints(app, blueprints)


    :param app: Flask application
    :type app: :class:`flask.Flask`
    :param blueprints: Blueprints to register on the application.
        Expects a list of elements which elements are either

        - a :class:`flask.Blueprint`
        - a function that takes a :class:`flask.Flask` as argument and eventually register a blueprint on it
    :type blueprints: list
    """

    blueprints = blueprints or []

    # Set hooks
    for blueprint in blueprints:
        if isinstance(blueprint, Blueprint):
            app.register_blueprint(blueprint)
        else:
            blueprint(app)
