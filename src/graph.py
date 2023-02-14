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

        self.calculate_node_diff('Mock0', 'Mock1')


        self.axis.clear()
        for key, value in self.node_dict.items():
            self.axis.plot(value[0], value[1], label=key)

        self.axis.axes.set_xlabel("Time in seconds")
        self.axis.axes.set_ylabel("RSSI Strength (ΔdBm)")

        self.axis.grid(axis = 'y')
        self.axis.legend()

        title=plt.title("Frequency changes detected by sensor")
        title.set_weight('bold')

    def get_node_dict(self) -> dict:
        """Returns node dict, used for testing"""
        return self.node_dict

    def get_std_dev(self, node_id):
        """Returns the standard deviation of the RSSI values of a given node"""
        return np.std(self.node_dict[node_id])

    def calculate_gradient(self, initial, final):
        """Take tuple of thing"""
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



if __name__ == "__main__":
    anim_plot = AnimatedPlot(interface = "mock")
    anim = anim_plot.ani
    plt.show()
