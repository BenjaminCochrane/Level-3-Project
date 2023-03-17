"""
This module provides a graphical user interface (GUI) for displaying a dynamic
plot using the Tkinter library and the matplotlib library. It also allows the user to
start and stop recording the data and storing it in a csv file using the options
provided in the GUI. In other words, the data is stored as a Pandas DataFrame and can
be saved in a new file, appended to an existing file or overwritten in an existing
file based on the user's choice.
"""

#from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import pandas as pd
from serial_interface import SerialInterface
from mock import Mock
from packet_format import PacketFormat

class AnimatedPlot():
    """Animation function for graphing"""
    def __init__ (self, window = None, interface = 'serial'):
        """Constructor function for AnimPlot
            window specifies how many values should be used
            for the calculation of the running average
            (Allows latest values to have greater impact)
        """
        expected_format = PacketFormat()
        self.data = pd.DataFrame(columns = expected_format.__slots__)

        self.window = window
        if interface == "serial":
            self.interface = SerialInterface()
        if interface == "mock":
            self.interface  = Mock()
        self.fig, self.axis = plt.subplots()
        self.instances={"animation":animation.FuncAnimation(self.fig,self.update, interval=25),
                        "paused": False,
                        "colors":{},
                        "colors_count":0,
                        }

        color_map = plt.get_cmap('gist_rainbow')
        for i in range(0,6):
            self.instances["colors"][i]= color_map(1.*i/6)
            # self.colors[i] = color_map(1.*i/6)

    def start_animation(self):
        '''Function to unpause animation'''
        self.instances["animation"].resume()
        # self.animation.resume()
        self.instances["paused"] = False
        # self.paused = False

    def stop_animation(self):
        '''Function to pause animation'''
        # self.animation.pause()
        self.instances["animation"].pause()
        # self.paused = True
        self.instances["paused"] =True

    def toggle_pause(self):
        '''Function to toggle the pausing of animation'''
        # if self.paused:
        if self.instances["paused"] :
            # self.animation.resume()
            self.instances["animation"].resume()
        else:
            # self.animation.pause()
            self.instances["animation"].pause()
        self.instances["paused"] = not self.instances["paused"]
        # self.paused = not self.paused

    def update(self, _):
        """Updates the graph with new plots
            num_nodes should only be specified when using the mock
        """

        data = self.interface.get_values()
        if data:
            for packet in data:
                self.data.loc[-1] = packet
                self.data.index = self.data.index + 1
                self.data = self.data.sort_index()

        self.axis.clear()

        self.data = self.data.sort_values(by='time')
        time_slice = self.data

        if len(self.data.index) > 0:
            df_time = self.data.iloc[-1].time - 60
            time_slice = self.data[self.data['time'] >= df_time]

        for node in sorted(time_slice.node_id.unique()):
            values = time_slice.loc[self.data['node_id'] == node]

            #Assign color
            # if not self.colors.get(node):
            if not self.instances["colors"].get(node):
                self.instances["colors"][node]= self.instances["colors"].pop(
                    self.instances["colors_count"])
                # self.colors[node] = self.colors.pop(self.colors_count)
                # self.colors_count += 1
                self.instances["colors_count"] +=1

            # self.axis.plot(values['time'], values['rssi'], label=node, color=self.colors[node])
            self.axis.plot(values['time'], values['rssi'], label=node,
                           color=self.instances["colors"][node])

        self.axis.axes.set_xlabel("Time in seconds")
        self.axis.axes.set_ylabel("RSSI Strength (dBm)")

        self.axis.grid(axis = 'y')
        self.axis.legend(loc='upper left')
        title=plt.title("Frequency changes detected by sensor (60s timeframe)")
        title.set_weight('bold')

    def get_current_data(self):
        '''Returns self.data sorted by time'''
        return self.data.sort_values(by=['time'])

    def __str__(self):
        return "graph"

    def get_serial_interface(self):
        """returns the graphs serial interface"""
        if self.interface == SerialInterface:
            return self.interface
        return None

    def get_std_dev(self, node_id):
        """Returns the standard deviation of the RSSI values of a given node"""
        node_values = self.data.loc[self.data['node_id'] == node_id, 'rssi'].tolist()

        return np.format_float_positional(np.std(node_values),precision=3)

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

        node_id = 'diff_' + str(node_id_1) + '_' + str(node_id_2)

        time_slice = self.data

        if len(self.data.index) > 0:
            df_time = self.data.iloc[-1].time - 60
            time_slice = self.data[self.data['time'] >= df_time]

        last_time_calculated = time_slice[time_slice['node_id'] == node_id]['time'].tolist()
        if len(last_time_calculated) == 0:
            last_time_calculated = 0
        else:
            last_time_calculated = last_time_calculated[-1]

        node_1 = time_slice.loc[(time_slice['node_id'] == node_id_1)
                                & (time_slice['time'] > last_time_calculated)]
        node_2 = time_slice.loc[(time_slice['node_id'] == node_id_2)
                                & (time_slice['time'] > last_time_calculated)]

        node_1 = [node_1['time'].to_list(), node_1['rssi'].to_list()]
        node_2 = [node_2['time'].to_list(), node_2['rssi'].to_list()]

        #Create a list of every unique timestamp in both nodes
        times_needed = [time for time in sorted(list(set(node_1[0]+node_2[0])))
                        if time >= last_time_calculated]

        node_1 = self.calculate_node_at_all_times(node_1, times_needed)
        node_2 = self.calculate_node_at_all_times(node_2, times_needed)


        node_data={"times":[], "differences":[] , "row":[]}
        #Get [[Times],[Difference between interpolated RSSI strengths at those times]]
        for i in range (0, min(len(node_1[0]),len(node_2[0]))):
            node_data["times"].append(max(node_1[0][i], node_2[0][i]))
            node_data["differences"].append(node_1[1][i] - node_2[1][i])

        for time, diff in zip(node_data["times"] , node_data["differences"]):
            node_data['row'] = []
            for _, slot in enumerate(PacketFormat().__slots__):
                if slot == 'node_id':
                    node_data["row"].append(node_id)
                elif slot == 'time':
                    node_data["row"].append(time)
                elif slot == 'rssi':
                    node_data["row"].append(diff)
                else:
                    node_data["row"].append(None)

            self.data.loc[-1] = node_data["row"]
            self.data.index = self.data.index + 1
            self.data = self.data.sort_index()

    def reset_data(self):
        '''Clears all data'''
        expected_format = PacketFormat()
        self.data = pd.DataFrame(columns = expected_format.__slots__)

    def switch_interface(self, interface_object):
        '''Switch interface to given interface object'''
        self.interface = interface_object


    def set_window(self, window):
        '''Set self window as window'''
        self.window = window
