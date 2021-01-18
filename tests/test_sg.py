from datetime import datetime

import markdown
import pytest

from sg import sg


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
    md = sg.markdown_factory()
    html, _ = sg.convert_markdown(md, input_)
    assert expected in html


@pytest.mark.parametrize("input_, expected", [
    ('foo: bar', {'foo': 'bar'}),
    ('tags: this, is, a, test\n', {'tags': ['this', 'is', 'a', 'test']}),
    ('date: 2020-01-01 12:10', {'date': datetime(2020, 1, 1, 12, 10)}),
])
def test_convert_metadata(input_, expected):
    md = sg.markdown_factory()
    _, meta = sg.convert_markdown(md, input_)
    assert expected == meta


def test_markdown_factory():
    md = sg.markdown_factory()
    assert isinstance(md, markdown.Markdown)
