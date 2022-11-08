"""
Graph as a class
"""
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from mock import Mock

class AnimatedPlot():
    """Animation function for graphing"""
    def __init__ (self):
        """Constructor function for AnimPlot"""

        self.times = []
        self.rssi_values = []
        self.mock = Mock()

        self.fig, self.axis = plt.subplots()
        
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=125)

    def update(self, interval):
        """Updates the graph with new plots"""

        time, rssi_value, self.node_id = self.mock.get_latest()

        self.times.append(time)
        self.rssi_values.append(rssi_value)

        self.axis.clear()
        self.axis.plot(self.times, self.rssi_values)

        self.axis.axes.set_xlabel("Time in seconds")
        self.axis.axes.set_ylabel("RSSI Strength (ΔdBm)")

        self.axis.grid(axis = 'y')
        #self.ax.fill_between(self.times, self.rssi_values, alpha=0.5)

        title=plt.title("Frequency changes detected by sensor")
        title.set_weight('bold')

if __name__ == "__main__":
    anim_plot = AnimatedPlot()
    anim = anim_plot.ani
    plt.show()
