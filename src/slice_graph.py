"""
A class for the slice graph, which takes an initial filename, creates a dataframe from the file
and plots it. Intended to clear up the code in gui.py and make updating slices easier.
"""
# Necessary imports
from tkinter import messagebox
import pandas as pd
import matplotlib
import numpy as np
from matplotlib import pyplot as plt

try:
    matplotlib.use("TkAgg")
except ImportError:
    print("Error importing matplotlib TkAgg")

class SliceGraph():
    """
    Class containing data for slice graph as well
    as getter functions, and multiple functions
    that can be chained to convert a filename to a
    plot via a dataframe.
    """
    def __init__(self, filename):
        """Call to initialise the class, filename acquired
        in gui.py/filedialog.askopenfilename call"""
        self.filename = filename
        # Creates initial plot
        self.data_frame = self.file_to_df(filename)
        self.slice_plot = self.df_to_plot(self.data_frame)
        self.slice_fig = self.get_plot_fig()

    def get_data_frame(self) -> pd.DataFrame:
        """Returns dataframe contained by the class"""
        return self.data_frame

    def get_plot_fig(self) -> plt.Figure:
        """Returns figure contained by class"""
        return self.slice_plot.get_figure()

    def get_max_time(self) -> np.float64:
        """Returns the maximum time of dataframe"""
        max_time = self.data_frame["time"].iloc[-1]
        return max_time

    def file_to_df(self, filename, start_time_str = "0", end_time_str = "0") -> pd.DataFrame:
        """Helper function: [filename,start_time,end_time]
        - > [expected dataframe or None if fail]"""

        try:
            start_time = float(start_time_str)
            end_time = float(end_time_str)
        except ValueError as verror:
            start_time = 0
            end_time = self.data_frame["time"].iloc[-1]
            messagebox.showerror("Value Error",verror)

        try:
            if filename is not None:
                data_frame_temp=pd.read_csv(filename)#, usecols=csv_cols, delimiter=delim)
            if start_time >= end_time:
                self.data_frame = data_frame_temp
            else:
                self.data_frame = data_frame_temp.query("@start_time <= time <= @end_time")

        except UnicodeDecodeError:
            print("Wrong file format: File chosen is not a csv!")
            self.data_frame = None

        return self.data_frame


    def df_to_plot(self, data_frame) -> plt.Axes:
        """Helper function: [data_frame] -> [expected plot in required format]"""
        try:
            self.slice_plot = data_frame.plot(x="time",y="rssi")
            # Used to ensure consistency between graphs in app
            self.slice_plot.axes.set_xlabel("Time in seconds")
            self.slice_plot.axes.set_ylabel("RSSI Strength (dBm)")
            title=plt.title("Frequency changes detected by sensor")
            title.set_weight('bold')
        except AttributeError:
            print("Incorrect dataframe input!")
            self.slice_plot = None

        return self.slice_plot

    def make_slice(self, start_time, end_time) -> None:
        """Function that takes start and end time, and alters the graph to show the slice given"""
        filename = self.filename
        self.data_frame = self.file_to_df(filename, start_time, end_time)
        self.slice_plot = self.df_to_plot(self.data_frame)
        self.slice_fig = self.get_plot_fig()

    def __str__(self):
        return "SliceGraph"
