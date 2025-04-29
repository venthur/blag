"""Test blag."""

import os
from argparse import Namespace
from datetime import datetime
from tempfile import TemporaryDirectory
from typing import Any

import pytest
from jinja2 import Template
from pytest import CaptureFixture, LogCaptureFixture

from blag import __VERSION__, blag


def test_generate_feed(cleandir: str) -> None:
    """Test generate_feed."""
    articles: list[tuple[str, dict[str, Any]]] = []
    blag.generate_feed(articles, "build", " ", " ", " ", " ")
    assert os.path.exists("build/atom.xml")


def test_feed(cleandir: str) -> None:
    """Test feed."""
    articles: list[tuple[str, dict[str, Any]]] = [
        (
            "dest1.html",
            {
                "title": "title1",
                "date": datetime(2019, 6, 6),
                "content": "content1",
            },
        ),
        (
            "dest2.html",
            {
                "title": "title2",
                "date": datetime(1980, 5, 9),
                "content": "content2",
            },
        ),
    ]

    blag.generate_feed(
        articles,
        "build",
        "https://example.com/",
        "blog title",
        "blog description",
        "blog author",
    )
    with open("build/atom.xml") as fh:
        feed = fh.read()

    assert "<title>blog title</title>" in feed
    # enable when https://github.com/getpelican/feedgenerator/issues/22
    # is fixed
    # assert '<subtitle>blog description</subtitle>' in feed
    assert "<author><name>blog author</name></author>" in feed

    # article 1
    assert "<title>title1</title>" in feed
    assert '<summary type="html">title1' in feed
    assert "<published>2019-06-06" in feed
    assert '<content type="html">content1' in feed
    assert '<link href="https://example.com/dest1.html"' in feed

    # article 2
    assert "<title>title2</title>" in feed
    assert '<summary type="html">title2' in feed
    assert "<published>1980-05-09" in feed
    assert '<content type="html">content2' in feed
    assert '<link href="https://example.com/dest2.html"' in feed


def test_generate_feed_with_description(cleandir: str) -> None:
    """Test generate_feed with description."""
    # if a description is provided, it will be used as the summary in
    # the feed, otherwise we simply use the title of the article
    articles: list[tuple[str, dict[str, Any]]] = [
        (
            "dest.html",
            {
                "title": "title",
                "description": "description",
                "date": datetime(2019, 6, 6),
                "content": "content",
            },
        )
    ]
    blag.generate_feed(articles, "build", " ", " ", " ", " ")

    with open("build/atom.xml") as fh:
        feed = fh.read()

    assert "<title>title</title>" in feed
    assert '<summary type="html">description' in feed
    assert "<published>2019-06-06" in feed
    assert '<content type="html">content' in feed


def test_feed_is_unicode(cleandir: str) -> None:
    """Test generate_feed."""
    articles: list[tuple[str, dict[str, Any]]] = []
    blag.generate_feed(articles, "build", " ", " ", " ", " ")
    with open("build/atom.xml") as fh:
        feed = fh.read()
    assert 'encoding="utf-8"' in feed


def test_parse_args_build() -> None:
    """Test parse_args with build."""
    # test default args
    args = blag.parse_args(["build"])
    assert args.input_dir == "content"
    assert args.output_dir == "build"
    assert args.template_dir == "templates"
    assert args.static_dir == "static"

    # input dir
    args = blag.parse_args(["build", "-i", "foo"])
    assert args.input_dir == "foo"
    args = blag.parse_args(["build", "--input-dir", "foo"])
    assert args.input_dir == "foo"

    # output dir
    args = blag.parse_args(["build", "-o", "foo"])
    assert args.output_dir == "foo"
    args = blag.parse_args(["build", "--output-dir", "foo"])
    assert args.output_dir == "foo"

    # template dir
    args = blag.parse_args(["build", "-t", "foo"])
    assert args.template_dir == "foo"
    args = blag.parse_args(["build", "--template-dir", "foo"])
    assert args.template_dir == "foo"

    # static dir
    args = blag.parse_args(["build", "-s", "foo"])
    assert args.static_dir == "foo"
    args = blag.parse_args(["build", "--static-dir", "foo"])
    assert args.static_dir == "foo"


def test_get_config() -> None:
    """Test get_config."""
    config = """
[main]
base_url = https://example.com/
title = title
description = description
author = a. u. thor
    """
    # happy path
    with TemporaryDirectory() as dir:
        configfile = f"{dir}/config.ini"
        with open(configfile, "w") as fh:
            fh.write(config)

        config_parsed = blag.get_config(configfile)
        assert config_parsed["base_url"] == "https://example.com/"
        assert config_parsed["title"] == "title"
        assert config_parsed["description"] == "description"
        assert config_parsed["author"] == "a. u. thor"

    # a missing required config causes a sys.exit
    for x in "base_url", "title", "description", "author":
        config2 = "\n".join(
            [line for line in config.splitlines() if not line.startswith(x)]
        )
        with TemporaryDirectory() as dir:
            configfile = f"{dir}/config.ini"
            with open(configfile, "w") as fh:
                fh.write(config2)
            with pytest.raises(SystemExit):
                config_parsed = blag.get_config(configfile)

    # base_url gets / appended if it is missing
    config = """
[main]
base_url = https://example.com
title = title
description = description
author = a. u. thor
    """
    with TemporaryDirectory() as dir:
        configfile = f"{dir}/config.ini"
        with open(configfile, "w") as fh:
            fh.write(config)

        config_parsed = blag.get_config(configfile)
        assert config_parsed["base_url"] == "https://example.com/"


