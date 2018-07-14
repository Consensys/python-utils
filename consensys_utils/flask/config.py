"""
    consensys_utils.flask.config
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    App configuration

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from ..config import create_yaml_config_loader
from ..utils import import_optional_module

flask = import_optional_module('flask')


class Config(flask.Config):
    """Application configuration class

    We overide Flask config to enable configuration loading from .yaml file
    """

    def from_yaml(self, config_path, schema):
        """Load configuration from .yml file

        :param config_path: Path to .yml configuration file
        :type config_path: str
        """
        config_loader = create_yaml_config_loader(schema)
        for key, value in config_loader.load(config_path).items():
            self[key] = value


def set_app_config(app, config_path):
    """Set application configuration

    :param config_path: Path to .yml configuration file
    :type config_path: str
    """

    app.config.from_yaml(config_path, app.config_schema)

    return app.config
