"""
    consensys_utils.gunicorn.workers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements Gunicorn workers

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import errno
import ssl

import gunicorn.http as http
import gunicorn.util as util
from gunicorn.workers.sync import SyncWorker, StopWaiting

from ..exceptions import PauseIteration


class SyncIteratingWorker(SyncWorker):
    """A Gunicorn synchronous worker that allows to run an iterable WSGI application.

    It allows to run a loop process that iterates over a WSGI application object
    while allowing to process HTTP requests.

    Since the worker is synchronous it is thread safe to modify
    the WSGI object either when iterating or when handling an HTTP request.

    **Remark**

    Such a worker should not be considered highly performing as HTTP server but
    for dealing with a few requests to control the iterable WSGI application
    it is well suited.
    """

    def accept(self, listener):  # pragma: no cover
        client, address = listener.accept()
        # :class:`SyncIteratingWorker` uses non blocking connection sockets so we
        # directly fall back on iteration when no data is available on connection
        client.setblocking(False)
        util.close_on_exec(client)
        self.handle(listener, client, address)

    def iterate(self):
        """Iterate on WSGI object"""

        next(self.wsgi)

    def handle(self, listener, client, address):  # noqa: C901, pragma: no cover
        """Handle a request

        Method is almost identical to :meth:`gunicorn.workers.sync.SyncWorker` one.

        We need to overide this  method because we use non blocking socket connections
        thus we are more sensitive to :meth:`errno.EAGAIN` errors.
        """
        req = None
        try:
            if self.cfg.is_ssl:
                client = ssl.wrap_socket(client, server_side=True, **self.cfg.ssl_options)
            parser = http.RequestParser(self.cfg, client)
            req = next(parser)
            self.handle_request(listener, req, client, address)
        except http.errors.NoMoreData as e:
            self.log.debug("Ignored premature client disconnection. %s", e)
        except StopIteration as e:
            self.log.debug("Closing connection. %s", e)
        except ssl.SSLError as e:
            if e.args[0] == ssl.SSL_ERROR_EOF:
                self.log.debug("ssl connection closed")
                client.close()
            else:
                self.log.debug("Error processing SSL request.")
                self.handle_error(req, client, address, e)
        except EnvironmentError as e:
            # Added in ConsenSys-Utils: we do not log exception on :meth:`errno.EAGAIN`
            if e.errno not in (errno.EPIPE, errno.ECONNRESET, errno.EAGAIN):
                self.log.exception("Socket error processing request.")
            else:
                if e.errno == errno.ECONNRESET:
                    self.log.debug("Ignoring connection reset")
                elif e.errno == errno.EAGAIN:
                    self.log.debug("Ignoring EAGAIN")
                else:
                    self.log.debug("Ignoring EPIPE")
        except Exception as e:
            self.handle_error(req, client, address, e)
        finally:
            util.close(client)

    def run(self):  # noqa: C901
        """Run the main worker loop

        At each step of the loop it

        1. Handles entry socket request if available
        2. Iterate on the WSGI iterable object

        If a :meth:`consensys_utils.exceptions.PauseIteration` is caught when iterating
        on the WSGI object then the loop waits by entering a stale state freeing CPU usage.

        Receiving an HTTP request instantaneously gets the loop out of stale state.
        """

        # self.socket appears to lose its blocking status after
        # we fork in the arbiter. Reset it here.
        for s in self.sockets:
            s.setblocking(0)

        listener = self.sockets[0]
        while self.alive:  # pragma: no branch
            self.notify()

            # Accept a connection. If we get an error telling us
            # that no connection is waiting we fall back to iteration
            try:
                self.accept(listener)
                # Keep processing client until no one is waiting
                continue
            except EnvironmentError as e:
                if e.errno not in (errno.EAGAIN, errno.ECONNABORTED, errno.EWOULDBLOCK):  # pragma: no cover
                    raise

            # If no client is waiting we fall back on iteration
            try:
                self.iterate()
                # Keep iterating until an error is raised
                continue
            except PauseIteration as e:
                timeout = e.timeout or self.timeout or 1
            except StopIteration:  # pragma: no cover
                self.log.info("Stop iteration")
                raise
            except Exception:
                self.log.exception("Error during iteration")
                raise

            if not self.is_parent_alive():
                return

            try:
                # We wait until it is time to iterate again or
                # we have received a message through the socket
                self.log.debug("Pausing iteration for %s seconds" % timeout)
                self.wait(timeout)
            except StopWaiting:  # pragma: no cover
                return
