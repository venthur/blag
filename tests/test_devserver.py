import time

import pytest

from tempfile import TemporaryDirectory
from blag import devserver


@pytest.fixture
def tempdir():
    with TemporaryDirectory() as dir:
        yield dir


def test_get_last_modified(tempdir):
    # take initial time
    t1 = devserver.get_last_modified([tempdir])

    # wait a bit, create a file and measure again
    time.sleep(0.1)
    with open(f'{tempdir}/test', 'w') as fh:
        fh.write('boo')
    t2 = devserver.get_last_modified([tempdir])

    # wait a bit and take time again
    time.sleep(0.1)
    t3 = devserver.get_last_modified([tempdir])

    assert t2 > t1
    assert t2 == t3
