.. _schema:

Schema
~~~~~~

ConsenSys-Utils gathers a bench of useful :class:`~cfg_loader.schema.ConfigSchema` that can be reused in any project.

Logging
```````

Logging schema

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

Schema for WSGI middlewares

Request ID
^^^^^^^^^^

.. py:currentmodule:: consensys_utils.config.schema.wsgi

.. autoclass:: WSGIConfigSchema
    :members:

.. autoclass:: RequestIDConfigSchema
    :members:

Gunicorn
````````

Gunicorn configuration schemas

.. py:currentmodule:: consensys_utils.config.schema.gunicorn

.. autoclass:: GunicornConfigSchema

.. autoclass:: ServerSocketConfigSchema

.. autoclass:: WorkerProcessesConfigSchema

.. autoclass:: LoggingConfigSchema

.. autoclass:: ServerMechanicsConfigSchema

.. autoclass:: ProcessNamingConfigSchema

.. autoclass:: SSLConfigSchema

.. autoclass:: SecurityConfigSchema
