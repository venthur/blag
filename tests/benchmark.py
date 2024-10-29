import os

import blag
from blag.blag import build


def test_performance(args) -> None:
    # create 1000 random markdown files in the content directory
    with open(os.path.join(blag.__path__[0], "content", "testpage.md")) as fh:
              markdown = fh.read()
    for i in range(10000):
        with open(f"content/{i}.md", "w") as f:
            f.write(markdown)
            f.write(str(i))

    from time import time

    t = time()
    build(args)
    print(time() - t)

    import cProfile

    t = time()
    #cProfile.run("build(args)")
    build(args)
    print(time() - t)


    1 / 0
