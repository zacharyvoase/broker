from webob import acceptparse


Accept = acceptparse.Accept
MIMEAccept = acceptparse.MIMEAccept


class Broker(object):

    """
    Function dispatch based on MIME Accept-* headers.

    Initialize a broker with some dispatched-to functions matched against MIME
    types::

        >>> b = Broker()
        >>> html_handler = b.add("text/html", lambda x: (1, x))
        >>> xml_handler = b.add("application/xml", lambda x: (2, x))
        >>> json_handler = b.add("application/json", lambda x: (3, x))

    Select a backend function based on an Accept header value::

        >>> b.select("text/html") is html_handler
        True
        >>> b.select("text/html,application/json;q=0.1") is html_handler
        True
        >>> b.select("text/html;q=0.1,application/json") is json_handler
        True

    Call the backend functions directly::

        >>> b("text/html", 'hello')
        (1, 'hello')
        >>> b("text/html,application/json;q=0.1", 'world')
        (1, 'world')
        >>> b("text/html;q=0.1,application/json", 'json_stuff')
        (3, 'json_stuff')

    The constructor also accepts an `accept_cls` keyword argument, which
    defaults to ``webob.acceptparse.MIMEAccept``. If you're matching on
    elements that are *not* MIME types, change this to
    ``webob.acceptparse.Accept`` (aliased, for convenience, as
    ``broker.Accept``).
    """

    def __init__(self, accept_cls=acceptparse.MIMEAccept):
        self.registry = {}
        self.accept_cls = accept_cls

    def add(self, mimetype, function, quality=1):

        """
        Register a function for a MIME type, optionally with a server quality.

        Return the function directly. If `quality` is not provided, defaults to
        1.

            >>> b = Broker()
            >>> _ = b.add('text/html', 'html_func')
            >>> b.registry['text/html']
            ('html_func', 1)
            >>> _ = b.add('application/json', 'json_func', quality=0.5)
            >>> b.registry['application/json']
            ('json_func', 0.5)
        """

        self.registry[mimetype] = (function, quality)
        return function

    def register(self, mimetype, quality=1):
        """
        Build a decorator for registering a function for a MIME type.

            >>> b = Broker()
            >>> @b.register("text/html")
            ... def html_func(x):
            ...     return x + 1
            >>> @b.register("application/json", quality=0.25)
            ... def json_func(x):
            ...     return x + 5
            >>> b.registry['text/html']
            (<function html_func at 0x...>, 1)
            >>> b.registry['application/json']
            (<function json_func at 0x...>, 0.25)
        """

        def decorator(function):
            return self.add(mimetype, function, quality=quality)
        return decorator

    def select(self, accept_header):

        """
        Get the best function for a given Accept header.

        Raise :exc:`NotAcceptable` if no acceptable function is found.

            >>> b = Broker()
            >>> _ = b.add('text/html', 1)
            >>> _ = b.add('application/json', 2)
            >>> b.select('text/html')
            1
            >>> b.select('application/json')
            2
        """

        accept = self.accept_cls(accept_header)
        match = accept.best_match(self.server_types())
        if match is None:
            raise NotAcceptable
        return self.registry[match][0]

    def server_types(self):

        """
        Return a list of `(mimetype, quality)` pairs, sorted by quality.

            >>> b = Broker()
            >>> b.add('application/json', None, quality=0.75)
            >>> b.add('application/xml', None, quality=0.25)
            >>> b.add('text/html', None, quality=1)
            >>> b.server_types()
            [('text/html', 1), ('application/json', 0.75), ('application/xml', 0.25)]
        """

        types = []
        for mimetype, func_qual in self.registry.items():
            types.append((mimetype, func_qual[1]))
        types.sort(key=lambda pair: pair[::-1], reverse=True)
        return types

    def __call__(self, accept_header, *args, **kwargs):

        """
        Select and call the best function for the given Accept header.

        Raise :exc:`NotAcceptable` if no acceptable function is found.
        """

        return self.select(accept_header)(*args, **kwargs)


def _get_tests():
    """Enables ``python setup.py test``."""
    import doctest
    return doctest.DocTestSuite(optionflags=doctest.ELLIPSIS)
