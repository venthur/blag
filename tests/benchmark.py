import os

import blag
from blag.blag import build


def test_performance(args) -> None:
    FILES = 1000
    print(f"Generating {FILES} files")
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
    print(t_first)

    t = time()
    build(args)
    t_second = time() - t
    print(t_second)
    print(f"First run: {t_first:.2f}s, second run: {t_second:.2f}s")
    print(f"Speedup: {t_first/t_second:.2f}")

