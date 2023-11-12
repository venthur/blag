"""Development Server.

This module provides functionality for blag's development server. It
automatically detects changes in certain directories and rebuilds the
site if necessary.

"""

# remove when we don't support py38 anymore
from __future__ import annotations

import argparse
import logging
import multiprocessing
import os
import time
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import NoReturn

from blag import blag

logger = logging.getLogger(__name__)


def get_last_modified(dirs: list[str]) -> float:
    """Get the last modified time.

    This method recursively goes through `dirs` and returns the most
    recent modification time time found.

    Parameters
    ----------
    dirs
        list of directories to search

    Returns
    -------
    float
        most recent modification time found in `dirs`

    """
    last_mtime = 0.0

    for dir in dirs:
        for root, dirs, files in os.walk(dir):
            for f in files:
                mtime = os.stat(os.path.join(root, f)).st_mtime
                if mtime > last_mtime:
                    last_mtime = mtime

    return last_mtime


def autoreload(args: argparse.Namespace) -> NoReturn:
    """Start the autoreloader.

    This method monitors the given directories for changes (i.e. the
    last modified time). If the last modified time has changed, a
    rebuild is triggered.

    A rebuild is also performed immediately when this method is called
    to avoid serving stale contents.

    Parameters
    ----------
    args
        contains the input-, template- and static dir

    """
    dirs = [args.input_dir, args.template_dir, args.static_dir]
    logger.info(f"Monitoring {dirs} for changes...")
    # make sure we trigger the rebuild immediately when we enter the
    # loop to avoid serving stale contents
    last_mtime = 0.0
    while True:
        mtime = get_last_modified(dirs)
        if mtime > last_mtime:
            last_mtime = mtime
            logger.info("Change detected, rebuilding...")
            blag.build(args)
        time.sleep(1)


def serve(args: argparse.Namespace) -> None:
    """Start the webserver and the autoreloader.

    Parameters
    ----------
    args
        contains the input-, template- and static dir

    """
    httpd = HTTPServer(
        ("", 8000),
        partial(SimpleHTTPRequestHandler, directory=args.output_dir),
    )
    proc = multiprocessing.Process(target=autoreload, args=(args,))
    proc.start()
    logger.info("\n\n  Devserver Started -- visit http://localhost:8000\n")
    httpd.serve_forever()
