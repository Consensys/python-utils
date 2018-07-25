"""
    consensys_utils.flask.extensions.health
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Declares health check extension

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import healthcheck


class HealthCheck(healthcheck.HealthCheck):
    """Healthcheck extension that declares an health check route

    Healthcheck URL can be set at application initialization by reading app configuration
    """

    def init_app(self, app, path=None):
        path = path or app.config['health']['ENDPOINT_URL']
        super().init_app(app, path)


# Default health extension
health = HealthCheck()
