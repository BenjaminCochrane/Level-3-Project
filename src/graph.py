"""
Graph as a class
"""
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from serial_interface import SerialInterface
from mock import Mock

class AnimatedPlot():
    """Animation function for graphing"""
    def __init__ (self, window = None, interface = "mock"):
        """Constructor function for AnimPlot
            window specifies how many values should be used
            for the calculation of the running average
            (Allows latest values to have greater impact)
        """

        #self.node_dict = {}
        self.node_dict = defaultdict(lambda: ([],[]))
        self.window = window

        if interface == "serial":
            self.interface = SerialInterface()
        if interface == "mock":
            self.interface  = Mock()

        self.fig, self.axis = plt.subplots()

        self.ani = animation.FuncAnimation(self.fig, self.update, interval=250)

    def update(self, _):
        """Updates the graph with new plots
            num_nodes is only used with the mock
        """

        data = self.interface.get_values()


        if data:
            for tup in data:
                self.node_dict[tup[2]][0].append(tup[0])
                self.node_dict[tup[2]][1].append(tup[1])

            time, _, node_id = data[0][0],data[0][1],data[0][2]

            self.node_dict['running_average'][0].append(time)
            if self.window:
                count = min(self.window, len(self.node_dict[node_id][1]))
                self.node_dict['running_average'][1].append(
                    sum(self.node_dict[node_id][1][len(self.node_dict[node_id][1]) - count:])/count
                )
            else:
                self.node_dict['running_average'][1].append(
                    sum(self.node_dict[node_id][1])/len(self.node_dict[node_id][0])
                )


        self.axis.clear()
        for key, value in self.node_dict.items():
            self.axis.plot(value[0], value[1], label=key)

        self.axis.axes.set_xlabel("Time in seconds")
        self.axis.axes.set_ylabel("RSSI Strength (ΔdBm)")

        self.axis.grid(axis = 'y')
        self.axis.legend()

        title=plt.title("Frequency changes detected by sensor")
        title.set_weight('bold')

    def __str__(self):
        return "graph"

    def get_node_dict(self) -> dict:
        """Returns node dict, used for testing"""
        return self.node_dict

    def get_std_dev(self, node_id):
        """Returns the standard deviation of the RSSI values of a given node"""
        return np.std(self.node_dict[node_id])


if __name__ == "__main__":
    anim_plot = AnimatedPlot(interface = "serial")
    anim = anim_plot.ani
    plt.show()
