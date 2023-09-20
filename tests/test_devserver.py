"""Tests for the devserver module."""


# remove when we don't support py38 anymore
from __future__ import annotations

import threading
import time
from argparse import Namespace

import pytest

from blag import devserver


def test_get_last_modified(cleandir: str) -> None:
    """Test get_last_modified."""
    # take initial time
    t1 = devserver.get_last_modified(["content"])

    # wait a bit, create a file and measure again
    time.sleep(0.1)
    with open("content/test", "w") as fh:
        fh.write("boo")
    t2 = devserver.get_last_modified(["content"])

    # wait a bit and take time again
    time.sleep(0.1)
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
        args=(args,),
        daemon=True,
    )
    t0 = devserver.get_last_modified(["build"])
    t.start()
    # try for 5 seconds...
    for i in range(5):
        time.sleep(1)
        t1 = devserver.get_last_modified(["build"])
        print(t1)
        if t1 > t0:
            break
    assert t1 > t0


@pytest.mark.filterwarnings(
    "ignore::pytest.PytestUnhandledThreadExceptionWarning"
)
def test_autoreload(args: Namespace) -> None:
    """Test autoreload."""
    t = threading.Thread(
        target=devserver.autoreload,
        args=(args,),
        daemon=True,
    )
    t.start()

    t0 = devserver.get_last_modified(["build"])

    # create a dummy file that can be build
    with open("content/test.md", "w") as fh:
        fh.write("boo")

    # try for 5 seconds to see if we rebuild once...
    for i in range(5):
        time.sleep(1)
        t1 = devserver.get_last_modified(["build"])
        if t1 > t0:
            break
    assert t1 > t0
