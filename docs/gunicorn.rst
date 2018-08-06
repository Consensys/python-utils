Gunicorn
========

ConsenSys-Utils slightly enhances `gunicorn`_ for better compatibility with its features

.. _`gunicorn`: https://github.com/benoitc/gunicorn


Application
~~~~~~~~~~~

.. py:currentmodule:: consensys_utils.gunicorn.app

.. autoclass:: WSGIApplication
    :members:

Config
~~~~~~

.. py:currentmodule:: consensys_utils.gunicorn.config

.. autoclass:: Config
    :members:

Logging
~~~~~~~

.. py:currentmodule:: consensys_utils.gunicorn.logging

.. autoclass:: Logger
    :members:

.. autoclass:: RequestIDLogger
    :members:

Workers
~~~~~~~

.. py:currentmodule:: consensys_utils.gunicorn.workers

.. autoclass:: SyncIteratingWorker
    :members:
