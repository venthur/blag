# remove when we don't support py38 anymore
from __future__ import annotations
import datetime

from jinja2 import Template


def test_page(page_template: Template) -> None:
    ctx = {
        'content': 'this is the content',
        'title': 'this is the title',
    }
    result = page_template.render(ctx)
    assert 'this is the content' in result
    assert 'this is the title' in result


def test_article(article_template: Template) -> None:
    ctx = {
        'content': 'this is the content',
        'title': 'this is the title',
        'date': datetime.datetime(1980, 5, 9),
    }
    result = article_template.render(ctx)
    assert 'this is the content' in result
    assert 'this is the title' in result
    assert '1980-05-09' in result


def test_index(index_template: Template) -> None:
    entry = {
        'title': 'this is a title',
        'dst': 'https://example.com/link',
        'date': datetime.datetime(1980, 5, 9),
    }
    archive = [entry]
    ctx = {
        'archive': archive,
    }
    result = index_template.render(ctx)
    assert 'site title' in result

    assert 'this is a title' in result
    assert '1980-05-09' in result
    assert 'https://example.com/link' in result

    assert '/archive.html' in result


def test_archive(archive_template: Template) -> None:
    entry = {
        'title': 'this is a title',
        'dst': 'https://example.com/link',
        'date': datetime.datetime(1980, 5, 9),
    }
    archive = [entry]
    ctx = {
        'archive': archive,
    }
    result = archive_template.render(ctx)
    assert 'Archive' in result

    assert 'this is a title' in result
    assert '1980-05-09' in result
    assert 'https://example.com/link' in result


def test_tags(tags_template: Template) -> None:
    tags = [('foo', 42)]
    ctx = {
        'tags': tags,
    }
    result = tags_template.render(ctx)
    assert 'Tags' in result

    assert 'foo.html' in result
    assert 'foo' in result
    assert '42' in result


def test_tag(tag_template: Template) -> None:
    entry = {
        'title': 'this is a title',
        'dst': 'https://example.com/link',
        'date': datetime.datetime(1980, 5, 9),
    }
    archive = [entry]
    ctx = {
        'tag': 'foo',
        'archive': archive,
    }
    result = tag_template.render(ctx)
    assert 'foo' in result

    assert 'this is a title' in result
    assert '1980-05-09' in result
    assert 'https://example.com/link' in result
