"""
    consensys_utils.gunicorn.config
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Declares new settings for Gunicorn application

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from gunicorn.config import Setting, validate_dict, Config as _Config


class LoggingConfig(Setting):
    name = "logging"
    section = "Logging"
    validator = validate_dict
    default = {}
    desc = """\
    The logging config to use.
    """


class WSGIConfig(Setting):
    name = "wsgi"
    section = "WSGI"
    validator = validate_dict
    default = {}
    desc = """\
    The WSGI config to use.
    """


class Config(_Config):
    """Ensure Above Settings have been correctly declared"""
