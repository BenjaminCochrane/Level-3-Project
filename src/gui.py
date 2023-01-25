"""
This module provides a graphical user interface (GUI) for displaying a dynamic
plot using the Tkinter library and the matplotlib library. It also allows the user to
start and stop recording the data and storing it in a csv file.
"""
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from graph import AnimatedPlot

matplotlib.use("TkAgg")

class Main():
#     def __init__(self, animated_plot):
#         self.animated_plot = animated_plot

#         self.root = Tk()
#         self.root.title("RSSI Analyzer")

#         self.start_button = Button(self.root, text="Start Recording", command=self.start_recording)
#         self.start_button.grid(row=0, column=0)

#         self.stop_button = Button(self.root, text="Stop Recording", command=self.stop_recording)
#         self.stop_button.grid(row=0, column=1)

#     def start_recording(self):
#         self.animated_plot.ani.event_source.start()

#     def stop_recording(self):
#         data = self.animated_plot.get_current_data()
#         df = pd.DataFrame(data, columns=["Time", "RSSI Value", "Node ID"])
#         df.to_csv("data.csv")

# if __name__ == "__main__":
#     animated_plot = AnimatedPlot(10)
#     gui = Main(animated_plot)
#     plt.show()

 

    def __init__(self, animated_plot):
        
        self.animated_plot = animated_plot
        self.root = tk.Tk()
        self.root.title("RSSI Strength Plot")
        
        self.figure = self.animated_plot.fig
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack()
        
        self.start_button = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.start_button.pack()
        
        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack()
        
        self.root.mainloop()

    def start_recording(self):
        self.animated_plot.ani.event_source.start()
    
    def stop_recording(self):
        # self.animated_plot.ani.event_source.stop()
        data = self.animated_plot.get_current_data()
        df = pd.DataFrame(data, columns=["Time", "RSSI Value", "Node ID"])
        df.to_csv("data.csv")
        
 
if __name__ == "__main__":
    animated_plot = AnimatedPlot(10)
    gui = Main(animated_plot)
    plt.show()

 

 