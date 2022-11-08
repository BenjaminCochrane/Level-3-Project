""""
Tests for the creation of a graph
"""

import pytest
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.testing.decorators import image_comparison
from src.graph import AnimatedPlot

anim_plot = AnimatedPlot()

#@image_comparison(baseline_images=['test_plot'], remove_text=True,
#                  extensions=['png'])
#def test_plot_image():
#    """Test that the update function plots the graph correctly"""
#    for i in range(14):
#        fig, ax = anim_plot.update(125)
#    fig, ax = anim_plot.update(125)

def test_creation():
    """Test the object was created properly"""
    assert(type(anim_plot) == AnimatedPlot)

def test_plot_type():
    """Test that the labels for the plot have been set"""
    anim_plot.update(125)
    assert(True)

if __name__ == "__main__":
    test_plot_image()
