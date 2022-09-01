# remove when we don't support py38 anymore
from __future__ import annotations

from pytest import MonkeyPatch

from blag.quickstart import get_input, quickstart


def test_get_input_default_answer(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr('builtins.input', lambda x: '')
    answer = get_input("foo", "bar")
    assert answer == 'bar'


def test_get_input(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr('builtins.input', lambda x: 'baz')
    answer = get_input("foo", "bar")
    assert answer == 'baz'


def test_quickstart(cleandir: str, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr('builtins.input', lambda x: 'foo')
    quickstart(None)
    with open('config.ini', 'r') as fh:
        data = fh.read()
    assert 'base_url = foo' in data
    assert 'title = foo' in data
    assert 'description = foo' in data
    assert 'author = foo' in data
