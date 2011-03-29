from webob import acceptparse


class Broker(object):

    """
    Function dispatch based on MIME Accept-* headers.

    Initialize a broker with some dispatched-to functions matched against MIME
    types:

        >>> b = Broker()
        >>> html_handler = b.add("text/html", lambda x: (1, x))
        >>> xml_handler = b.add("application/xml", lambda x: (2, x))
        >>> json_handler = b.add("application/json", lambda x: (3, x))

    Select a backend function based on an Accept header:

        >>> b.select("text/html") is html_handler
        True
        >>> b.select("text/html,application/json;q=0.1") is html_handler
        True
        >>> b.select("text/html;q=0.1,application/json") is json_handler
        True

    Call the backend functions directly:

        >>> b("text/html", 'hello')
        (1, 'hello')
        >>> b("text/html,application/json;q=0.1", 'world')
        (1, 'world')
        >>> b("text/html;q=0.1,application/json", 'json_stuff')
        (3, 'json_stuff')
    """

    def __init__(self):
        self.register = {}

    def add(self, mimetype, function, quality=1):
        """Register a function against a MIME type on this broker."""

        self.register[mimetype] = (function, quality)
        return function

    def select(self, accept_header):

        """
        Get the best function for a given Accept header.

        Raise :exc:`NotAcceptable` if no acceptable function is found.
        """

        server_types = [(mimetype, func_qual[1])
                for mimetype, func_qual in self.register.items()]
        accept = acceptparse.MIMEAccept("Accept", accept_header)
        match = accept.best_match(server_types)
        if match is None:
            raise NotAcceptable
        return self.register[match][0]

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
