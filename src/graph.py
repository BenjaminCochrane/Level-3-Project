"""
Graph as a class
"""
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
#from serial_interface import SerialInterface
from mock import Mock

class AnimatedPlot():
    """Animation function for graphing"""
    def __init__ (self, window = None):
        """Constructor function for AnimPlot
            window specifies how many values should be used
            for the calculation of the running average
            (Allows latest values to have greater impact)
        """
        self.node_dict = defaultdict(lambda: ([],[]))
        self.window = window
        self.mock = Mock()
        self.fig, self.axis = plt.subplots()
        self.ani_playing = None
        self.current_data = []
    def start_animation(self):
        '''Function to start animation'''
        self.ani_playing = animation.FuncAnimation(self.fig, self.update, interval=125)
        self.ani_playing.event_source.start()
        plt.show()
    def stop_animation(self):
        '''Function to stop animation'''
        self.ani_playing.event_source.stop()
    def get_ani_playing(self):
        '''Function to get the state of the animation'''
        return self.ani_playing
    def update(self, _, num_nodes=1):
        """Updates the graph with new plots
            num_nodes should only be specified when using the mock
        """
        time, rssi_value, node_id = self.mock.get_latest(num_nodes)
        self.current_data.append([time, rssi_value, node_id])
        self.node_dict[node_id][0].append(time)
        self.node_dict[node_id][1].append(rssi_value)
        #Running average
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
        #self.current_data.append((time, rssi_value, node_id))
    def get_current_data(self):
        '''Function that returns the current data'''
        print("get_current_data method called, current_data:", self.current_data)
        return self.current_data
    def __str__(self):
        return "graph"

    def get_node_dict(self) -> dict:
        """Returns node dict, used for testing"""
        return self.node_dict

    def get_std_dev(self, node_id):
        """Returns the standard deviation of the RSSI values of a given node"""
        return np.std(self.node_dict[node_id])

if __name__ == "__main__":
    anim_plot = AnimatedPlot(10)
    anim = anim_plot.ani
    plt.show()
    print(anim_plot.get_std_dev('Mock0'))
