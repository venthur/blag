"""Test the version module."""


# remove when we don't support py38 anymore
from __future__ import annotations

import blag


def test_version() -> None:
    """Test the version of the package."""
    assert isinstance(blag.__VERSION__, str)
