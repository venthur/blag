"""Pytest fixtures."""

import os
from argparse import Namespace
from collections.abc import Callable, Iterator
from tempfile import TemporaryDirectory

import pytest
from jinja2 import Environment, Template

from blag import blag, quickstart


@pytest.fixture
def environment(cleandir: str) -> Iterator[Environment]:
    """Create a Jinja2 environment."""
    site = {
        "base_url": "site base_url",
        "title": "site title",
        "description": "site description",
        "author": "site author",
    }
    env = blag.environment_factory("templates", globals_=dict(site=site))
    yield env


@pytest.fixture
def page_template(environment: Environment) -> Iterator[Template]:
    """Create a Jinja2 page-template."""
    yield environment.get_template("page.html")


@pytest.fixture
def article_template(environment: Environment) -> Iterator[Template]:
    """Create a Jinja2 article-template."""
    yield environment.get_template("article.html")


@pytest.fixture
def index_template(environment: Environment) -> Iterator[Template]:
    """Create a Jinja2 index-template."""
    yield environment.get_template("index.html")


@pytest.fixture
def archive_template(environment: Environment) -> Iterator[Template]:
    """Create a Jinja2 archive-template."""
    yield environment.get_template("archive.html")


@pytest.fixture
def tags_template(environment: Environment) -> Iterator[Template]:
    """Create a Jinja2 tags-template."""
    yield environment.get_template("tags.html")


@pytest.fixture
def tag_template(environment: Environment) -> Iterator[Template]:
    """Create a Jinja2 tag-template."""
    yield environment.get_template("tag.html")


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
        os.mkdir(f"{dir}/build")
        with open(f"{dir}/config.ini", "w") as fh:
            fh.write(config)
        # change directory
        old_cwd = os.getcwd()
        os.chdir(dir)
        quickstart.copy_default_theme()
        yield dir
        # and change back afterwards
        os.chdir(old_cwd)


@pytest.fixture
def args(cleandir: Callable[[], Iterator[str]]) -> Iterator[Namespace]:
    """Create a Namespace with default arguments."""
    args = Namespace(
        input_dir="content",
        output_dir="build",
        static_dir="static",
        template_dir="templates",
    )
    yield args
