"""
    consensys_utils.gunicorn.logging
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements a Gunicorn Logger that supports ConsenSys-Utils features

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import traceback

from gunicorn import glogging

from ..logging import create_logger
from ..wsgi import header_to_environ_key


class Logger(glogging.Logger):
    """Enrich Gunicorn logger class

    In particular it overrides the following methods

    - `setup` to load logging configuration from a .yml file
    """

    def setup(self, cfg):
        """Setup the logger configuration from .yml file"""
        super().setup(cfg)
        if hasattr(cfg, 'logging') and cfg.logging:  # pragma: no branch
            create_logger(cfg.logging, glogging.CONFIG_DEFAULTS)


class RequestIDLogger(Logger):
    """Gunicorn logger that handles Request ID header"""

    def __init__(self, *args, **kwargs):
        self.request_id_atom = None
        super().__init__(*args, **kwargs)

    def setup(self, cfg):
        super().setup(cfg)
        request_id_header = cfg.wsgi['request_id']['REQUEST_ID_HEADER']
        request_id_environ_key = header_to_environ_key(request_id_header)
        self.request_id_atom = '{%s}e' % request_id_environ_key.lower()

    def access(self, resp, req, environ, request_time):
        """ See http://httpd.apache.org/docs/2.0/logs.html#combined
        for format details
        """

        safe_atoms = self.atoms_wrapper_class(self.atoms(resp, req, environ,
                                                         request_time))

        try:
            # Add an extra id field to be logged for request ID
            self.access_log.info(self.cfg.access_log_format,
                                 safe_atoms,
                                 extra={'id': safe_atoms.get(self.request_id_atom, '-')})
        except Exception:  # pragma: no cover
            self.error(traceback.format_exc())
