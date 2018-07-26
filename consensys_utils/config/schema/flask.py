"""
    consensys_utils.config.schema.flask
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Flask App configuration Schema

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import cfg_loader
from marshmallow import fields

from .gunicorn import GunicornConfigSchema
from .logging import LoggingConfigSchema
from .wsgi import WSGIConfigSchema


class BaseConfigSchema(cfg_loader.ConfigSchema):
    """Base flask configuration schema

    Describes and validates against

    .. list-table::
        :widths: 30 50 20
        :header-rows: 1

        * - Key
          - Comment
          - Default value

        * - ``APP_NAME``
          - Required name of the application
          - Required
    """

    # Name of the app
    APP_NAME = fields.Str(required=True)


class CookieConfigSchema(cfg_loader.ConfigSchema):
    """Flask Session cookie configuration

    Describes and validates against

    .. list-table::
        :widths: 30 50 20
        :header-rows: 1

        * - Key
          - Comment
          - Default value

        * - ``NAME``
          - The name of the session cookie
          - 'session'

        * - ``DOMAIN``
          - The domain match rule that the session cookie will be valid for
          - ``None``

        * - ``PATH``
          - Path to the session cookie will be valid for
          - ``None``

        * - ``HTTPONLY``
          - Browsers will not allow JavaScript access to cookies marked as “HTTP only” for security
          - ``True``

        * - ``SECURE``
          - Browsers will only send cookies with requests over HTTPSd
          - ``False``

        * - ``SAMESITE``
          - Restrict how cookies are sent with requests from external sites
          - ``None``
    """

    NAME = fields.Str(missing='session')
    DOMAIN = fields.Str()
    PATH = fields.Str()
    HTTPONLY = fields.Bool(missing=True)
    SECURE = fields.Bool(missing=False)
    SAMESITE = fields.Str()


class SessionConfigSchema(cfg_loader.ConfigSchema):
    """Flask Session configuration

    Describes and validates against

    .. list-table::
        :widths: 30 50 20
        :header-rows: 1

        * - Key
          - Comment
          - Default value

        * - ``cookie``
          - Session cookie configuration in :class:`CookieConfigSchema` format
          - :class:`CookieConfigSchema` default

        * - ``REFRESH_EACH_REQUEST``
          - Control whether the cookie is sent with every response
          - ``True``
    """

    cookie = cfg_loader.fields.UnwrapNested(CookieConfigSchema,
                                            missing=CookieConfigSchema().load({}),
                                            prefix='COOKIE_')
    REFRESH_EACH_REQUEST = fields.Bool(missing=True)


class HealthCheckConfigSchema(cfg_loader.ConfigSchema):
    """Healthcheck configuration configuration schema

    Describes and validates against

    .. list-table::
        :widths: 30 50 20
        :header-rows: 1

        * - Key
          - Comment
          - Default value

        * - ``ENDPOINT_URL``
          - Endpoint URL for healthcheck
          - `/healthcheck`
    """

    ENDPOINT_URL = fields.Str(missing='/healthcheck')


class SwaggerSpecConfigSchema(cfg_loader.ConfigSchema):
    """Swagger UI Specification configuration schema

    Describes and validates against

    .. list-table::
        :widths: 30 50 20
        :header-rows: 1

        * - Key
          - Comment
          - Default value

        * - ``ENDPOINT``
          - Swagger-UI endpoint
          - 'apispec_1'

        * - ``ROUTE``
          - Endpoint of the json spec of the API
          - '/apispec_1.json'
    """

    ENDPOINT = fields.Str(missing='apispec_1', attribute='endpoint')
    ROUTE = fields.Str(missing='/apispec_1.json', attribute='route')


class SwaggerConfigSchema(cfg_loader.ConfigSchema):
    """Swagger configuration

    .. list-table::
        :widths: 30 50 20
        :header-rows: 1

        * - Key
          - Comment
          - Default value

        * - ``specs``
          - List of Swagger-UI specs in :class:`SwaggerSpecConfigSchema` format
          - [{'ENDPOINT': 'apispec_1', 'ROUTE': '/apispec_1.json'}]

        * - ``STATIC_URL_PATH``
          - Endpoint for Swagger static files
          - '/flasgger_static'

        * - ``SWAGGER_UI``
          - Boolean indicating if Swagger UI should be activated
          - ``False``

        * - ``SPECS_ROUTE``
          - Route to retrieve specifications
          - '/apidocs/'
    """

    specs = fields.List(fields.Nested(SwaggerSpecConfigSchema),
                        missing=[SwaggerSpecConfigSchema().load({})])
    STATIC_URL_PATH = fields.Str(missing='/flasgger_static', attribute='static_url_path')
    SWAGGER_UI = fields.Bool(missing=False, attribute='swagger_ui')
    SPECS_ROUTE = fields.Str(missing='/apidocs/', attribute='specs_route')


class FlaskConfigSchema(cfg_loader.ConfigSchema):
    """Flask application configuration schema

    Describes and validates against

    .. list-table::
        :widths: 30 50 20
        :header-rows: 1

        * - Key
          - Comment
          - Default value

        * - ``base``
          - Required base configuration in :class:`BaseConfigSchema` format
          - :class:`BaseConfigSchema` default

        * - ``session``
          - Cookie session configuration in :class:`SessionConfigSchema` format
          - :class:`SessionConfigSchema` default

        * - ``PERMANENT_SESSION_LIFETIME``
          - Cookie’s expiration in number of seconds
          - 2678400

        * - ``healthcheck``
          - Healthcheck configuration in :class:`HealthCheckConfigSchema` format
          -

        * - ``swagger``
          - Swagger configuration in :class:`SwaggerConfigSchema` format
          -
    """

    # Base config section
    base = cfg_loader.fields.UnwrapNested(BaseConfigSchema, required=True)

    session = cfg_loader.fields.UnwrapNested(SessionConfigSchema,
                                             missing=SessionConfigSchema().load({}), prefix='SESSION_')
    PERMANENT_SESSION_LIFETIME = fields.TimeDelta(missing=2678400)

    health = fields.Nested(HealthCheckConfigSchema)

    swagger = fields.Nested(SwaggerConfigSchema,
                            attribute='SWAGGER')


class ConfigSchema(cfg_loader.ConfigSchema):
    """Configuration schema

    Describes and validates against

    .. list-table::
        :widths: 30 50 20
        :header-rows: 1

        * - Key
          - Comment
          - Default value

        * - ``flask``
          - Required Flask config in :class:`FlaskConfigSchema` format
          - **Required**

        * - ``wsgi``
          - Wsgi configuration in :class:`WSGIConfigSchema` format
          - ``{}``

        * - ``logging``
          - Logging configuration in :class:`LoggingConfigSchema` format
          -

        * - ``gunicorn``
          - Gunicorn configuration in :class:`GunicornConfigSchema` format
          -
    """

    flask = cfg_loader.fields.UnwrapNested(FlaskConfigSchema,
                                           required=True)

    wsgi = fields.Nested(WSGIConfigSchema,
                         missing={})

    logging = fields.Nested(LoggingConfigSchema)

    gunicorn = fields.Nested(GunicornConfigSchema)
