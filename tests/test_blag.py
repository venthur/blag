from tempfile import TemporaryDirectory
import os
from datetime import datetime

import pytest

from blag import blag


@pytest.fixture
def outdir():
    with TemporaryDirectory() as dir:
        yield dir


def test_generate_feed(outdir):
    articles = []
    blag.generate_feed(articles, outdir, ' ', ' ', ' ', ' ')
    assert os.path.exists(f'{outdir}/atom.xml')


def test_feed(outdir):
    articles = [
        [
            'dest1.html',
            {
                'title': 'title1',
                'date': datetime(2019, 6, 6),
                'content': 'content1',
            }
        ],
        [
            'dest2.html',
            {
                'title': 'title2',
                'date': datetime(1980, 5, 9),
                'content': 'content2',
            }
        ],

    ]

    blag.generate_feed(articles, outdir, 'https://example.com/', 'blog title',
                       'blog description', 'blog author')
    with open(f'{outdir}/atom.xml') as fh:
        feed = fh.read()

    assert '<title>blog title</title>' in feed
    # enable when https://github.com/getpelican/feedgenerator/issues/22
    # is fixed
    # assert '<subtitle>blog description</subtitle>' in feed
    assert '<author><name>blog author</name></author>' in feed

    # article 1
    assert '<title>title1</title>' in feed
    assert '<summary type="html">title1' in feed
    assert '<published>2019-06-06' in feed
    assert '<content type="html">content1' in feed
    assert '<link href="https://example.com/dest1.html"' in feed

    # article 2
    assert '<title>title2</title>' in feed
    assert '<summary type="html">title2' in feed
    assert '<published>1980-05-09' in feed
    assert '<content type="html">content2' in feed
    assert '<link href="https://example.com/dest2.html"' in feed


def test_generate_feed_with_description(outdir):
    # if a description is provided, it will be used as the summary in
    # the feed, otherwise we simply use the title of the article
    articles = [[
        'dest.html',
        {
            'title': 'title',
            'description': 'description',
            'date': datetime(2019, 6, 6),
            'content': 'content',
        }
    ]]
    blag.generate_feed(articles, outdir, ' ', ' ', ' ', ' ')

    with open(f'{outdir}/atom.xml') as fh:
        feed = fh.read()

    assert '<title>title</title>' in feed
    assert '<summary type="html">description' in feed
    assert '<published>2019-06-06' in feed
    assert '<content type="html">content' in feed


def test_parse_args_build():
    # test default args
    args = blag.parse_args(['build'])
    assert args.input_dir == 'content'
    assert args.output_dir == 'build'
    assert args.template_dir == 'templates'
    assert args.static_dir == 'static'

    # input dir
    args = blag.parse_args(['build', '-i', 'foo'])
    assert args.input_dir == 'foo'
    args = blag.parse_args(['build', '--input-dir', 'foo'])
    assert args.input_dir == 'foo'

    # output dir
    args = blag.parse_args(['build', '-o', 'foo'])
    assert args.output_dir == 'foo'
    args = blag.parse_args(['build', '--output-dir', 'foo'])
    assert args.output_dir == 'foo'

    # template dir
    args = blag.parse_args(['build', '-t', 'foo'])
    assert args.template_dir == 'foo'
    args = blag.parse_args(['build', '--template-dir', 'foo'])
    assert args.template_dir == 'foo'

    # static dir
    args = blag.parse_args(['build', '-s', 'foo'])
    assert args.static_dir == 'foo'
    args = blag.parse_args(['build', '--static-dir', 'foo'])
    assert args.static_dir == 'foo'


def test_get_config():
    config = """
[main]
base_url = https://example.com/
title = title
description = description
author = a. u. thor
    """
    # happy path
    with TemporaryDirectory() as dir:
        configfile = f'{dir}/config.ini'
        with open(configfile, 'w') as fh:
            fh.write(config)

        config_parsed = blag.get_config(configfile)
        assert config_parsed['base_url'] == 'https://example.com/'
        assert config_parsed['title'] == 'title'
        assert config_parsed['description'] == 'description'
        assert config_parsed['author'] == 'a. u. thor'

    # a missing required config causes a sys.exit
    for x in 'base_url', 'title', 'description', 'author':
        config2 = '\n'.join([line
                             for line
                             in config.splitlines()
                             if not line.startswith(x)])
        with TemporaryDirectory() as dir:
            configfile = f'{dir}/config.ini'
            with open(configfile, 'w') as fh:
                fh.write(config2)
            with pytest.raises(SystemExit):
                config_parsed = blag.get_config(configfile)

    # base_url gets / appended if it is missing
    config = """
[main]
base_url = https://example.com
title = title
description = description
author = a. u. thor
    """
    with TemporaryDirectory() as dir:
        configfile = f'{dir}/config.ini'
        with open(configfile, 'w') as fh:
            fh.write(config)

        config_parsed = blag.get_config(configfile)
        assert config_parsed['base_url'] == 'https://example.com/'


def test_environment_factory():
    globals_ = {
        'foo': 'bar',
        'test': 'me'
    }
    env = blag.environment_factory(globals_=globals_)
    assert env.globals['foo'] == 'bar'
    assert env.globals['test'] == 'me'
