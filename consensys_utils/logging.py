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


def create_logger(config):
    """Create logger

    :param config: Logging configuration
    :type config: dict
    """

    if 'LOGGING_CONFIG_PATH' in config:  # pragma: no branch
        # Assumes we are trying to load configuration from a .yml file
        from .utils import import_optional_module
        cfg_loader = import_optional_module('cfg_loader')
        config = cfg_loader.utils.parse_yaml_file(config['LOGGING_CONFIG_PATH'])

    if config:  # pragma: no branch
        dictConfig(config)
