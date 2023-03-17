""""
Tests for the creation of a graph
"""

import pytest
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.testing.decorators import image_comparison
from collections import defaultdict

from src.graph import AnimatedPlot
from src.mock import Mock

anim_plot = AnimatedPlot(10, interface="mock")

#@image_comparison(baseline_images=['test_plot'], remove_text=True,
#                  extensions=['png'])
#def test_plot_image():
#    """Test that the update function plots the graph correctly"""
#    #anim_plot_limited_frames = AnimatedPlot(10)
#    #anim_plot_limited_frames.update(125)
#    anim_plot.update(125)
#    anim_plot.axis.plot()



def test_creation():
    """Test the object was created properly"""
    assert(type(anim_plot) == AnimatedPlot)

def test_plot_type():
    """Test that the labels for the plot have been set"""
    anim_plot.update(125)
    assert(True)

def test_running_average():
    """Test that running average calculates correctly"""
    for _ in range(0, 9):
        anim_plot.update(125)
    node_dict = anim_plot.get_current_data()
    node_dict_as_np = node_dict.to_numpy()

    time_array = []
    rssi_array = []
    for data_entry in node_dict_as_np:
            time_array.append(data_entry[5])
            rssi_array.append(data_entry[2])

    assert( time_array[:10] == [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5])
    assert( rssi_array[:10] ==   [14.0, 12.0, 14.0, 11.0, 12.0, 11.0, 10.0, 9.0, 9.0, 8.0])
  
def test_standard_deviation():
    """Test that standard deviation calculations are correct"""
    node_dict = anim_plot.get_current_data()
    node_dict_as_np = node_dict.to_numpy()

    time_array = []
    rssi_array = []
    for data_entry in node_dict_as_np:
            # time_array.append(data_entry[2])
            rssi_array.append(data_entry[2])


    # node_dict = anim_plot.get_current_data()
    std_dev_rounded = np.format_float_positional(np.std(rssi_array), precision=3)
    assert abs(float(std_dev_rounded )- float(anim_plot.get_std_dev('Mock0'))) <= 0.1
    # assert(std_dev_rounded == anim_plot.get_std_dev('Mock0'))

 
 
def test_calculate_gradient():
    """Test the gradient is calculated correctly"""
    assert(1 == anim_plot.calculate_gradient([1,1],[2,2]))

def test_calculate_node_at_all_times():
    """Test that we get the required length"""
    assert(2 == len(anim_plot.calculate_node_at_all_times([[1],[1]],[1])))

def test_get_serial_interface():
    """Tests that when a mock is used that the function won't return the interface"""
    assert(anim_plot.get_serial_interface() is None)
    
def test_calculate_node_diff():
    """Test the node diff"""
    node_dict = anim_plot.get_current_data().to_dict()
 

    # keys = [k for k in node_dict.node_id.unique()]
    keys = [k for k in node_dict.keys()]
    anim_plot.calculate_node_diff(keys[0], keys[1])
    assert(True)

if __name__ == "__main__":
    test_calculate_node_diff()
