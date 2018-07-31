Flask
=====

ConsenSys-Utils defines many resources for working with `Flask`_ application.
It is highly recommended you have some basic knowledge of `Flask`_ before using ConsenSys-Utils.

.. _`Flask`: http://flask.pocoo.org/docs/1.0/

Application Factory
~~~~~~~~~~~~~~~~~~~

ConsenSys-Utils provides useful resources to implement the Flask application factory pattern

.. py:currentmodule:: consensys_utils.flask

.. autoclass:: FlaskFactory
    :members:

.. autoclass:: BaseFlaskFactory
    :members:

.. autoclass:: Flask
    :members:

WSGI
~~~~

ConsenSys-Utils implements functions to facilitate Flask app decoration with WSGI middlewares

.. py:currentmodule:: consensys_utils.flask.wsgi

.. autofunction:: apply_middlewares

.. autofunction:: apply_request_id_middleware


Extensions
~~~~~~~~~~

ConsenSys-Utils implements functions to facilitate initialization of Flask extensions on an application

.. py:currentmodule:: consensys_utils.flask.extensions

.. autofunction:: initialize_extensions

.. autofunction:: initialize_health_extension

.. autofunction:: initialize_swagger_extension

.. autofunction:: initialize_web3_extension

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

Web3
````

.. py:currentmodule:: consensys_utils.flask.extensions.web3

.. autoclass:: FlaskWeb3
    :members:

Config
~~~~~~

.. py:currentmodule:: consensys_utils.flask.config

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
