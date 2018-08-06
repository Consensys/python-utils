Changelog
=========

Here you can see the full list of changes between each releases of ConsenSys-Utils.

Version 0.2.0b1
---------------

Released on August 6th 2018

Feat

- Config: schema for web3 provider
- Web3: implement create_provider function
- Flask: implement Web3 extension
- Flask: implement Flask-Iterable extension
- Gunicorn: implement SyncIteratingWorker

Chore

- Examples: implement an example for an iterating worker

Version 0.1.0
-------------

Released on July 30th 2018

Fix

- Flask: Enhance consensys_utils.flask.cli.FlaskGroup
- Flask: Improve Factory pattern

Version 0.1.0b4
---------------

Released on July 27th 2018

Refactor

- Config: update default values of Gunicorn configuration schema

Version 0.1.0b3
---------------

Released on July 27th 2018

Fix

- Gunicorn: fix gunicorn application to use ``consensys_utils.gunicorn.config.Config``

Tests

- Gunicorn: add tests for ``gunicorn.config.schema.GunicornConfigSchema``

Version 0.1.0b2
---------------

Released on July 26th 2018

Fix

- Flask: update FlaskFactory

Version 0.1.0b1
---------------

Released July 26th 2018

Features

- Config: implement config package
- Flask: implement WSGI middlewares helpers
- Flask: implement application hooks helpers
- Flask: implement config features to integrate with `cfg-loader`_
- Flask: implement flask extensions helpers
- Flask: implement default extension for healthcheck
- Flask: implement default extension for Swagger
- Flask: implement logging features
- Flask: implement blueprints helpers
- Gunicorn: implement custom Gunicorn application
- Flask: implement CLI resources in particular FlaskGroup that allows to smoothly integrates with Gunicorn
- Config: Implement Gunicorn config schema

.. _cfg-loader: https://github.com/nmvalera/cfg-loader

Version 0.0.0
-------------

Unreleased

Chore

- Project: Initialize project