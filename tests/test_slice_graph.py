"""
Tests for slice_graph class
"""

import pytest
import sys
import os
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

from src.slice_graph import SliceGraph

# Get the file for testing
path = ""
try:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),'test_file.csv'))
except FileNotFoundError:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','test_file.csv'))

# Preliminary setup for some shared variables
slice_graph = SliceGraph(path)
test_df = pd.read_csv(path)

print(test_df)

def test_creation():
    """Test creation of SliceGraph"""
    assert(type(slice_graph)==SliceGraph)

def test_get_data_frame():
    """Test data frame repr. of slice graph"""
    assert(type(slice_graph.get_data_frame()==pd.DataFrame))

def test_get_plot_fig():
    """Test plot fig representation of the plot figure variable"""
    assert(type(slice_graph.get_plot_fig()==plt.Figure))

def test_file_to_df():
    """Test function to see if return type as expected"""
    assert(type(slice_graph.file_to_df(path))==pd.DataFrame)

def test_file_to_df_content():
    """Tests the equality of dataframes, including content"""
    df = slice_graph.get_data_frame()
    pd.testing.assert_frame_equal(test_df, df)
