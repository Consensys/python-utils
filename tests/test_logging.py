"""
    tests.test_logging
    ~~~~~~~~~~~~~~~~~~

    Test logging features

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import logging

import pytest

from consensys_utils.logging import create_logger

config = {
    'version': 1,
    'formatters': {
        'line': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-15s %(levelname)-8s %(message)s <ID=%(id)s>',
        },
    },
    'filters': {
        'id': {
            '()': 'consensys_utils.logging.IDFilter',
        }
    },
    'handlers': {
        'test': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['id'],
            'formatter': 'line',
        }
    },
    'loggers': {
        'test': {
            'level': 'DEBUG',
            'handlers': ['test'],
        }
    }
}


def test_create_logger():
    create_logger(config)


@pytest.fixture(scope='function')
def logger():
    create_logger(config)
    yield logging.getLogger('test')


def test_id_filter(caplog, logger):
    with caplog.at_level(logging.DEBUG, logger='test'):
        logger.debug('Test Message')
        logger.debug('Test Message', extra={'id': 'test-id'})
    assert caplog.records[0].id == '-'
    assert caplog.records[1].id == 'test-id'
