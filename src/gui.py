"""
This module provides a graphical user interface (GUI) for displaying a dynamic
plot using the Tkinter library and the matplotlib library. It also allows the user to
start and stop recording the data and storing it in a csv file using the options
provided in the GUI. In other words, the data is stored as a Pandas DataFrame and can
be saved in a new file, appended to an existing file or overwritten in an existing
file based on the user's choice.
"""
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import OptionMenu
from functools import partial
import datetime
import os
import pandas as pd
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph import AnimatedPlot
from slice_graph import SliceGraph


HEADLESS = None
try:
    matplotlib.use("TkAgg")
except ImportError:
    HEADLESS = True
    print("Running in headless mode...")

class Main():
    '''
    Main class that creates the GUI window, buttons and provides functionality for
    the buttons to start and stop recording the data and plotting the graph
    '''
    def __init__(self, anim_plot):
        """
        Constructor for GUI,
        Animated plot specifies embedded graph
        """

        # self.animated_plot = AnimatedPlot(interface="serial")

        # if self.animated_plot.get_serial_interface() is None:
        #     self.animated_plot = AnimatedPlot(interface="mock")
        #     self.serial_mock_button.config(text="Switch to Serial Mode")
        #     print("switched to mock")
        #     self.interface_version = "mock"
        # else:
        #     self.serial_mock_button.config(text="Switch to Mock Mode")
        #     self.interface_version = "serial"

        self.data_indices = {
            "start_data_index" : 0,
            "end_data_index"   : 0,
        }

        self.window_data = {
            'animated_plot' : anim_plot,
            'interface_version' : None,
        }

        if not HEADLESS:
            self.root = tk.Tk()
            self.root.title("RSSI Strength Plot")

        self.buttons = {
            'graph_button'          :tk.Button(self.root, text="Toggle Graphing",
                                        command=self.toggle_graphing),
            'start_recording'       :tk.Button(self.root, text="Start Recording",
                                        command=self.start_recording),
            'stop_recording'        :tk.Button(self.root, text="Stop Recording",
                                        command=self.stop_recording),
            'next_page'      :tk.Button(self.root, text="Time Slicing page"),
            'serial_mock_button' :tk.Button(self.root, text="---",
                                            command=self.switch_serial_mock),
            "slicing_window_button" :tk.Button(self.root, text="Time Slicing",
                                                command = self.open_slice_window)
        }

        for button in self.buttons.values():
            button.pack()

        self.window_data['figure'] = self.window_data['animated_plot'].fig
        self.window_data['canvas'] = FigureCanvasTkAgg(self.window_data['figure'], self.root)
        self.window_data['canvas'].get_tk_widget().pack()

        #checks if serial works and if not then a mock is brought up
        if self.window_data["animated_plot"].get_serial_interface() is None:
            self.window_data["animated_plot"] = AnimatedPlot(interface="mock")
            self.buttons["serial_mock_button"].config(text="Switch to Serial Mode")
            print("switched to mock")
            self.window_data["interface_version"] = "mock"
        else:
            self.buttons["serial_mock_button"].config(text="Switch to Mock Mode")
            self.window_data["interface_version"] = "serial"
        # Set-up for slice window
        self.slice_canvas = None

        #std deviation text box
        self.standard_deviation_text_box = tk.Text(self.root, height = 3, width = 40)
        self.standard_deviation_text_box.pack()
        self.updating_standard_deviation()

        #adds pop up when window is closed
        #to make sure the user wants to exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.data_frame = pd.DataFrame()

        self.root.mainloop()

    def toggle_graphing(self):
        '''
        Method to start or stop the animation/graphing depending on the current state
        '''
        self.window_data['animated_plot'].toggle_pause()
        #if self.graph_started:
        #    self.stop_graphing()
        #    self.buttons['graph_button'].config(text="Start Graphing")
        #    self.graph_started=False
        #else:
        #    self.buttons['graph_button'].config(text="Stop Graphing")
        #    self.graph_started=True
        #    self.start_graphing()

    def start_graphing(self):
        '''
        Method to starts the animation/graphing
        '''
        #self.anim_started=self.animated_plot.get_ani_playing()
        self.window_data['animated_plot'].start_animation()
        #self.anim_started = True

    def stop_graphing(self):
        '''
        Method to stop the animation, get the current data and store it
        '''
        self.window_data['animated_plot'].stop_animation()
        #self.anim_started=self.animated_plot.get_ani_playing()
        #if self.anim_started:
        #    self.animated_plot.stop_animation()
        #    self.anim_started = False

    def start_recording(self):
        '''
        Method to start the animation in the AnimatedPlot object
        '''
        self.data_indices['start_data_index']=len(
            self.window_data['animated_plot'].get_current_data()
        )
        print("starting index", self.data_indices['start_data_index']-1)
        self.window_data['animated_plot'].start_animation()
        self.buttons['graph_button'].config(text="Stop Graphing")
        #self.graph_button.config(text="Stop Graphing")
        #self.graph_started=True

    def stop_recording(self):
        '''
        Method to stop the animation, get the current data and
        store it in a Pandas DataFrame
        '''
        self.window_data['animated_plot'].stop_animation()
        data = self.window_data['animated_plot'].get_current_data()
        self.data_indices['end_data_index']=len(data)-1
        # note for me :A Pandas DataFrame is a two-dimensional data structure that
        # can store data in tabular form (rows and columns). The rows can be
        # labeled and the columns can be named. It is similar to a spreadsheet
        # or a SQL table, and provides powerful and convenient data analysis
        # and manipulation methods.DataFrames can be created from different data
        # sources such as dictionaries, lists, arrays, and more, and can
        # be easily exported to various file formats (e.g., CSV, Excel, JSON, etc.).
        self.data_frame = pd.DataFrame(
            data[self.data_indices['start_data_index']:self.data_indices['end_data_index']],
            columns=["Time", "RSSI Value", "Node ID"]
        )
        print("data frame before caling the saving choices", self.data_frame)
        self.saving_choices()

    def save_new_file(self):
        """Saves data to a new file with the format "data-YYYY-MM-DD HH:MM:SS.csv";"""
        saved_files_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_files')
        os.makedirs(saved_files_dir, exist_ok=True)
        file_path = os.path.join(saved_files_dir, "data-" +
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

        new_file_button =  tk.Button(saving_options_window, text="Save data in a new file",
                                     command = self.save_new_file)
        append_button =    tk.Button(saving_options_window, text="Append data to an existing file",
                                     command = self.append_to_file)
        overwrite_button = tk.Button(saving_options_window, text="Overwrite existing file",
                                     command = self.overwrite_file)

        new_file_button.pack()
        append_button.pack()
        overwrite_button.pack()

    def switch_serial_mock(self):
        """Switches between mock mode and serial mode"""
        if self.window_data["interface_version"] == "mock":
            self.window_data["serial_mock_button"].config(text = "Switch to Serial Mode")
            self.window_data["animated_plot"]  = AnimatedPlot(interface="serial")
            self.window_data["canvas"]  = FigureCanvasTkAgg(self.animated_plot.fig, self.root)
        elif self.window_data["interface_version"] == "serial":
            self.window_data["serial_mock_button"].config(text = "Switch to Mock Mode")
            self.window_data["animated_plot"]  = AnimatedPlot(interface="mock")
            self.window_data["canvas"] = FigureCanvasTkAgg(self.animated_plot.fig, self.root)

    def port_selection_dropdown(self):
        """Allows user to select a port they want to use"""
        interface = self.window_data["animated_plot"].get_serial_interface()
        if interface :
            port_list = interface.get_port_list()
            dropdown = OptionMenu(self.root, default = None, *port_list)
            dropdown.pack()

    def open_slice_window(self):
        """Function to create slice window. Asks user for 
        filename [csv] from which the slice should be taken"""
        # Set the root and get filename from user
        root = self.root

        while True:
            filename = filedialog.askopenfilename() # Ask for csv to take slice from
            if not(filename.endswith(".csv")) or filename is None:
                messagebox.showerror("Wrong File Type!", "Wrong File Type! \
                                     Please choose a csv file.")
            else:
                break

        # Opens and focuses on the slice window
        slice_window = tk.Toplevel(root)
        # Dictionary that holds all frames
        frame_dict = {
            "graph_frame" : tk.Frame(slice_window),
            "button_frame" : tk.Frame(slice_window),
        }
        # Packs frames which are necessary for easier visual formatting
        for frame in frame_dict.values():
            frame.pack()

        # Setup for the Slice Window
        slice_window.title("Slice")
        slice_window.geometry("500x500")
        slice_window.focus()

        def take_slice(slice_graph, start_entry, end_entry) -> None:
            """Helper function to take a slice for slice_button"""
            # Clean the canvas so it can be redrawn
            self.slice_canvas.get_tk_widget().pack_forget()
            # Get the string in first and second entry
            time_strings = {
                "start_time_str" : start_entry.get(),
                "end_time_str" : end_entry.get()
            }
            slice_graph.make_slice(time_strings["start_time_str"], time_strings["end_time_str"])
            # Redraw and repack
            self.slice_canvas = FigureCanvasTkAgg\
                (figure = slice_graph.get_plot_fig(), master = frame_dict["graph_frame"])
            self.slice_canvas.get_tk_widget().pack()

        def save_slice(slice_graph) -> None:
            """Takes current slice data and saves as csv, called by Save Slice button"""
            file = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
            data = slice_graph.get_data_frame()
            data = data.to_csv(index = False)
            file.write(data)
            file.close()

        # Creates an instance of SliceGraph class
        slice_graph = SliceGraph(filename)
        if slice_graph.get_data_frame() is None:
            slice_window.destroy()
        # Variable for storing the maximum/end time of the graph
        end_time = slice_graph.get_max_time()
        self.slice_canvas = FigureCanvasTkAgg\
            (figure = slice_graph.get_plot_fig(), master = frame_dict["graph_frame"])
        self.slice_canvas.get_tk_widget().pack()

        # Creation and positioning of slice and save slice buttons and user entry fields
        labels_entries={
            "start_time_label" : tk.Label(frame_dict["button_frame"], text="Start time"),
            "start_entry" : tk.Entry(frame_dict["button_frame"]),
            "end_time_label" : tk.Label(frame_dict["button_frame"], text="End time"),
            "end_entry" : tk.Entry(frame_dict["button_frame"])
        }

        for element in labels_entries.values():
            element.pack(side=tk.LEFT)

        labels_entries["start_entry"].insert(0, "0")
        labels_entries["end_entry"].insert(0, f"{end_time}")

        # Creates partial of take_slice and save slice, so params can be included in button call
        partials = {
            "take_slice_partial" : partial(take_slice, slice_graph, labels_entries["start_entry"],
                                           labels_entries["end_entry"]),
            "save_slice_partial" : partial(save_slice, slice_graph)
        }
        buttons_slice = {
            "slice_button"      : tk.Button(frame_dict["button_frame"], text="Take a Slice",
                                            command=partials["take_slice_partial"]),
            "save_slice_button" : tk.Button(frame_dict["button_frame"], text="Save a Slice",
                                            command=partials["save_slice_partial"]),
        }

        for button in buttons_slice.values():
            button.pack(side=tk.LEFT)

    def __str__(self):
        return "GUI"

    def updating_standard_deviation(self):
        """A live updating standard deviation of every node"""
        node_dictionary = self.window_data["animated_plot"].get_node_dict()
        self.standard_deviation_text_box.delete(1.0, tk.END)
        self.standard_deviation_text_box.insert(tk.END, "Standard Deviation:\n")
        std_text=""
        for node in node_dictionary.keys():
            std_text+=node+ ": "+str(self.window_data["animated_plot"].get_std_dev(node))+'\n'

        self.standard_deviation_text_box.insert(tk.END, std_text)

        self.standard_deviation_text_box.after(100, self.updating_standard_deviation)

    def on_closing(self):
        """Checks if you want to quit the program"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            sys.exit(0)

if __name__ == "__main__":
    animated_plot= AnimatedPlot(10)
    gui = Main(animated_plot)
    #plt.show()
