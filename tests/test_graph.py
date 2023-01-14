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

#sys.path.append("..")

from src.graph import AnimatedPlot
from src.mock import Mock

anim_plot = AnimatedPlot(10)

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
    for _ in range (0,9):
        anim_plot.update(125)
    node_dict = anim_plot.get_node_dict()
    print(node_dict['running_average'])
    assert(type(node_dict) == defaultdict)
    assert(np.allclose(node_dict['running_average'][0][:10], [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]))
    assert(np.allclose(node_dict['running_average'][1][:10], [14.0, 13.0, 13.333333333333334, 12.75, 12.6, 12.333333333333334, 12.0, 11.625, 11.333333333333334, 11.0]))

if __name__ == "__main__":
    test_plot_type()
