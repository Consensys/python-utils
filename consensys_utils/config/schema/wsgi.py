"""
    consensys_utils.config.schema.wsgi
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    WSGI middlewares configuration schema

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import cfg_loader
from marshmallow import fields


class RequestIDConfigSchema(cfg_loader.ConfigSchema):
    """Request ID Middleware configuration

    Describes and validates against

    .. list-table::
        :widths: 30 50 20
        :header-rows: 1

        * - Key
          - Comment
          - Default value

        * - ``REQUEST_ID_HEADER``
          - Required header where to load/inject correlation ID
          - 'X-Request-ID'
    """

    # Request header indicating request ID (used as correlation ID for logs)
    REQUEST_ID_HEADER = fields.Str(missing='X-Request-ID')


class WSGIConfigSchema(cfg_loader.ConfigSchema):
    """Configuration relative to wsgi middlewares

    Describes and validates against

    .. list-table::
        :widths: 30 50 20
        :header-rows: 1

        * - Key
          - Comment
          - Default value

        * - ``request_id``
          - Request ID configuration in :class:`RequestIDConfigSchema`
          - ``None``
    """

    # Request id middleware section
    request_id = fields.Nested(RequestIDConfigSchema)
