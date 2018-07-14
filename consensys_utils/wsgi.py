"""
    consensys_utils.wsgi
    ~~~~~~~~~~~~~~~~~~~~

    Implement WSGI utility resources

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import uuid

__all__ = [
    'RequestIDMiddleware',
]


def generate_request_id():
    return str(uuid.uuid4())


def header_to_environ_key(header):
    return 'HTTP_{0}'.format(header.upper().replace('-', '_'))


class RequestIDMiddleware:
    """Middleware that manages Request ID header

    :param wsgi: WSGI application to apply middleware on
    :type wsgi: WSGI application
    :param request_id_header: Name of the request ID header (e.g. "X-Request-ID")
    :type request_id_header: str
    """

    def __init__(self, wsgi, config):
        self.wsgi = wsgi
        self.request_id_header = config['REQUEST_ID_HEADER']
        self.request_id_environ_key = header_to_environ_key(self.request_id_header)

    def __call__(self, environ, start_response):
        """Make the wrapped application callable ro respect WSGI specification"""

        # Set the Request ID header if not yet set
        request_id = environ.setdefault(self.request_id_environ_key, generate_request_id())

        # Upgrade start_response to include the request id header
        def start_response_with_request_id(status, response_headers, exc_info=None):
            response_headers.append((self.request_id_header, request_id))
            return start_response(status, response_headers, exc_info)

        return self.wsgi(environ, start_response_with_request_id)
