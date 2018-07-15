.. _api_reference:

***
API
***

.. module:: consensys_utils

This part of the documentation covers all the interfaces of ConsenSys-Utils.

Config
======

ConsenSys-Utils configuration resources are based on `cfg-loader`_

.. _cfg-loader: https://github.com/nmvalera/cfg-loader

Schema
~~~~~~

ConsenSys-Utils defines various useful configuration schemas that allow to validate against configuration data

Logging
```````

.. py:currentmodule:: consensys_utils.config.schema.logging

.. autoclass:: LoggingConfigSchema
    :members:

Flask
`````

Flask application configuration schemas

.. py:currentmodule:: consensys_utils.config.schema.flask

.. autoclass:: FlaskConfigSchema
    :members:

Base
^^^^

.. autoclass:: BaseConfigSchema
    :members:

Session
^^^^^^^

.. autoclass:: SessionConfigSchema
    :members:

.. autoclass:: CookieConfigSchema
    :members:

Health Check
^^^^^^^^^^^^

.. autoclass:: HealthCheckConfigSchema
    :members:

Swagger
^^^^^^^
.. autoclass:: SwaggerConfigSchema
    :members:

WSGI
````

Flask application configuration schemas

Request ID
^^^^^^^^^^

.. py:currentmodule:: consensys_utils.config.schema.wsgi

.. autoclass:: WSGIConfigSchema
    :members:

.. autoclass:: RequestIDConfigSchema
    :members:

Loader
~~~~~~

.. py:currentmodule:: consensys_utils.config.loader

.. autofunction:: create_yaml_config_loader