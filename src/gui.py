"""
This module provides a graphical user interface (GUI) for displaying a dynamic
plot using the Tkinter library and the matplotlib library. It also allows the user to
start and stop recording the data and storing it in a csv file using the options 
provided in the GUI. In other words, the data is stored as a Pandas DataFrame and can 
be saved in a new file, appended to an existing file or overwritten in an existing 
file based on the user's choice.
"""
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import datetime
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph import AnimatedPlot


headless = None
try:
    matplotlib.use("TkAgg")
except ImportError:
    headless = True
    print("Running in headless mode...")

class Main():
    ''' 
    Main class that creates the GUI window, buttons and provides functionality for 
    the buttons to start and stop recording the data and plotting the graph
    '''
    def __init__(self, animated_plot):
        """
        Constructor for GUI,
        Animated plot specifies embedded graph
        """
        # self.anim_started=False
        
        self.saved_files_dir =""
        self.filename=""
        self.start_data_index=0
        self.end_data_index=0
        self.animated_plot = animated_plot

        if not headless:
            self.root = tk.Tk()
            self.root.title("RSSI Strength Plot")

        self.buttons = {
            'graph_button'   :tk.Button(self.root, text="Start Graphing",
                                        command=self.start_graphing),
            'start_recording':tk.Button(self.root, text="Start Recording",
                                        command=self.start_recording),
            'stop_recording' :tk.Button(self.root, text="Stop Recording",
                                        command=self.stop_recording),
            'next_page'      :tk.Button(self.root, text="Time Slicing page"),
        }

        self.pack_method = {
            'next_page' : "right",
        }

        for name, button in self.buttons.items():
           button.pack(side=self.pack_method.get(name))
         
        self.figure = self.animated_plot.fig
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack()

        #States
        self.anim_started=False
        self.graph_started=False

        self.root.mainloop()

    def toggle_graphing(self):
        '''
        Method to start or stop the animation/graphing depending on the current state
        '''
        if self.graph_started:
            self.stop_graphing()
            self.buttons['graph_button'].config(text="Start Graphing")
            self.graph_started=False
        else:
            self.buttons['graph_button'].config(text="Stop Graphing")
            self.graph_started=True
            self.start_graphing()
            
    def start_graphing(self):
        '''
        Method to starts the animation/graphing
        '''
        self.anim_started=self.animated_plot.get_ani_playing()
        self.animated_plot.start_animation()
        self.anim_started = True
         
    def stop_graphing(self):
        '''
        Method to stop the animation, get the current data and store it
        '''
        
        self.anim_started=self.animated_plot.get_ani_playing()
        if self.anim_started:
            self.animated_plot.stop_animation()
            self.anim_started = False

    def start_recording(self):
        '''
        Method to start the animation in the AnimatedPlot object
        '''
        start_data_set = self.animated_plot.get_current_data()
        self.start_data_index=len(self.animated_plot.get_current_data())
        print("starting index", self.start_data_index-1)
        self.animated_plot.start_animation()
        self.anim_started = True
        self.buttons['graph_button'].config(text="Stop Graphing")
        #self.graph_button.config(text="Stop Graphing")
        self.graph_started=True

    def stop_recording(self):
        '''
        Method to stop the animation, get the current data and
        store it in a Pandas DataFrame
        '''
        self.anim_started = False
        data = self.animated_plot.get_current_data()
        self.end_data_index=len(data)-1
        # note for me :A Pandas DataFrame is a two-dimensional data structure that
        # can store data in tabular form (rows and columns). The rows can be
        # labeled and the columns can be named. It is similar to a spreadsheet
        # or a SQL table, and provides powerful and convenient data analysis
        # and manipulation methods.DataFrames can be created from different data
        # sources such as dictionaries, lists, arrays, and more, and can
        # be easily exported to various file formats (e.g., CSV, Excel, JSON, etc.).
        self.data_frame = pd.DataFrame(data[self.start_data_index:self.end_data_index], 
        columns=["Time", "RSSI Value", "Node ID"])
        print("data frame before caling the saving choices", self.data_frame)
        self.saving_choices()

    def save_new_file(self):
        """Saves data to a new file with the format "data-YYYY-MM-DD HH:MM:SS.csv";"""
        self.saved_files_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_files')
        os.makedirs(self.saved_files_dir, exist_ok=True)
        file_path = os.path.join(self.saved_files_dir, "data-" +
                                 str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                 + ".csv")
        self.data_frame.to_csv(file_path, index=False)
        messagebox.showinfo(title=None, message=f"Data saved successfully to {file_path}")

    def append_to_file(self):
        """Open a file dialog to select the file to append to, then save data"""
        file_list = []
        for file in os.listdir():
            if file.endswith(".csv"):
                file_list.append(file)
        # note for me: tkinter.filedialog module provides functions
        # for opening and saving files. It presents the user with a file
        # selection dialog to choose a file or directory on their system
        selected_file = tk.filedialog.askopenfilename(initialdir = ".",
        title = "Select file",filetypes = (("CSV files","*.csv"),))
        if selected_file:
            self.data_frame.to_csv(selected_file, mode='a', header=False, index=False)
            messagebox.showinfo(title="Success",
                message="Data saved successfully to " + selected_file)
        else:
            messagebox.showerror(title="FAILURE",
                message="Data not saved, please check if you have selected a file.")

    def overwrite_file(self):
        """Open a file dialog to select the file to overwrite, then save data"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        directory_path = os.path.join(script_dir, os.pardir, 'saved_files')
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        files = [f for f in os.listdir(directory_path) if f.endswith(".csv")]
        if not files:
            messagebox.showerror("Error! No existing files found")
            return
        file = filedialog.askopenfilename(initialdir=directory_path,
            title="Select file to overwrite", filetypes=(("CSV files", "*.csv"),))
        if not file:
            return
        # confirmation to overwrite it
        if os.path.exists(file):
            confirmed = messagebox.askyesno(title="Confirm overwrite",
                                    message="The file already exists. Do you want to overwrite it?")
            if not confirmed:
                return
        self.data_frame.to_csv(file, index=False)
        messagebox.showinfo(title=None, message="Data saved successfully to " + file)

    def saving_choices(self):
        '''
        Method that creates a new Tkinter window for the user to choose how to
        save the recorded data:
        saving the data in a new file,
        appending it to an existing file,
        or overwriting an existing file.
        '''
        saving_options_window = tk.Toplevel()
        saving_options_window.title("Save Data Options")

        new_file_button =  tk.Button(saving_options_window, text = "Save data in a new file",
                                     command = self.save_new_file)
        append_button =    tk.Button(saving_options_window, text = "Append data to an existing file",
                                     command = self.append_to_file)
        overwrite_button = tk.Button(saving_options_window, text = "Overwrite existing file",
                                     command = self.overwrite_file)

        new_file_button.pack()
        append_button.pack()
        overwrite_button.pack()

if __name__ == "__main__":
    animated_plot= AnimatedPlot(10)
    gui = Main(animated_plot)
    #plt.show()

# if __name__ == "__main__":
#     root = tk.Tk()
#     anim_plot = AnimatedPlot(10)
#     app = Main(anim_plot, root)
#     root.mainloop()
