"""Development Server.

This module provides functionality for blag's development server. It
automatically detects changes in certain directories and rebuilds the
site if necessary.

"""

import os
import logging
import time
import multiprocessing
from http.server import SimpleHTTPRequestHandler, HTTPServer
from functools import partial

from blag import blag


logger = logging.getLogger(__name__)


def get_last_modified(dirs):
    """Get the last modified time.

    This method recursively goes through `dirs` and returns the most
    recent modification time time found.

    Parameters
    ----------
    dirs : list[str]
        list of directories to search

    Returns
    -------
    int
        most recent modification time found in `dirs`

    """
    last_mtime = 0

    for dir in dirs:
        for root, dirs, files in os.walk(dir):
            for f in files:
                mtime = os.stat(os.path.join(root, f)).st_mtime
                if mtime > last_mtime:
                    last_mtime = mtime

    return last_mtime


def autoreload(args):
    """Start the autoreloader.

    This method monitors the given directories for changes (i.e. the
    last modified time). If the last modified time has changed, a
    rebuild is triggered.

    Parameters
    ----------
    args : argparse.Namespace

    """
    dirs = [args.input_dir, args.template_dir, args.static_dir]
    logger.info(f'Monitoring {dirs} for changes...')
    last_mtime = get_last_modified(dirs)
    while True:
        mtime = get_last_modified(dirs)
        if mtime > last_mtime:
            last_mtime = mtime
            logger.debug('Change detected, rebuilding...')
            blag.build(args)
        time.sleep(1)


def serve(args):
    """Start the webserver and the autoreloader.

    Parameters
    ----------
    args : arparse.Namespace

    """
    httpd = HTTPServer(('', 8000), partial(SimpleHTTPRequestHandler,
                       directory=args.output_dir))
    proc = multiprocessing.Process(target=autoreload, args=(args,))
    proc.start()
    httpd.serve_forever()
