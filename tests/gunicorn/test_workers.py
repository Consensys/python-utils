"""
    tests.gunicorn.test_workers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test Gunicorn Configuration schema

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import errno
import unittest.mock as mock

import pytest
from gunicorn.config import Config

from consensys_utils.gunicorn.workers import SyncIteratingWorker, PauseIteration


class IteratorTest:
    MAX_ITERATION = 10

    def __init__(self):
        self.meter = 0
        self.mock_next = mock.Mock()

    def __iter__(self):
        return self

    def __next__(self):
        if self.meter >= self.MAX_ITERATION:
            raise StopIteration
        self.mock_next(self.meter)
        if self.meter % 2 == 1:
            # Indicating the running loop to pause iteration for 2 secs
            self.meter += 1
            raise PauseIteration(2)
        self.meter += 1


@pytest.fixture(scope='function')
def iterator():
    yield IteratorTest()


@pytest.fixture(scope='function')
def worker(iterator):
    # Mock socket listener
    mock_listener = mock.Mock()
    sockets = [mock_listener]

    # Declare worker
    mock_log = mock.Mock()
    worker = SyncIteratingWorker(None, None, sockets, None, None, Config(), mock_log)
    worker.wsgi = iterator
    worker.alive = True

    yield worker


@mock.patch('consensys_utils.gunicorn.workers.SyncIteratingWorker.notify')
@mock.patch('consensys_utils.gunicorn.workers.SyncIteratingWorker.accept')
@mock.patch('consensys_utils.gunicorn.workers.SyncIteratingWorker.is_parent_alive')
@mock.patch('consensys_utils.gunicorn.workers.SyncIteratingWorker.wait')
def test_sync_iterating_worker(wait, is_parent_alive, accept, notify, worker):
    # Define a iterator for test purpose

    # Mock SyncIteratingWorker.accept to simulate an IO Error when accepting a connexion
    error = OSError()
    error.errno = errno.EAGAIN
    accept.side_effect = [True] + IteratorTest.MAX_ITERATION * [error]

    # Mock SyncIteratingWorker.is_parent_alive to simulate a parent alive at all time
    is_parent_alive.return_value = True

    with pytest.raises(StopIteration):
        worker.run()

    # Ensure iterator has been called the expected number of times
    assert len(worker.wsgi.mock_next.call_args_list) == 10
    for i in range(10):
        worker.wsgi.mock_next.assert_any_call(i)

    assert len(wait.call_args_list) == 5
    assert len(is_parent_alive.call_args_list) == 5
    assert len(notify.call_args_list) == 12


@mock.patch('consensys_utils.gunicorn.workers.SyncIteratingWorker.notify')
@mock.patch('consensys_utils.gunicorn.workers.SyncIteratingWorker.accept')
@mock.patch('consensys_utils.gunicorn.workers.SyncIteratingWorker.is_parent_alive')
@mock.patch('consensys_utils.gunicorn.workers.SyncIteratingWorker.wait')
def test_sync_iterating_worker_parent_dead(wait, is_parent_alive, accept, notify, worker):
    # Define a iterator for test purpose

    # Mock SyncIteratingWorker.accept to simulate an IO Error when accepting a connexion
    error = OSError()
    error.errno = errno.EAGAIN
    accept.side_effect = error

    # Mock SyncIteratingWorker.is_parent_alive to simulate a dead parent
    is_parent_alive.return_value = False

    assert worker.run() is None

    # Ensure iterator has been called the expected number of times
    assert len(worker.wsgi.mock_next.call_args_list) == 2
    worker.wsgi.mock_next.assert_any_call(0)
    worker.wsgi.mock_next.assert_any_call(1)

    assert len(wait.call_args_list) == 0
    assert len(is_parent_alive.call_args_list) == 1
    assert len(notify.call_args_list) == 2


@mock.patch('consensys_utils.gunicorn.workers.SyncIteratingWorker.notify')
@mock.patch('consensys_utils.gunicorn.workers.SyncIteratingWorker.accept')
@mock.patch('consensys_utils.gunicorn.workers.SyncIteratingWorker.is_parent_alive')
@mock.patch('consensys_utils.gunicorn.workers.SyncIteratingWorker.wait')
def test_sync_iterating_worker_iteration_raise(wait, is_parent_alive, accept, notify, worker):
    # Define a iterator for test purpose

    # Mock SyncIteratingWorker.accept to simulate an IO Error when accepting a connexion
    error = OSError()
    error.errno = errno.EAGAIN
    accept.side_effect = error

    # Mock SyncIteratingWorker.is_parent_alive to simulate a parent alive at all time
    is_parent_alive.return_value = True

    next_error = Exception()
    worker.wsgi.mock_next.side_effect = next_error
    with pytest.raises(Exception) as e:
        worker.run()
    assert e.value == next_error

    # Ensure iterator has been called the expected number of times
    assert len(worker.wsgi.mock_next.call_args_list) == 1
    assert len(wait.call_args_list) == 0
    assert len(notify.call_args_list) == 1
