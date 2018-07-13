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

Loader
~~~~~~

.. py:currentmodule:: consensys_utils.config.loader

.. autofunction:: create_yaml_config_loader

Utils
=====

.. py:currentmodule:: consensys_utils.utils

.. autofunction:: import_optional_module