"""
    consensys_utils.flask.blueprints
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement helpers to set blueprints on flask application

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

DEFAULT_BLUEPRINT_REGISTERS = {}


def register_blueprints(app, blueprint_registers=None):
    """Register blueprints on a Flask application

    :param app: Flask application
    :type app: :class:`flask.Flask`
    :param blueprint_registers: Blueprints to register on the application
    :type blueprint_registers: dict
    """

    blueprint_registers = blueprint_registers or {}

    # Set default hooks
    for blueprint, register in DEFAULT_BLUEPRINT_REGISTERS.items():
        blueprint_registers.setdefault(blueprint, register)

    # Set hooks
    for register in blueprint_registers.values():
        register(app)
