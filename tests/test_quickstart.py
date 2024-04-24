"""Tests for the quickstart module."""

import os

from pytest import MonkeyPatch

from blag.quickstart import get_input, quickstart


def test_get_input_default_answer(monkeypatch: MonkeyPatch) -> None:
    """Test get_input with default answer."""
    monkeypatch.setattr("builtins.input", lambda x: "")
    answer = get_input("foo", "bar")
    assert answer == "bar"


def test_get_input(monkeypatch: MonkeyPatch) -> None:
    """Test get_input."""
    monkeypatch.setattr("builtins.input", lambda x: "baz")
    answer = get_input("foo", "bar")
    assert answer == "baz"


def test_quickstart(cleandir: str, monkeypatch: MonkeyPatch) -> None:
    """Test quickstart."""
    monkeypatch.setattr("builtins.input", lambda x: "foo")
    quickstart(None)
    with open("config.ini") as fh:
        data = fh.read()
    assert "base_url = foo" in data
    assert "title = foo" in data
    assert "description = foo" in data
    assert "author = foo" in data

    for template in (
        "archive.html",
        "article.html",
        "base.html",
        "index.html",
        "page.html",
        "tag.html",
        "tags.html",
    ):
        assert os.path.exists(f"templates/{template}")

    for directory in "build", "content", "static":
        assert os.path.exists(directory)
