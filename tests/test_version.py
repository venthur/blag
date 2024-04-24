"""Test the version module."""

import blag


def test_version() -> None:
    """Test the version of the package."""
    assert isinstance(blag.__VERSION__, str)
