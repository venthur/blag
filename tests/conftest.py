# remove when we don't support py38 anymore
from __future__ import annotations
from argparse import Namespace
from typing import Iterator, Callable
from tempfile import TemporaryDirectory
import os

import pytest
from jinja2 import Environment, Template

from blag import blag, quickstart


@pytest.fixture
def environment(cleandir: str) -> Iterator[Environment]:
    site = {
        'base_url': 'site base_url',
        'title': 'site title',
        'description': 'site description',
        'author': 'site author',
    }
    env = blag.environment_factory('templates', globals_=dict(site=site))
    yield env


@pytest.fixture
def page_template(environment: Environment) -> Iterator[Template]:
    yield environment.get_template('page.html')


@pytest.fixture
def article_template(environment: Environment) -> Iterator[Template]:
    yield environment.get_template('article.html')


@pytest.fixture
def index_template(environment: Environment) -> Iterator[Template]:
    yield environment.get_template('index.html')


@pytest.fixture
def archive_template(environment: Environment) -> Iterator[Template]:
    yield environment.get_template('archive.html')


@pytest.fixture
def tags_template(environment: Environment) -> Iterator[Template]:
    yield environment.get_template('tags.html')


@pytest.fixture
def tag_template(environment: Environment) -> Iterator[Template]:
    yield environment.get_template('tag.html')


@pytest.fixture
def cleandir() -> Iterator[str]:
    """Create a temporary working directory and cwd."""
    config = """
[main]
base_url = https://example.com/
title = title
description = description
author = a. u. thor
    """

    with TemporaryDirectory() as dir:
        for d in 'content', 'build', 'static':
            os.mkdir(f'{dir}/{d}')
        with open(f'{dir}/config.ini', 'w') as fh:
            fh.write(config)
        # change directory
        old_cwd = os.getcwd()
        os.chdir(dir)
        quickstart.copy_templates()
        yield dir
        # and change back afterwards
        os.chdir(old_cwd)


@pytest.fixture
def args(cleandir: Callable[[], Iterator[str]]) -> Iterator[Namespace]:

    args = Namespace(
        input_dir='content',
        output_dir='build',
        static_dir='static',
        template_dir='templates',
    )
    yield args
