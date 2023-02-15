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
import csv

matplotlib.use("TkAgg")

class Main():
    ''' 
    Main class that creates the GUI window, buttons and provides functionality for 
    the buttons to start and stop recording the data and plotting the graph
    '''
    # pylint: disable=too-many-instance-attributes
    # Nine is reasonable in this case.
    def __init__(self, animated_plot):
        self.start_data_index=0
        self.end_data_index=0
        self.animated_plot = animated_plot
        self.root = tk.Tk()
        self.root.title("RSSI Strength Plot")

        self.start_graphing_button = tk.Button(self.root,
                                            text="Start Graphing",
                                            command=self.start_graphing)
        self.start_graphing_button.pack()

        self.stop_graphing_button = tk.Button(self.root, text="Stop Graphing",
                                              command=self.stop_graphing)
        self.stop_graphing_button.pack()
        self.figure = self.animated_plot.fig
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack()

        self.start_recording_button = tk.Button(self.root, text="Start Recording",
                                                command=self.start_recording)
        self.start_recording_button.pack()
        self.stop_recording_button = tk.Button(self.root, text="Stop Recording",
                                                 command=self.stop_recording)
        self.stop_recording_button.pack()
        self.next_page_button = tk.Button(self.root, text="Time Slicing page")
        self.next_page_button.pack(side="right")
        self.root.mainloop()
    def start_graphing(self):
        '''
        Method to starts the animation/graphing
        '''
        self.animated_plot.start_animation()
    def stop_graphing(self):
        '''
        Method to stop the animation, get the current data and store it
        '''
        if self.animated_plot.get_ani_playing():
            self.animated_plot.stop_animation()
    def start_recording(self):
        '''
        Method to start the animation in the AnimatedPlot object
        '''
        start_data_set = self.animated_plot.get_current_data()
        self.start_data_index=len(self.animated_plot.get_current_data())
        print("starting index", self.start_data_index-1)
        #start animation if not started to have something to record
        self.animated_plot.start_animation()

    def stop_recording(self):
        '''
        Method to stop the animation, get the current data and
        store it in a Pandas DataFrame
        '''
        data = self.animated_plot.get_current_data()
        self.end_data_index=(len(data))
        # not for me :A Pandas DataFrame is a two-dimensional data structure that
        # can store data in tabular form (rows and columns). The rows can be
        # labeled and the columns can be named. It is similar to a spreadsheet
        # or a SQL table, and provides powerful and convenient data analysis
        # and manipulation methods.DataFrames can be created from different data
        # sources such as dictionaries, lists, arrays, and more, and can
        # be easily exported to various file formats (e.g., CSV, Excel, JSON, etc.).
        self.data_frame = pd.DataFrame(data[self.start_data_index:self.end_data_index], columns=[  "Time", "RSSI Value", "Node ID"])
        print("data frame before caling the saving choices", self.data_frame)
        self.saving_choices()
    def saving_choices(self):
        '''
        Method that creates a new Tkinter window for the user to choose how to
        save the recorded data:
        saving the data in a new file, appending it to an existing file,
        or overwriting an existing file.
        If the user chooses to save the data in a new file,
        it creates a new file with the format "data-YYYY-MM-DD HH:MM:SS.csv";
        if the user chooses to append the data to an existing file,
        it opens a file dialog to select the file to append to;
        if the user chooses to overwrite an existing file,
        it opens a file dialog to select the file to overwrite.
        '''
        saving_options_window = tk.Toplevel()
        saving_options_window.title("Save Data Options")

        choice = tk.StringVar(value="a")
        a_button = tk.Radiobutton(saving_options_window,
                    text="Save data in a new file", variable=choice, value="a")
        b_button = tk.Radiobutton(saving_options_window,
                    text="Append data to an existing file", variable=choice, value="b")

        c_button = tk.Radiobutton(saving_options_window,
                    text="Overwrite existing file", variable=choice, value="c")

        a_button.pack()
        b_button.pack()
        c_button.pack()
        # from docs: class pandas.DataFrame(data=None, index=None,
        # columns=None, dtype=None, copy=None)
        # data_dict={"Time": [], "RSSI Value": [], "Node ID": []}
        # data_frame = pd.DataFrame(data=data_dict, dtype=None)
        # print()
        def save_data():
            def switch(lang):
                if lang == "a":
                    file_name = "data-" + str(
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ".csv"
                     
                    data=self.data_frame.to_csv(file_name)
                    # with open(file_name, 'w', newline='') as file:
                    #     print(data)
                    #     print(type(data))
                    #     print(len(data))
                    #     writer = csv.writer(file)
                    #     writer.writerows(data)
                    #     #writer.clos

                        # file.write(data) #instead of file
                        # file.close()


                    # data_frame = pd.DataFrame(data_dict)
                    # data_frame.to_csv(file_name, index=False)
                    # note for me: messagebox module displays message boxes
                    # with various types of buttons (e.g. OK, Cancel, Yes, No, etc.).
                    # Can be used to display error messages,
                    # warnings, and other types of information to the user.
                    messagebox.showinfo(title=None,
                    message=  "Data saved successfully to " + file_name)
                     
                    # file.write(data) #instead of file
                    # file.close()

                elif lang == "b":
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
                        self.data_frame.to_csv(selected_file, mode='a', header=False)
                        messagebox.showinfo(title="Success",
                        message="Data saved successfully to " + selected_file)
                    else:
                        messagebox.showerror(title="FAILURE",
                        message="Data not saved, pleease check if you have selected a file.")
                elif lang == "c":
                    # check the list of files in the directory yhat end with .csv
                    files = [f for f in os.listdir() if f.endswith(".csv")]
                    if not files:
                        messagebox.showerror("Error! No existing files found")
                        return
                    # Present this list of files to the user in a dialog
                    # parent - the window to place the dialog on top of
                    # title - the title of the window
                    # initialdir - the directory that the dialog starts in
                    # initialfile - the file selected upon opening of the dialog
                    # filetypes - a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
                    # defaultextension - default extension to append to file (save dialogs)
                    # multiple - when true, selection of multiple items is allowed
                    file = filedialog.askopenfilename(title=
                    "Select which .csv file you would like to overwrite",
                    filetypes=(("CSV files", "*.csv"),), initialdir=".")
                    if not file:
                        return
                    # Finally, save the data to the selected file
                    self.data_frame.to_csv(file, index=False)
                    messagebox.showinfo(title = None,
                    message = "Data saved successfully to " + file)
            switch(choice.get())
            saving_options_window.destroy()
        save_button = tk.Button(saving_options_window, text="Save", command=save_data)
        save_button.pack()
if __name__ == "__main__":
    animated_plot_two = AnimatedPlot(10)
    gui = Main(animated_plot_two)
    plt.show()
