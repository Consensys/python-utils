"""
    app.config.loader
    ~~~~~~~~~~~~~~~~~

    Configuration loader

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import os

from cfg_loader import YamlConfigLoader  # noqa: E402

# configuration file path
CONFIG_FILE_ENV_VAR = 'CONFIG_FILE'


# Configuration scheme loader
def create_yaml_config_loader(config_schema, default_config_path='config.yml'):
    """Create a configuration loader that can read configuration from .yml file

    :param config_schema: Configuration schema
    :type config_schema: subclass of :class:`cfg_loader.ConfigSchema`
    :param default_config_path: Default path where to load configuration from
    :type default_config_path: str
    """
    return YamlConfigLoader(config_schema,
                            substitution_mapping=os.environ,
                            config_file_env_var=CONFIG_FILE_ENV_VAR,
                            default_config_path=default_config_path)
