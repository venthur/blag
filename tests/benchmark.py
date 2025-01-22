"""Benchmark the performance of the blag build command."""

import logging
import os
from argparse import Namespace

from pytest import LogCaptureFixture

import blag
from blag.blag import build


def test_performance(args: Namespace, caplog: LogCaptureFixture) -> None:
    """Test performance of the build command."""
    caplog.set_level(logging.ERROR)

    FILES = 10000
    print(f"Generating {FILES} markdown files")
    # create random markdown files in the content directory
    with open(os.path.join(blag.__path__[0], "content", "testpage.md")) as fh:
        markdown = fh.read()
    for i in range(FILES):
        with open(f"content/{i}.md", "w") as f:
            f.write(markdown)
            f.write(str(i))

    from time import time

    t = time()
    build(args)
    t_first = time() - t

    t = time()
    build(args)
    t_second = time() - t
    print(f"First run: {t_first:.2f}s, second run: {t_second:.2f}s")
    print(f"Speedup: {t_first/t_second:.2f}")
