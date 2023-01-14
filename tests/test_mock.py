"""
Tests for the mocking of data
"""

import pytest
import sys
#sys.path.append("..")

from src.mock import Mock
mock_obj = Mock()

def test_mock_datatype() -> None:
    """Test that the mock returns a tuple of data"""

    assert (type(mock_obj.get_latest()) == tuple)

def test_number_datapoints() -> None:
    """Test that the mock returns the correct number of data points"""
    xs = []
    ys = []

    for i in range(0,10):
        x,y, nodeID = mock_obj.get_latest()
        xs.append(x)
        ys.append(y)

    assert (len(xs) == 10)
    assert (len(ys) == 10)

def test_node_id() -> None:
    """Test that the node_id is valid"""
    x,y, node_id = mock_obj.get_latest()
    assert (type(node_id) == str)

def test_point_validity() -> None:
    """Test that the points are reasonable"""

    for i in range(0,10):
        x,y,node_id = mock_obj.get_latest()
        assert (0 < y < 40)

def test_string_representation() -> None:
    """Test string representation"""

    assert(type(str(Mock)) == str)
