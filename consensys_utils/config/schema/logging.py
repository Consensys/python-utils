"""
    consensys_utils.config.schema.logging
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Logging configuration schema

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import cfg_loader


class LoggingConfigSchema(cfg_loader.ConfigSchema):
    """Logging configuration schema

    Describes and validates against

    .. list-table::
        :widths: 30 50 20
        :header-rows: 1

        * - Key
          - Comment
          - Default value

        * - ``LOGGING_CONFIG_PATH``
          - Valid path to a .yml logging configuration file
          - logging.yml
    """

    # Logging file
    LOGGING_CONFIG_PATH = cfg_loader.fields.Path(missing='logging.yml')
