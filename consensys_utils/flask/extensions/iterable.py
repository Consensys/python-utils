"""
    app.extensions.iterable
    ~~~~~~~~~~~~~~~~~~~~~~~

    Implement an extension to make a Flask app iterable

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""


class FlaskIterable:
    """Flask extension to make an application iterable

    Example:

    .. doctest::

        >>> from flask import Flask
        >>> from consensys_utils.exceptions import PauseIteration

        # Declare an iterator that we want to properly managed using Gunicorn
        >>> class Iterator:
        ...     def __init__(self):
        ...         self.meter = 0
        ...
        ...     def set_config(self, config):
        ...         self.meter = config['meter']
        ...
        ...     def __iter__(self):
        ...         return self
        ...
        ...     def __next__(self):
        ...         print(self.meter)
        ...         self.meter += 1
        ...         if self.meter >= 5:
        ...             raise StopIteration

        # We declare a Flask application and extend it to make it iterable
        >>> app = Flask(__name__)
        >>> app.config['meter'] = 1
        >>> iterable = FlaskIterable(Iterator)
        >>> iterable.init_app(app)

        # We can now iterate on the application
        >>> for _ in app:
        ...     continue
        1
        2
        3
        4

    :param iterator_class: An iterator class (it must implement ``__iter__`` and ``__next__`` methods)
    :type iterator_class: type
    :param app: Optional Flask application or blueprint object to extend
    :type app: flask.Flask
    """

    def __init__(self, iterator, app=None):
        self.iterator = iterator

        if app:  # pragma: no branch
            self.init_app(app)

    def init_app(self, app):
        """Initialize application

        :param app: Flask application or blueprint object to extend
        :type app: flask.Flask
        """

        if isinstance(self.iterator, type):
            app.iterator = self.iterator()
        else:
            app.iterator = self.iterator

        if hasattr(app.iterator, 'set_config'):  # pragma: no branch
            app.iterator.set_config(app.config)

        # Overide application class to make it iterable
        class Iterable(app.__class__):
            def __iter__(self):
                return app.iterator

            def __next__(self):
                return next(app.iterator)

        app.__class__ = Iterable
