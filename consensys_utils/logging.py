"""
    consensys_utils.logging
    ~~~~~~~~~~~~~~~~~~~~~~~

    Logging resources

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import logging
from logging.config import dictConfig


class IDFilter(logging.Filter):
    """Logging filter that add an ID attribute to log record"""

    def filter(self, record):
        """Add an ID attribute to log record"""

        if not hasattr(record, 'id') or record.id is None:  # pragma: no branch
            record.id = '-'

        return True


def create_logger(config, default_config=None):
    """Create logger

    :param config: Logging configuration
    :type config: dict
    :param default_config: Default logging configuration
    :type default_config: dict
    """

    final_config = (default_config or {}).copy()
    final_config.update(config)

    if 'LOGGING_CONFIG_PATH' in final_config:  # pragma: no branch
        # Assumes we are trying to load configuration from a .yml file
        from cfg_loader.utils import parse_yaml_file
        final_config.update(parse_yaml_file(final_config['LOGGING_CONFIG_PATH']))

    if final_config:  # pragma: no branch
        dictConfig(final_config)
