"""
    consensys_utils.exceptions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    ConsenSys-Utils exceptions

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""


class PauseIteration(Exception):
    """Error indicating to pause iteration

    Useful when combined with :meth:`consensys_utils.gunicorn.workers.SyncIteratingWorker`

    :param timeout: Maximum time to pause before re-starting iteration
    :type timeout: float
    """

    def __init__(self, timeout=None):
        self.timeout = timeout
