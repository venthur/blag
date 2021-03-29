from tempfile import TemporaryDirectory
from os import mkdir

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


@pytest.fixture
def tempdir():
    with TemporaryDirectory() as dir:
        for d in 'content', 'build', 'static', 'templates':
            mkdir(f'{dir}/{d}')
        yield dir


@pytest.fixture
def args(tempdir):

    class NameSpace:
        def __init__(self, **kwargs):
            for name in kwargs:
                setattr(self, name, kwargs[name])

    args = NameSpace(
            input_dir=f'{tempdir}/content',
            output_dir=f'{tempdir}/build',
            static_dir=f'{tempdir}/static',
            template_dir=f'{tempdir}/templates',
    )
    yield args
