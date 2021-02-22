from tempfile import TemporaryDirectory
import os

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
    with TemporaryDirectory() as dir:
        configfile = f'{dir}/config.ini'
        with open(configfile, 'w') as fh:
            fh.write(config)

        config_parsed = blag.get_config(configfile)
        assert config_parsed['base_url'] == 'https://example.com/'
        assert config_parsed['title'] == 'title'
        assert config_parsed['description'] == 'description'
        assert config_parsed['author'] == 'a. u. thor'

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
