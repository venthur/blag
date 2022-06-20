from tempfile import TemporaryDirectory
import os
from datetime import datetime

import pytest

from blag import blag


def test_generate_feed(cleandir):
    articles = []
    blag.generate_feed(articles, 'build', ' ', ' ', ' ', ' ')
    assert os.path.exists('build/atom.xml')


def test_feed(cleandir):
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

    blag.generate_feed(articles, 'build', 'https://example.com/',
                       'blog title', 'blog description', 'blog author')
    with open('build/atom.xml') as fh:
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


def test_generate_feed_with_description(cleandir):
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
    blag.generate_feed(articles, 'build', ' ', ' ', ' ', ' ')

    with open('build/atom.xml') as fh:
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


def test_process_markdown(cleandir, page_template, article_template):
    page1 = """\
title: some page

some text
foo bar
    """

    article1 = """\
title: some article1
date: 2020-01-01

some text
foo bar
    """

    article2 = """\
title: some article2
date: 2021-01-01

some text
foo bar
    """

    convertibles = []
    for i, txt in enumerate((page1, article1, article2)):
        i = str(i)
        with open(f'content/{i}', 'w') as fh:
            fh.write(txt)
        convertibles.append([i, i])

    articles, pages = blag.process_markdown(
            convertibles,
            'content',
            'build',
            page_template,
            article_template
    )

    assert isinstance(articles, list)
    assert len(articles) == 2
    for dst, context in articles:
        assert isinstance(dst, str)
        assert isinstance(context, dict)
        assert 'content' in context

    assert isinstance(pages, list)
    assert len(pages) == 1
    for dst, context in pages:
        assert isinstance(dst, str)
        assert isinstance(context, dict)
        assert 'content' in context


def test_build(args):
    page1 = """\
title: some page

some text
foo bar
    """

    article1 = """\
title: some article1
date: 2020-01-01
tags: foo, bar

some text
foo bar
    """

    article2 = """\
title: some article2
date: 2021-01-01
tags: baz

some text
foo bar
    """

    # write some convertibles
    convertibles = []
    for i, txt in enumerate((page1, article1, article2)):
        i = str(i)
        with open(f'{args.input_dir}/{i}.md', 'w') as fh:
            fh.write(txt)
        convertibles.append([i, i])

    # some static files
    with open(f'{args.static_dir}/test', 'w') as fh:
        fh.write('hello')

    os.mkdir(f'{args.input_dir}/testdir')
    with open(f'{args.input_dir}/testdir/test', 'w') as fh:
        fh.write('hello')

    blag.build(args)


def test_main(cleandir):
    blag.main(['build'])


def test_cli_version(capsys):
    with pytest.raises(SystemExit) as ex:
        blag.main(['--version'])
    # normal system exit
    assert ex.value.code == 0
    # proper version reported
    out, _ = capsys.readouterr()
    assert blag.__VERSION__ in out


def test_cli_verbose(cleandir, caplog):
    blag.main(['build'])
    assert 'DEBUG' not in caplog.text

    blag.main(['--verbose', 'build'])
    assert 'DEBUG' in caplog.text
