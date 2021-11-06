import time
import threading

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


def test_autoreload_builds_immediately(args):
    # create a dummy file that can be build
    with open('content/test.md', 'w') as fh:
        fh.write('boo')

    t = threading.Thread(target=devserver.autoreload,
                         args=(args, ),
                         daemon=True,)
    t0 = devserver.get_last_modified(['build'])
    t.start()
    # try for 5 seconds...
    for i in range(5):
        time.sleep(1)
        t1 = devserver.get_last_modified(['build'])
        print(t1)
        if t1 > t0:
            break
    assert t1 > t0


def test_autoreload(args):
    t = threading.Thread(target=devserver.autoreload,
                         args=(args, ),
                         daemon=True,)
    t.start()

    t0 = devserver.get_last_modified(['build'])

    # create a dummy file that can be build
    with open('content/test.md', 'w') as fh:
        fh.write('boo')

    # try for 5 seconds...
    for i in range(5):
        time.sleep(1)
        t1 = devserver.get_last_modified(['build'])
        print(t1)
        if t1 > t0:
            break
    assert t1 > t0
