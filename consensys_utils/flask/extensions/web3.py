"""
    app.extensions.web3
    ~~~~~~~~~~~~~~~~~~~

    Declares Flask-Web3 extension

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import flask_web3

from ...web3 import create_provider


class FlaskWeb3(flask_web3.FlaskWeb3):
    """A Flask-Web3 class that supports initializing application with configuration
     in format :meth:`consensys_utils.config.schema.flask.ConfigSchema`

     You can customize this class the same you would do with :class:`flask_web3.FlaskWeb3`
     """

    def init_app(self, app):
        """Initialize application

        :param app: Flask application or blueprint object to extend
        :type app: flask.Flask
        """

        # Create a provider
        self.providers = self.create_provider(app.config.get('web3'))

        # Attached the extension to the app
        app.web3 = self


web3 = FlaskWeb3(create_provider=create_provider)
