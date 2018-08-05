"""
    app.extensions.iterable
    ~~~~~~~~~~~~~~~~~~~~~~~

    Implement an extension to make a Flask app iterable

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""


class FlaskIterable:
    """Flask extension to make an application iterable

    :param iterator_class: An iterator class (it must implement ``__iter__`` and ``__next__`` methods)
    :type iterator_class: type
    :param app: Optional Flask application or blueprint object to extend
    :type app: flask.Flask
    """

    def __init__(self, iterator_class, app=None):
        self.iterator_class = iterator_class

        if app:  # pragma: no branch
            self.init_app(app)

    def init_app(self, app):
        """Initialize application

        :param app: Flask application or blueprint object to extend
        :type app: flask.Flask
        """

        app.iterator = self.iterator_class()

        if hasattr(app.iterator, 'set_config'):  # pragma: no branch
            app.iterator.set_config(app.config)

        # Overide application class to make it iterable
        class Iterable(app.__class__):
            def __iter__(self):
                return app.iterator

            def __next__(self):
                return next(app.iterator)

        app.__class__ = Iterable
