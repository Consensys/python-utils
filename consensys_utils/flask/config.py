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

    ConsenSys-Utils slightly overrides :class:`~flask.Config` to enable configuration loading from .yml file
    using `cfg-loader`_

    .. _`cfg-loader`: https://cfg-loader.readthedocs.io/en/stable/
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
    :param yaml_config_loader: Optional .yml config loader
    :type yaml_config_loader: :class:`cfg_loader.loader.YamlConfigLoader`
    :param config_path: Path to the .yml config file
    :type config_path: str
    """

    if config:
        app.config.update(config)
    elif yaml_config_loader and hasattr(app.config, 'from_yaml'):
        app.config.from_yaml(yaml_config_loader, config_path)
