"""
    consensys_utils.flask.app
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements a WSGI application object.

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from .config import Config
from .logging import create_logger
from ..config.schema.flask import ConfigSchema
from ..utils import import_optional_module

flask = import_optional_module('flask')


class Flask(flask.Flask):
    """Flask app class

    We slightly customize

    - config_class to handle .yaml configuration loading
    - logger to load logging info from .yml file
    """

    config_class = Config

    def __init__(self, *args, config_schema=ConfigSchema, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_schema = config_schema

    @flask.helpers.locked_cached_property
    def logger(self):
        return create_logger(self)
