from datetime import datetime

import pytest
import markdown

from blag.markdown import convert_markdown, markdown_factory


@pytest.mark.parametrize("input_, expected", [
    # inline
    ('[test](test.md)', 'test.html'),
    ('[test](test.md "test")', 'test.html'),
    ('[test](a/test.md)', 'a/test.html'),
    ('[test](a/test.md "test")', 'a/test.html'),
    ('[test](/test.md)', '/test.html'),
    ('[test](/test.md "test")', '/test.html'),
    ('[test](/a/test.md)', '/a/test.html'),
    ('[test](/a/test.md "test")', '/a/test.html'),
    # reference
    ('[test][]\n[test]: test.md ''', 'test.html'),
    ('[test][]\n[test]: test.md "test"', 'test.html'),
    ('[test][]\n[test]: a/test.md', 'a/test.html'),
    ('[test][]\n[test]: a/test.md "test"', 'a/test.html'),
    ('[test][]\n[test]: /test.md', '/test.html'),
    ('[test][]\n[test]: /test.md "test"', '/test.html'),
    ('[test][]\n[test]: /a/test.md', '/a/test.html'),
    ('[test][]\n[test]: /a/test.md "test"', '/a/test.html'),
])
def test_convert_markdown_links(input_, expected):
    md = markdown_factory()
    html, _ = convert_markdown(md, input_)
    assert expected in html


@pytest.mark.parametrize("input_, expected", [
    ('foo: bar', {'foo': 'bar'}),
    ('foo: those are several words', {'foo': 'those are several words'}),
    ('tags: this, is, a, test\n', {'tags': ['this', 'is', 'a', 'test']}),
    ('tags: this, IS, a, test', {'tags': ['this', 'is', 'a', 'test']}),
    ('date: 2020-01-01 12:10', {'date':
                                datetime(2020, 1, 1, 12, 10).astimezone()}),
])
def test_convert_metadata(input_, expected):
    md = markdown_factory()
    _, meta = convert_markdown(md, input_)
    assert expected == meta


def test_markdown_factory():
    md = markdown_factory()
    assert isinstance(md, markdown.Markdown)
