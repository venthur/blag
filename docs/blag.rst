Manual
======


Quickstart
----------

Install blag from PyPI_

.. code-block:: sh

    $ pip install blag

.. _pypi: https://pypi.org/project/blag/

Run blag's quickstart command to create the configuration, templates and some
initial content.

.. code-block:: sh

    $ blag quickstart

Create some content

.. code-block:: sh

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

If you want to customize the look of the generated site, visit the ``template``
directory. It contains jinja2 templates and can be modified as needed.

Those directories can be changed via command line arguments. See

.. code-block:: sh

    $ blag --help


Manual
------


Pages and Articles
^^^^^^^^^^^^^^^^^^

Internally, blag differentiates between **pages** and **articles**.
Intuitively, pages are simple pages and articles are blog posts. The decision
whether a document is a page or an article is made depending on the presence
of the ``date`` metadata element: Any document that contains the ``date``
metadata element is an article, everything else a page.

This differentiation has consequences:

* blag uses different templates: ``page.html`` and ``article.html``
* only articles are collected in the Atom feed
* only articles are aggregated in the tag pages

blag does **not** enforce a certain directory structure for pages and
articles. You can mix and match them freely or structure them in different
directories. blag will mirror the structure found in the ``content`` directory

::

    content/
        article1.md
        article2.md
        page1.md

results in:

::

    build/
        article1.html
        article2.html
        page1.html

Arbitrary complex structures are possible too:

::

    content/
        posts/
            2020/
                2020-01-01-foo.md
                2020-02-01-foo.md
        pages/
            foo.md
            bar.md

results in:

::

    build/
        posts/
            2020/
                2020-01-01-foo.html
                2020-02-01-foo.html
        pages/
            foo.html
            bar.html


Static Files
^^^^^^^^^^^^

Static files can be put into the ``content`` directory and will be copied over
to the ``build`` directory as well. If you want better separation between
content and static files, you can use the ``static`` directory and put the
files there. All files and directories found in the ``static`` directory will
be copied over to ``build``.

::

    content/
        foo.md
        bar.md
        kitty.jpg

results in:

::

    build/
        foo.html
        bar.html
        kitty.jpg

Alternatively:

::

    content/
        foo.md
        bar.md
    static/
        kitty.jpg

results in:

::

    build/
        foo.html
        bar.html
        kitty.jpg


Internal Links
--------------

In contrast to most other static blog generators, blag will automatically
convert **relative** markdown links. That means you can link you content using
relative markdown links and blag will convert them to html automatically. The
advantage is that your content tree in markdown is consistent and
self-contained even if you don't generate html from it.


.. code-block:: markdown

   [...]
   this is a [link](foo.md) to an internal page foo.

becomes

.. code-block:: html

   <p>this is a <a href="foo.html">link</a> to an internal page foo.</p>


Templating
----------

Templates are stored by default in the ``templates`` directory.

============ ====================================== ===================
Template     Used For                               Variables
============ ====================================== ===================
page.html    pages (i.e. non-articles)              site, content, meta
article.html articles (i.e. blog posts)             site, content, meta
index.html   landing page of the blog               site, archive
archive.html archive page of the blog               site, archive
tags.html    list of tags                           site, tags
tag.html     archive of Articles with a certain tag site, archive, tag
============ ====================================== ===================

If you make use of Jinja2's template inheritance, you can of course have more
template files in the ``templates`` directory.

``site``
    This dictionary contains the site configuration, namely: ``base_url``,
    ``title``, ``description`` and ``author``. Don't confuse the site-title
    and -description with the title and description of individual pages or
    articles.

``content``
    HTML, converted from markdown.

``meta``
    ``meta`` stands for all metadata elements available in the article or
    page. Please be aware that those are not wrapped in a dictionary, but
    **directly** available as variables.

``archive``
    A list of ``[destination path, context]`` tuples, where the context are
    the respective variables that would be provided to the individual page or
    article.

``tags``
    List of tags.

``tag``
    A tag.


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


Devserver
---------

blag provides a devserver which you can use for local web-development. The
devserver provides a simple web server, serving your site in
http://localhost:8000 and will automatically rebuild the project when it
detects modifications in one of the ``content``, ``static`` and ``templates``
directories.

.. code-block:: sh

    $ blag serve

