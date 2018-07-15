"""
    consensys_utils.flask.extensions.health
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Declares health check extension

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import healthcheck


class HealthCheck(healthcheck.HealthCheck):
    """Healthcheck extension"""

    def init_app(self, app):
        super().init_app(app, app.config['health']['ENDPOINT_URL'])


# Default health extension
health = HealthCheck()
