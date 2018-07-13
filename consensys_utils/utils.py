"""
    consensys_utils.utils
    ~~~~~~~~~~~~~~~~~~~~~

    Utility functions

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import inspect
from importlib import import_module


def import_optional_module(name):
    """Import a module

    In case the module is missing it raises an error with a message indicating to install

    :param name: Name of the module to import
    :type name: str
    """
    try:
        return import_module(name)
    except ImportError:
        # Get name of the module from which the import_optional_module is called
        module = inspect.getmodule(inspect.stack()[1][0])
        raise ImportError("To use '{}' make sure to have '{}' installed".format(module.__name__, name))
