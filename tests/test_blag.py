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
