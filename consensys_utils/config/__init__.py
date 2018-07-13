"""
    consensys_utils.config
    ~~~~~~~~~~~~~~~~~~~~~~

    Resources used for configuration loading

    Most of the resources in this package rely on Cfg-Loader package
    (c.f. https://github.com/nmvalera/cfg-loader)

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from .loader import create_yaml_config_loader
from .schema import LoggingConfigSchema

__all__ = [
    'LoggingConfigSchema',
    'create_yaml_config_loader',
]
