import datetime

import pytest

from blag import blag


@pytest.fixture
def environment():
    site = {
        'base_url': 'site base_url',
        'title': 'site title',
        'description': 'site description',
        'author': 'site author',
    }
    env = blag.environment_factory(globals_=dict(site=site))
    yield env


@pytest.fixture
def page_template(environment):
    yield environment.get_template('page.html')


@pytest.fixture
def article_template(environment):
    yield environment.get_template('article.html')


@pytest.fixture
def archive_template(environment):
    yield environment.get_template('archive.html')


@pytest.fixture
def tags_template(environment):
    yield environment.get_template('tags.html')


@pytest.fixture
def tag_template(environment):
    yield environment.get_template('tag.html')


def test_page(page_template):
    ctx = {
        'content': 'this is the content',
        'title': 'this is the title',
    }
    result = page_template.render(ctx)
    assert 'this is the content' in result
    assert 'this is the title' in result


def test_article(article_template):
    ctx = {
        'content': 'this is the content',
        'title': 'this is the title',
    }
    result = article_template.render(ctx)
    assert 'this is the content' in result
    assert 'this is the title' in result


def test_archive(archive_template):
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
    assert 'site title' in result

    assert 'this is a title' in result
    assert '1980-05-09' in result
    assert 'https://example.com/link' in result


def test_tags(tags_template):
    tags = [('foo', 42)]
    ctx = {
        'tags': tags,
    }
    result = tags_template.render(ctx)
    assert 'Tags' in result

    assert 'foo.html' in result
    assert 'foo' in result
    assert '42' in result


def test_tag(tag_template):
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
    assert 'Tag foo' in result

    assert 'this is a title' in result
    assert '1980-05-09' in result
    assert 'https://example.com/link' in result
