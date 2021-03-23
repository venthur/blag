Manual
======

Quickstart
----------

Install blag from PyPI_

.. code-block:: sh

    $ pip install blag

.. _pypi: https://pypi.org/project/blag/

Run blag's quickstart command to create the configuration needed

.. code-block:: sh

    $ blag quickstart

Create some content

.. code-block:: sh

    $ mkdir content
    $ edit content/hello-world.md

Generate the website

.. code-block:: sh

    $ blag build

By default, blag will search for content in ``content`` and the output will be
generated in ``build``. All markdown files in ``content`` will be converted to
html, all other files (i.e. static files) will be copied over).

If you want more separation between the static files and the markdown content,
you can put all static files into the ``static`` directory. Blag will copy
them over to the ``build`` directory.

If you want to customize the looks of the generated site, create a
``template`` directory and put your jinja2 templates here.

Those directories can be changed via command line arguments. See

.. code-block:: sh

    $ blag --help


Manual
------

some text


Templating
----------

Metadata
---------

blag supports metadata elements in the markdown files. They must come before
the content and should be separated from the content with a blank line:

.. code-block:: markdown

    title: foo
    date: 2020-02-02
    tags: this, is, a, test
    description: some subtitle

    this is my content.
    [...]

blag supports *arbitrary* metadata in your documents, and you can use them
freely in you templates. However, some metadata elements are treated special:

``date``
    If a document contains the ``date`` element, it is treated as an
    **article**, otherwise as a **page**. Additionally, ``date`` elements are
    expected to be in ISO format (e.g. ``1980-05-05 21:58``). They are
    automatically converted into ``datetime`` objects with the local timezone
    attached.

``tags``
    Tags are interpreted as a comma separated list. All elements are stripped
    and converted to lower-case: ``tags: foo, Foo Bar, BAZ`` becomes: ``[foo,
    foo bar, baz]``.

    Tags in **articles** are also used to generate the tag-pages, that
    aggregate all articles per tag.

``title`` and ``description``
    The title and description are used in the html header and in the atom
    feed.
