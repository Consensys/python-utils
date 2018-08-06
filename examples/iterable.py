"""
    examples.iterable
    ~~~~~~~~~~~~~~~~~

    Implement an example of properly managing an iterator using Flask-Iterable and Gunicorn

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import logging
import os

from cfg_loader.utils import parse_yaml_file
from flask import current_app, jsonify
from gunicorn.app.base import BaseApplication

from consensys_utils.flask import Flask
from consensys_utils.flask.extensions.iterable import FlaskIterable
from consensys_utils.gunicorn.workers import PauseIteration

logger = logging.getLogger('examples.iterable')
LOGGING_FILE = os.path.join(os.path.dirname(__file__), 'logging.yml')


# Declare an iterator that we want to properly managed using Gunicorn
class Iterator:
    def __init__(self):
        self.meter = 0

    def set_config(self, config):
        self.meter = config['meter']

    def __iter__(self):
        return self

    def __next__(self):
        logger.info('Iterator.__next__ meter=%s' % self.meter)
        self.meter += 1
        if self.meter % 2 == 0:
            # Indicating the running loop to pause iteration for 2 secs
            raise PauseIteration(2)

        if self.meter >= 100:
            raise StopIteration()


# We declare a Flask application and extend it to make it iterable
iterable_app = Flask(__name__)
iterable_app.config['meter'] = 10
FlaskIterable(Iterator, iterable_app)


# We declare routes on Flask application to interact with the iterator
@iterable_app.route('/get')
def get():
    """Get current value of the iterator meter"""
    logger.info('app.get meter=%s' % current_app.iterator.meter)
    return jsonify({'data': current_app.iterator.meter})


@iterable_app.route('/set/<int:meter>')
def set(meter=0):
    """Set current value of the iterator meter"""
    current_app.iterator.meter = rv = meter
    logger.info('app.set meter=%s' % current_app.iterator.meter)
    return jsonify({'data': rv})


# We declare a custom Gunicorn application for the only matter of the example
class Application(BaseApplication):
    def load(self):
        return iterable_app

    def load_config(self):
        self.cfg.set('logconfig_dict', parse_yaml_file(LOGGING_FILE))
        # We use specific ConsenSys-Utils worker class
        self.cfg.set('worker_class', 'consensys_utils.gunicorn.workers.SyncIteratingWorker')


if __name__ == "__main__":
    # Run iterator
    app = Application()
    app.run()
