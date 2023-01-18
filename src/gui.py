"""
This module provides a graphical user interface (GUI) for displaying a dynamic
plot using the Tkinter library and the matplotlib library. It also allows the user to
start and stop recording the data and storing it in a csv file.
"""
import tkinter as tk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from graph import AnimatedPlot

matplotlib.use("TkAgg")

class Main():
    """TKinter window with embedded MatPlotLib graph"""

    def __init__(self):
        """
        Initialize the Main class.

        Creates the main window with a title 'GUI' and a fixed size of 500x500 pixels.
        Initializes the animated plot, canvas, and dataframe.
        """
        self.root = tk.Tk()
        self.root.title('GUI')
        self.root.geometry("500x500")
        self.animated_plot = AnimatedPlot()
        self.canvas = FigureCanvasTkAgg(self.animated_plot.fig, self.root)
        self.canvas.get_tk_widget().pack()

        self.start_stop_button = tk.Button(self.root,
        command=self.start_stop_recording, text="Start/Stop Recording")

        self.start_stop_button.pack()
        self.recording = False
        self.data = pd.DataFrame(columns=['time', 'rssi_value', 'node_id'])

    def start_stop_recording(self):
        """Button callback that records data"""
        if not self.recording:
            self.recording = True
            self.start_stop_button.config(text='Stop Recording')
        else:
            self.recording = False
            self.start_stop_button.config(text='Start Recording')
            self.data.to_csv('recording.csv', index=False)

    def __str__(self):
        return "GUI"

if __name__ == "__main__":
    my_gui = Main()
    my_gui.root.mainloop()
