"""
    tests.flask.test_blueprints
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test blueprints helpers

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

from unittest.mock import MagicMock

import pytest
from flask import Flask, Blueprint, jsonify

from consensys_utils.flask.blueprints import register_blueprints


@pytest.fixture(scope='function')
def app():
    _app = Flask(__name__)

    yield _app


def test_register_blueprints(client):
    test_blueprint = Blueprint('test', __name__)
    test_blueprint2 = Blueprint('test2', __name__)

    handler_mock = MagicMock()

    @test_blueprint.route('/test')
    def test():
        handler_mock()
        return jsonify({'data': 'test-value'})

    test_blueprints = [
        lambda app: app.register_blueprint(test_blueprint),
        test_blueprint2,
    ]

    register_blueprints(client.application, blueprints=test_blueprints)

    # Test if the blueprint has been correctly registered
    client.get('/test')
    assert len(handler_mock.call_args_list) == 1
