A playground for web scraping
=============================

This is an experimental playground for web scraping with XQuery.

Dependencies
------------

* Python 3.5
* Python click
* Python Requests
* Beautiful Soup 4
* XQilla 2.3

Overview
--------

The core of this system is a single Python function named `scrape`.
It takes a few keyword arguments, like `get`/`post`, `params` and `data`
to fetch a web resource.  After cleaning the HTML with BeautifulSoup,
it passes it as the context to an XQuery interpreter which loads an XQuery
expression from a file with the same basename as the calling function.

So for each specific scraping task, a Python function is defined which succinctly
specifies how and where to fetch the web resource from.  The actual query
is placed in a separate file.  Typical web scraping task definitions
become very small and are easy to write from scratch.

The file `xq.py` contains a set of example scraping tasks.
If you find this useful, or develop your own web scraping tasks for
popular public services, please let me know.

Todo
----

* Split single Python file into an executable frontend and rulsets in extra
  site/user-specific files.

