"""Test markdown module."""

from datetime import datetime
from typing import Any

import markdown
import pytest

from blag.markdown import convert_markdown, markdown_factory


@pytest.mark.parametrize(
    "input_, expected",
    [
        # inline
        ("[test](test.md)", "test.html"),
        ('[test](test.md "test")', "test.html"),
        ("[test](a/test.md)", "a/test.html"),
        ('[test](a/test.md "test")', "a/test.html"),
        ("[test](/test.md)", "/test.html"),
        ('[test](/test.md "test")', "/test.html"),
        ("[test](/a/test.md)", "/a/test.html"),
        ('[test](/a/test.md "test")', "/a/test.html"),
        # reference
        ("[test][]\n[test]: test.md " "", "test.html"),
        ('[test][]\n[test]: test.md "test"', "test.html"),
        ("[test][]\n[test]: a/test.md", "a/test.html"),
        ('[test][]\n[test]: a/test.md "test"', "a/test.html"),
        ("[test][]\n[test]: /test.md", "/test.html"),
        ('[test][]\n[test]: /test.md "test"', "/test.html"),
        ("[test][]\n[test]: /a/test.md", "/a/test.html"),
        ('[test][]\n[test]: /a/test.md "test"', "/a/test.html"),
    ],
)
def test_convert_markdown_links(input_: str, expected: str) -> None:
    """Test convert_markdown."""
    md = markdown_factory()
    html, _ = convert_markdown(md, input_)
    assert expected in html


@pytest.mark.parametrize(
    "input_, expected",
    [
        # scheme
        ("[test](https://)", "https://"),
        # netloc
        ("[test](//test.md)", "//test.md"),
        # no path
        ("[test]()", ""),
    ],
)
def test_dont_convert_normal_links(input_: str, expected: str) -> None:
    """Test convert_markdown doesn't convert normal links."""
    md = markdown_factory()
    html, _ = convert_markdown(md, input_)
    assert expected in html


@pytest.mark.parametrize(
    "input_, expected",
    [
        ("foo: bar", {"foo": "bar"}),
        ("foo: those are several words", {"foo": "those are several words"}),
        ("tags: this, is, a, test\n", {"tags": ["this", "is", "a", "test"]}),
        ("tags: this, IS, a, test", {"tags": ["this", "is", "a", "test"]}),
        (
            "date: 2020-01-01 12:10",
            {"date": datetime(2020, 1, 1, 12, 10).astimezone()},
        ),
    ],
)
def test_convert_metadata(input_: str, expected: dict[str, Any]) -> None:
    """Test convert_markdown converts metadata correctly."""
    md = markdown_factory()
    _, meta = convert_markdown(md, input_)
    assert expected == meta


def test_markdown_factory() -> None:
    """Test markdown_factory."""
    md = markdown_factory()
    assert isinstance(md, markdown.Markdown)


def test_smarty() -> None:
    """Test smarty."""
    md = markdown_factory()

    md1 = """

this --- is -- a test ...

    """
    html, meta = convert_markdown(md, md1)
    assert "mdash" in html
    assert "ndash" in html
    assert "hellip" in html


def test_smarty_code() -> None:
    """Test smarty doesn't touch code."""
    md = markdown_factory()

    md1 = """
```
this --- is -- a test ...
```
    """
    html, meta = convert_markdown(md, md1)
    assert "mdash" not in html
    assert "ndash" not in html
    assert "hellip" not in html
