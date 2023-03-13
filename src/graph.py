"""
This module provides a graphical user interface (GUI) for displaying a dynamic
plot using the Tkinter library and the matplotlib library. It also allows the user to
start and stop recording the data and storing it in a csv file using the options
provided in the GUI. In other words, the data is stored as a Pandas DataFrame and can
be saved in a new file, appended to an existing file or overwritten in an existing
file based on the user's choice.
"""

from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from serial_interface import SerialInterface
from mock import Mock

class AnimatedPlot():
    """Animation function for graphing"""
    def __init__ (self, window = None, interface = 'mock'):
        """Constructor function for AnimPlot
            window specifies how many values should be used
            for the calculation of the running average
            (Allows latest values to have greater impact)
        """
        self.node_dict = defaultdict(lambda: ([],[]))
        self.window = window
        if interface == "serial":
            self.interface = SerialInterface()
        if interface == "mock":
            self.interface  = Mock()

        self.fig, self.axis = plt.subplots()
        #self.ani_playing = None
        #self.current_data = []
        self.animation = animation.FuncAnimation(self.fig, self.update, interval=25)
        self.paused = False

    def start_animation(self):
        '''Function to unpause animation'''
        self.animation.resume()
        self.paused = False

    def stop_animation(self):
        '''Function to pause animation'''
        self.animation.pause()
        self.paused = True

    def toggle_pause(self):
        '''Function to toggle the pausing of animation'''
        if self.paused:
            self.animation.resume()
        else:
            self.animation.pause()
        self.paused = not self.paused

    def update(self, _):
        """Updates the graph with new plots
            num_nodes should only be specified when using the mock
        """
        time, rssi_value, node_id = self.interface.get_values()
    #    self.current_data.append([time, rssi_value, node_id])
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

    def get_current_data(self):
        '''Return node dict in alternate format'''
        data = []

        for node_id, tup in self.node_dict.items():
            print("tup:",tup)
            time = tup[0]
            rssi = tup[1]
            #for i in range(0, len(time)):
            for _, (time_val, rssi_val) in enumerate(zip(time, rssi)):
                data.append([time_val, rssi_val, node_id])

        sorted(data, key=lambda x: x[0])
        return data

    def __str__(self):
        return "graph"

    def get_serial_interface(self):
        """returns the graphs serial interface"""
        if self.interface == SerialInterface:
            return self.interface
        return None

    def get_node_dict(self) -> dict:
        """Returns node dict, used for testing"""
        return self.node_dict

    def get_std_dev(self, node_id):
        """Returns the standard deviation of the RSSI values of a given node"""
        return np.format_float_positional(np.std(self.node_dict[node_id]), precision=3)

    def calculate_gradient(self, initial, final):
        """Get gradient between given points"""
        #initial, final = (time, rssi)
        delta_y = final[1] - initial[1]
        delta_x = final[0] - initial[0]

        return delta_y/delta_x

    def calculate_node_at_all_times(self, node, times):
        """Linearly interpolate all value for a given node"""
        node_all_times=[times, [None for i in range(0, len(times))]]
        for time in times:
            #Case where we don't need to calculate value
            if time in node[0]:
                time_index = node[0].index(time)
                node_all_times[1][times.index(time)] = node[1][time_index]
                continue

            #Get index of largest time before wanted time
            before_index = None
            for i in range (0, len(node[0])):
                if node[0][i] < time:
                    before_index = i

            #Cannot calculate if the time wanted is before readings
            if before_index is None:
                continue

            #Get smallest time after wanted time
            after_index = None
            for i in range(before_index, len(node[0])):
                if node[0][i] > time:
                    after_index = i
                    break

            #Cannot calculate if the time wanted is after readings
            if after_index is None:
                continue

            #Calculate gradient as g = dy/dx between the reading before and after time
            gradient = self.calculate_gradient(
                [node[0][before_index],node[1][before_index]],
                [node[0][after_index],node[1][after_index]]
            )

            #Get how much to multiply the gradient by
            gradient_scalar = node[0][after_index] - node[0][before_index]

            time_index = times.index(time)
            node_all_times[1][time_index] = node[1][before_index] + gradient * gradient_scalar

            #Get rid of readings where we could not calculate a value
        node_all_times_slice = [[],[]]
        for i in range(0,len(node_all_times[0])):
            if node_all_times[1][i] is not None:
                node_all_times_slice[0].append(node_all_times[0][i])
                node_all_times_slice[1].append(node_all_times[1][i])

        return node_all_times_slice

    def calculate_node_diff(self, node_id_1, node_id_2):
        """
            Returns the difference between node_id_1 and node_id_2
            Works by interpolating values for all times then doing a
            piecewise subtraction
        """

        node_1 = self.node_dict[node_id_1]
        node_2 = self.node_dict[node_id_2]

        #Create a list of every unique timestamp in both nodes
        times = sorted(list(set(node_1[0]+node_2[0])))

        node_1_list = self.calculate_node_at_all_times(node_1, times)
        node_2_list = self.calculate_node_at_all_times(node_2, times)

        diff = [[],[]]

        #Get [[Times],[Difference between interpolated RSSI strengths at those times]]
        for i in range (0, min(len(node_1_list[0]),len(node_2_list[0]))):
            diff[0].append(max(node_1_list[0][i], node_2_list[0][i]))
            diff[1].append(node_1_list[1][i] - node_2_list[1][i])

        self.node_dict['diff_' + str(node_id_1) + '_' + str(node_id_2)] = diff



    def set_window(self, window):
        '''Set self window as window'''
        self.window = window

if __name__ == "__main__":
    anim_plot = AnimatedPlot(interface = "serial")
    anim = anim_plot.ani
    plt.show()
    print(anim_plot.get_std_dev('Mock0'))
