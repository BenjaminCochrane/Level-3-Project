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

    assert (type(mock_obj.get_latest()) == list)

def test_number_datapoints() -> None:
    """Test that the mock returns the correct number of data points"""
    xs = []
    ys = []

    for i in range(0,10):
        listt=mock_obj.get_latest()[0]
        x, y, nodeID =  listt[5],  listt[2],  listt[0]
        xs.append(x)
        ys.append(y)

    assert (len(xs) == 10)
    assert (len(ys) == 10)

def test_node_id() -> None:
    """Test that the node_id is valid"""
    listt=mock_obj.get_latest()[0]
    nodeID = listt[0]
    assert (type(nodeID) == str)

def test_point_validity() -> None:
    """Test that the points are reasonable"""

    for i in range(0,10):
        listt=mock_obj.get_latest()[0]
        y  =  listt[2]
        assert (0 < y < 40)

def test_string_representation() -> None:
    """Test string representation"""

    assert(type(str(Mock)) == str)
