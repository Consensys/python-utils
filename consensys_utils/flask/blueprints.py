"""
    consensys_utils.flask.blueprints
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement helpers to set blueprints on flask application

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from flask import Blueprint


def register_blueprints(app, blueprint_registers=None):
    """Register blueprints on a Flask application

    Example:

    .. doctest::
        >>> from flask import Flask, Blueprint

        >>> app = Flask(__name__)

        >>> my_bp1 = Blueprint('my-bp1', __name__)
        >>> my_bp2 = Blueprint('my-bp2', __name__)

        >>> blueprint_registers = {
        ...     'my-bp1': lambda app: app.register_blueprint(my_bp1),
        ...     'my-bp2': my_bp2
        ... }
        >>> register_blueprints(app, blueprint_registers)


    :param app: Flask application
    :type app: :class:`flask.Flask`
    :param blueprint_registers: Blueprints to register on the application
        Expects a dictionary in which values are either
         - a  :class:`flask.Blueprint`
         - a function that takes a :class:`flask.Flask` as argument
    :type blueprint_registers: dict
    """

    blueprint_registers = blueprint_registers or {}

    # Set hooks
    for register in blueprint_registers.values():
        if isinstance(register, Blueprint):
            app.register_blueprint(register)
        else:
            register(app)
