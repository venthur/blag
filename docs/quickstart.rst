Quickstart
==========

Install blag from PyPI_::

    $ pip install blag

.. _pypi: https://pypi.org/project/blag/

Run blag's quickstart command to create the configuration needed::

    $ blag quickstart

Create some content::

    $ mkdir content
    $ edit content/hello-world.md

Generate the website::

    $ blag build

By default, blag will search for content in ``content`` and the output will be
generated in ``build``. Those directories can be changed via command line
arguments. See::

    $ blag --help


