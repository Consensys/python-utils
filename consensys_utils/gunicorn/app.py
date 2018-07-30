"""
    consensys_utils.gunicorn.app
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements a Gunicorn App supporting ConsenSys-Utils features

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from gunicorn.app import base

from .config import Config


class WSGIApplication(base.Application):
    """An enhanced gunicorn WSGIApplication including ConsenSys-Utils features


    """

    def __init__(self, loader, *args, **kwargs):
        self.loader = loader
        super().__init__(*args, **kwargs)

    def load_default_config(self):
        # init configuration
        self.cfg = Config(self.usage, prog=self.prog)

    def load_config(self):
        # Load application config and update current config
        cfg = self.loader.load_config()

        if 'gunicorn' in cfg:  # pragma: no branch
            for k, v in cfg['gunicorn'].items():
                self.cfg.set(k.lower(), v)

        if 'logging' in cfg:  # pragma: no branch
            self.cfg.set('logging', cfg['logging'])

        if 'wsgi' in cfg:  # pragma: no branch
            self.cfg.set('wsgi', cfg['wsgi'])

        if hasattr(self.cfg, 'config') and self.cfg.config:  # pragma: no branch
            self.load_config_from_file(self.cfg.config)

        self.chdir()

    def load(self):
        return self.loader()