def test_environment_factory(cleandir: str) -> None:
    """Test environment_factory."""
    globals_: dict[str, object] = {"foo": "bar", "test": "me"}
    env = blag.environment_factory("templates", globals_=globals_)
    assert env.globals["foo"] == "bar"
    assert env.globals["test"] == "me"


def test_process_markdown(
    cleandir: str,
    page_template: Template,
    article_template: Template,
) -> None:
    """Test process_markdown."""
    page1 = """\
title: some page

some text
foo bar
    """

    article1 = """\
title: some article1
date: 2020-01-01

some text
foo bar
    """

    article2 = """\
title: some article2
date: 2021-01-01

some text
foo bar
    """

    convertibles = []
    for i, txt in enumerate((page1, article1, article2)):
        with open(f"content/{str(i)}", "w") as fh:
            fh.write(txt)
        convertibles.append((str(i), str(i)))

    articles, pages = blag.process_markdown(
        convertibles, "content", "build", page_template, article_template
    )

    assert isinstance(articles, list)
    assert len(articles) == 2
    for dst, context in articles:
        assert isinstance(dst, str)
        assert isinstance(context, dict)
        assert "content" in context

    assert isinstance(pages, list)
    assert len(pages) == 1
    for dst, context in pages:
        assert isinstance(dst, str)
        assert isinstance(context, dict)
        assert "content" in context


def test_build(args: Namespace) -> None:
    """Test build."""
    page1 = """\
title: some page

some text
foo bar
    """

    article1 = """\
title: some article1
date: 2020-01-01
tags: foo, bar

some text
foo bar
    """

    article2 = """\
title: some article2
date: 2021-01-01
tags: baz

some text
foo bar
    """

    # write some convertibles
    convertibles = []
    for i, txt in enumerate((page1, article1, article2)):
        with open(f"{args.input_dir}/{str(i)}.md", "w") as fh:
            fh.write(txt)
        convertibles.append((str(i), str(i)))

    # some static files
    with open(f"{args.static_dir}/test", "w") as fh:
        fh.write("hello")

    os.mkdir(f"{args.input_dir}/testdir")
    with open(f"{args.input_dir}/testdir/test", "w") as fh:
        fh.write("hello")

    blag.build(args)

    # test existence of the three converted files
    for i in range(3):
        assert os.path.exists(f"{args.output_dir}/{i}.html")
    # ... static file
    assert os.path.exists(f"{args.output_dir}/test")
    # ... directory
    assert os.path.exists(f"{args.output_dir}/testdir/test")
    # ... feed
    assert os.path.exists(f"{args.output_dir}/atom.xml")
    # ... index
    assert os.path.exists(f"{args.output_dir}/index.html")
    # ... archive
    assert os.path.exists(f"{args.output_dir}/archive.html")
    # ... tags
    assert os.path.exists(f"{args.output_dir}/tags/index.html")
    assert os.path.exists(f"{args.output_dir}/tags/foo.html")
    assert os.path.exists(f"{args.output_dir}/tags/bar.html")


def test_remove_extra_files(args):
    """Test that extra files are removed."""
    # create a file and directory in output dir that have no corresponding
    # source
    file_path = f'{args.output_dir}/a'
    dir_path = f'{args.output_dir}/b'
    fh = open(file_path, 'w')
    fh.close()
    os.mkdir(dir_path)

    blag.build(args)

    assert not os.path.exists(file_path)
    assert not os.path.exists(dir_path)


@pytest.mark.parametrize(
    "template",
    [
        "page.html",
        "article.html",
        "index.html",
        "archive.html",
        "tags.html",
        "tag.html",
    ],
)
def test_missing_template_raises(template: str, args: Namespace) -> None:
    """Test that missing templates raise SystemExit."""
    os.remove(f"templates/{template}")
    with pytest.raises(SystemExit):
        blag.build(args)


def test_main(cleandir: str) -> None:
    """Test main."""
    blag.main(["build"])


def test_cli_version(capsys: CaptureFixture[str]) -> None:
    """Test --version."""
    with pytest.raises(SystemExit) as ex:
        blag.main(["--version"])
    # normal system exit
    assert ex.value.code == 0
    # proper version reported
    out, _ = capsys.readouterr()
    assert __VERSION__ in out


def test_cli_verbose(cleandir: str, caplog: LogCaptureFixture) -> None:
    """Test --verbose."""
    blag.main(["build"])
    assert "DEBUG" not in caplog.text

    blag.main(["--verbose", "build"])
    assert "DEBUG" in caplog.text
