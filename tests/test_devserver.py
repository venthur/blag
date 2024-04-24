"""Tests for the devserver module."""


# remove when we don't support py38 anymore
from __future__ import annotations

import threading
import time
from argparse import Namespace

from blag import devserver

WAITTIME = 0.1


def test_get_last_modified(cleandir: str) -> None:
    """Test get_last_modified."""
    # take initial time
    t1 = devserver.get_last_modified(["content"])

    # wait a bit, create a file and measure again
    time.sleep(WAITTIME)
    with open("content/test", "w") as fh:
        fh.write("boo")
    t2 = devserver.get_last_modified(["content"])

    # wait a bit and take time again
    time.sleep(WAITTIME)
    t3 = devserver.get_last_modified(["content"])

    assert t2 > t1
    assert t2 == t3


def test_autoreload_builds_immediately(args: Namespace) -> None:
    """Test autoreload builds immediately."""
    # create a dummy file that can be build
    with open("content/test.md", "w") as fh:
        fh.write("boo")

    t = threading.Thread(
        target=devserver.autoreload,
        args=(args, WAITTIME),
        daemon=True,
    )
    t0 = devserver.get_last_modified(["build"])
    t.start()
    # try for 5 seconds...
    for i in range(5):
        time.sleep(WAITTIME)
        t1 = devserver.get_last_modified(["build"])
        print(t1)
        if t1 > t0:
            break
    assert t1 > t0


def test_autoreload(args: Namespace) -> None:
    """Test autoreload."""
    t = threading.Thread(
        target=devserver.autoreload,
        args=(args, WAITTIME),
        daemon=True,
    )
    t.start()

    t0 = devserver.get_last_modified(["build"])

    # create a dummy file that can be build
    with open("content/test.md", "w") as fh:
        fh.write("boo")

    # try for 5 seconds to see if we rebuild once...
    for i in range(5):
        time.sleep(WAITTIME)
        t1 = devserver.get_last_modified(["build"])
        if t1 > t0:
            break
    assert t1 > t0


def test_autoreload_does_not_crash(args: Namespace) -> None:
    """Test autoreload does not crash if build fails."""
    t = threading.Thread(
        target=devserver.autoreload,
        args=(args, WAITTIME),
        daemon=True,
    )
    t.start()

    t0 = devserver.get_last_modified(["build"])

    # create a file that causes build to crash
    with open("content/test.md", "w") as fh:
        fh.write("date: ")

    # try for 5 seconds to see if we rebuild once...
    for i in range(5):
        time.sleep(WAITTIME)
        t1 = devserver.get_last_modified(["build"])
        if t1 > t0:
            break
    assert t.is_alive()
