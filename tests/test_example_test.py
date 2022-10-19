import pytest,sys

from src.test_example import main

def test_test_example() -> None:
    assert main() is None
