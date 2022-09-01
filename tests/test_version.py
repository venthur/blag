# remove when we don't support py38 anymore
from __future__ import annotations

import blag


def test_version() -> None:
    assert isinstance(blag.__VERSION__, str)
