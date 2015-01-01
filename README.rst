albumleaf
=========

Albumleaf is a minimal web-based photo gallery. To use it, you need your own webserver, which isn't very accommodating. But it fulfills my requirements for sharing photos with family:

- Simplicity
- Sharing via a link (no signing up)
- Batch album downloads
- Self-hosting, which is the best bet for getting around the GFW

A few other features that some people may consider bugs:

- Uploading via ``scp -r``
- A little script to generate thumbnails and batch archives
- Vendorized dependencies
- Malleable page layout (it's just Bootstrap and jQuery+FancyBox)
- Filesystem as database

Installation
------------

Make sure you've got ``libjpeg`` first. On ``apt``, it's

::

    $ sudo apt-get install libjpeg-dev

and on OS X with Homebrew, it's

::

    $ brew install libjpeg


Then just ``pip`` it, ideally in a ``virtualenv``:

::

    $ pip install -r requirements.txt

Deployment
----------

::

    $ python webserver.py

Check ``--help`` for a few command-line switches. It's a Flask app so the default port is 5000, and running in debug mode will enable auto-reloading and tracebacks.

Go ahead and setup your reverse-proxying situation of choice. Static assets (resources and photos) are in ``static/`` which Flask will reluctanctly serve.

Publishing
----------

To upload photos, dump them in a directory under ``static/``, e.g. ``static/2015_Cancun_trip/``. Then

::

    $ python prepare_album.py static/2015_Cancun_trip/

will hook you up. Those underscores will be presented as spaces, by the way.

Obviously, there is no backup/fault tolerance of any sort. Don't be foolish.

TODO
----

The album index page could use some work. Or maybe it's good enough.
