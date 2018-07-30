"""
    consensys_utils.flask.config
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    App configuration

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""


def set_app_config(app, config=None):
    """Set application configuration

    :param app: Flask application
    :type app: :class:`flask.Flask`
    :param config: Optional Application configuration
    :type config: dict
    """

    if config:
        app.config.update(config)
