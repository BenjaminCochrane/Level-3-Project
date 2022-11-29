"""
Graph as a class
"""
import matplotlib.pyplot as plt
from matplotlib import animation
#from serial_interface import SerialInterface
from mock import Mock

class AnimatedPlot():
    """Animation function for graphing"""
    def __init__ (self):
        """Constructor function for AnimPlot"""

        self.node_dict = {}

        #self.times = []
        #self.rssi_values = []
        #self.serial_interface = SerialInterface()
        self.mock = Mock()

        self.fig, self.axis = plt.subplots()

        self.ani = animation.FuncAnimation(self.fig, self.update, interval=125)

    def update(self, _):
        """Updates the graph with new plots"""

        time, rssi_value, node_id = self.mock.get_latest()

        try:
            self.node_dict[node_id][0].append(time)
            self.node_dict[node_id][1].append(rssi_value)
        except KeyError:
            self.node_dict[node_id] = [[time], [rssi_value]]

        #self.times.append(time)
        #self.rssi_values.append(rssi_value)


        self.axis.clear()
        for key, value in self.node_dict.items():
            self.axis.plot(value[0], value[1], label=key)

        self.axis.axes.set_xlabel("Time in seconds")
        self.axis.axes.set_ylabel("RSSI Strength (ΔdBm)")

        self.axis.grid(axis = 'y')
        self.axis.legend()
        #self.ax.fill_between(self.times, self.rssi_values, alpha=0.5)

        title=plt.title("Frequency changes detected by sensor")
        title.set_weight('bold')

    def __str__(self):
        return "graph"

if __name__ == "__main__":
    anim_plot = AnimatedPlot()
    anim = anim_plot.ani
    plt.show()
