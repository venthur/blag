import time

from blag import devserver


def test_get_last_modified(cleandir):
    # take initial time
    t1 = devserver.get_last_modified(['content'])

    # wait a bit, create a file and measure again
    time.sleep(0.1)
    with open('content/test', 'w') as fh:
        fh.write('boo')
    t2 = devserver.get_last_modified(['content'])

    # wait a bit and take time again
    time.sleep(0.1)
    t3 = devserver.get_last_modified(['content'])

    assert t2 > t1
    assert t2 == t3
