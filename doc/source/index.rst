================
Broker |release|
================

Function dispatch in Python based on MIME Accept-* headers.

Initialize a broker with some dispatched-to functions matched against MIME
types:

    >>> b = Broker()
    >>> html_handler = b.add("text/html", lambda x: (1, x))
    >>> xml_handler = b.add("application/xml", lambda x: (2, x))
    >>> json_handler = b.add("application/json", lambda x: (3, x))

Select a backend function based on an Accept header:

    >>> b.select("text/html") is html_handler
    True
    >>> b.select("text/html,application/json") is html_handler
    True
    >>> b.select("text/html;q=0.1,application/json") is json_handler
    True

Call the backend function directly:

    >>> b("text/html", 'hello')
    (1, 'hello')
    >>> b("text/html,application/json", 'world')
    (2, 'world')
    >>> b("text/html;q=0.1,application/json", 'json_stuff')
    (3, 'json_stuff')

For a better understanding of what's possible, consult the API documentation
for the :mod:`broker` module.


Installation
============

The usual::

    pip install broker


Thanks
======

Underneath the hood, Broker uses `webob.acceptparse`_ to parse Accept headers
and match against your registered functions. It's this module that does the
heavy lifting; Broker is just a thin layer on top of that.

.. _webob.acceptparse: http://pythonpaste.org/webob/reference.html#accept-headers


(Un)license
===========

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
