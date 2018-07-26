Flask
=====

ConsenSys-Utils defines many resources for working with `Flask`_ application.
It is highly recommended you have some basic knowledge of `Flask`_ before using ConsenSys-Utils.

.. _`Flask`: http://flask.pocoo.org/docs/1.0/

Application
~~~~~~~~~~~

ConsenSys-Utils provides useful resources to implement the Flask application factory pattern

.. py:currentmodule:: consensys_utils.flask

.. autoclass:: FlaskFactory
    :members:

.. autoclass:: Flask
    :members:

Extensions
~~~~~~~~~~

ConsenSys-Utils implements functions to facilitate initialization of Flask extensions on an application

.. py:currentmodule:: consensys_utils.flask.extensions

.. autofunction:: initialize_extensions

.. autofunction:: initialize_health_extension

.. autofunction:: initialize_swagger_extension

ConsenSys-Utils defines a bench of `Flask` extensions that can be smoothly re-used.

Healthcheck
```````````

.. py:currentmodule:: consensys_utils.flask.extensions.health

.. autoclass:: HealthCheck
    :members:

Swagger
```````

.. py:currentmodule:: consensys_utils.flask.extensions.swagger

.. autoclass:: Swagger
    :members:

Config
~~~~~~

.. py:currentmodule:: consensys_utils.flask.config

.. autoclass:: Config
    :members:

.. autofunction:: set_app_config

Hooks
~~~~~

ConsenSys-Utils implements functions to facilitate setting Flask hooks on an application

.. py:currentmodule:: consensys_utils.flask.hooks

.. autofunction:: set_hooks

.. autofunction:: set_request_id_hook

Blueprints
~~~~~~~~~~

ConsenSys-Utils implements functions to facilitate registering blueprints on an application

.. py:currentmodule:: consensys_utils.flask.blueprints

.. autofunction:: register_blueprints

Logging
~~~~~~~

ConsenSys-Utils implements resources to facilitate logging blueprints on an application

.. py:currentmodule:: consensys_utils.flask.logging

.. autoclass:: RequestIDFilter
    :members:

.. autofunction:: create_logger
