"""
Tests for test_example, these tests should never fail
"""

import pytest
import sys

from src.test_example import main

def test_test_example() -> None:
    """Test that main doesn't return anything"""
    assert main() is None
