from jinja2 import Environment, PackageLoader
import pytest


@pytest.fixture
def environment():
    env = Environment(
            loader=PackageLoader('blag', 'templates')
    )
    yield env


@pytest.fixture
def page_template(environment):
    yield environment.get_template('page.html')


@pytest.fixture
def article_template(environment):
    yield environment.get_template('article.html')


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
