import blag


def test_version() -> None:
    assert isinstance(blag.__VERSION__, str)
