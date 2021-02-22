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
