# blag

blag is a blog-aware, static site generator, written in [Python][].

blag is named after [the blag of the webcomic xkcd][blagxkcd].

[python]: https://python.org
[blagxkcd]: https://blog.xkcd.com


## Features

* Write content in [Markdown][]
* Theming support using [Jinja2][] templates
* Generation of Atom feeds for blog content
* Fenced code blocks and syntax highlighting using [Pygments][]
* Integrated devserver

blag runs on Linux, Mac and Windows and requires Python >= 3.8

[markdown]: https://daringfireball.net/projects/markdown/
[jinja2]: https://palletsprojects.com/p/jinja/
[pygments]: https://pygments.org/


## Quickstart

```bash
$ pip install blag                  # 1. install blag
$ blag quickstart                   # 2. create a new site
$ vim content/hello-world.md        # 3. create some content
$ blag build                        # 4. build the website
```
