"""
    consensys_utils.flask.config
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    App configuration

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import flask


class Config(flask.Config):
    """Application configuration class

    We overide Flask config to enable configuration loading from .yaml file
    """

    def from_yaml(self, yaml_config_loader, config_path=None):
        """Load configuration from .yml file

        :param yaml_config_loader: Yaml configuration loader
        :type yaml_config_loader: :class:`cfg_loader.loader.YamlConfigLoader`
        :param config_path: Path to .yml configuration file
        :type config_path: str
        """

        for key, value in yaml_config_loader.load(config_path).items():
            self[key] = value


def set_app_config(app, config=None, yaml_config_loader=None, config_path=None):
    """Set application configuration

    :param app: Flask application
    :type app: :class:`flask.Flask`
    :param config: Optional Application configuration
    :type config: dict
    :param config_loader: Optional config loader
    :type cfg_loader: :class:`cfg_loader.loader.YamlConfigLoader`
    """

    if config:
        app.config.update(config)
    elif yaml_config_loader and hasattr(app.config, 'from_yaml'):
        app.config.from_yaml(yaml_config_loader, config_path)
