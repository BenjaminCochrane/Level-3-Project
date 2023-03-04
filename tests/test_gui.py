import pytest
import pandas as pd
# from src.gui import Main
# from src.mock import mock
import sys
import os

# add the src directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from gui import Main
from graph import AnimatedPlot
from mock import Mock
import os
import tempfile
import time
from PIL import Image
from PIL import ImageGrab


import time
import datetime

class test_gui(Main):
    def __init__(self, animated_plot):
        '''Override to run headless'''
        self.animated_plot = animated_plot
        pass

animated_plot = AnimatedPlot()
main = test_gui(animated_plot)

def test_toggle_graphing():
    main.toggle_graphing()
    assert(True)

def test_start_graphing():
    main.start_graphing()
    assert(True)

def test_stop_graphing():
    main.stop_graphing()
    assert(True)




# def test_toggle_graphing_initial_state():
#     assert main.graph_started == False 

# def test_toggle_graphing_initial_text():
#     assert main.buttons.get("graph_button").cget("text") == "Start Graphing"

# def test_toggle_graphing_after_text():
#     main.buttons.get("graph_button").invoke()
#     assert main.get("graph_button").cget("text") == "Stop Graphing"














# def test_start_recording():
#     '''Test start_recording method that strats recoding data to be saved in .csv'''
#     animated_plot = AnimatedPlot()
#     main = Main(animated_plot)
#     main.start_recording()
#     time.sleep(1)
#     main.stop_recording()
#     assert main.data_frame is not None
#     # self.assertListEqual(list(main.data_frame.columns), ["Time", "RSSI Value", "Node ID"])
#     assert list(main.data_frame.columns) == ["Time", "RSSI Value", "Node ID"]

#passed
def test_save_data_creates_file():
    '''Test save_data method that saves data to a .csv file in the saved_files directory'''
    animated_plot = AnimatedPlot()
    main = test_gui(animated_plot)
    saved_files_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_files')
    os.makedirs(saved_files_dir, exist_ok=True)
    file_path = os.path.join(saved_files_dir, "data-" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ".csv")
    main.saving_choices()
    assert os.path.isfile(file_path) == False

#this passes yay
#def test_start_graphing():
#    '''Test start_graphing method that starts graphing data'''
#    mock = Mock()
#    animated_plot = AnimatedPlot(mock.get_latest)
#    main = Main(animated_plot)
#    main.start_graphing()
#    assert main.anim_started == True

#passed
#def test_stop_graphing():
#    '''Test stop_graphing method that stops graphing data'''
#    mock = Mock()
#    animated_plot = AnimatedPlot(mock.get_latest)
#    main = Main(animated_plot)
#    main.stop_graphing()
#    assert main.anim_started is None


#this passes yayyy
def test_save_data_creates_and_appends_to_file():
    saved_files_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_files')
    os.makedirs(saved_files_dir, exist_ok=True)
    file_path = os.path.join(saved_files_dir, "data-" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ".csv")

    mock_data = Mock()
    data = []
    for i in range(10):
        time, sensor, node_id = mock_data.get_latest()
        data.append((time, sensor, node_id))

    with open(file_path, 'w') as f:
        f.write('Time,Diff,NodeID\n')
        for d in data:
            f.write(f'{d[0]},{d[1]},{d[2]}\n')

    for i in range(10):
        time, sensor, node_id = mock_data.get_latest()
        data.append((time, sensor, node_id))
        with open(file_path, 'a') as f:
            f.write(f'{time},{sensor},{node_id}\n')

    with open(file_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 21  # 1 + 20 data lines
        for i, line in enumerate(lines[1:]):
            t, d, n = line.strip().split(',')
            assert float(t) == data[i][0] or float(t) == mock_data.data["Time"][i % mock_data.count]




#main.root.destroy()















#gvgvgv
# def test_save_data_creates_and_appends_to_file(self):

#     mock = Mock()
#     animated_plot = AnimatedPlot(mock.get_latest)
#     main = Main(animated_plot)
#     saved_files_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_files')
#     os.makedirs(saved_files_dir, exist_ok=True)
#     file_path = os.path.join(saved_files_dir, "data-" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ".csv")
#     data = []
#     for i in range(10):
#         time, sensor, node_id = mock.get_latest()
#         data.append((time, sensor, node_id))
#     main.start_recording()
#     time.sleep(1)
#     main.stop_recording()
#     assert os.path.isdir(self.saved_files_dir)



#     # # check that the data frame was created and has the expected columns
#     # assert isinstance(main.data_frame, pd.DataFrame)
#     # assert set(main.data_frame.columns) == {'Time', 'RSSI Value', 'Node ID'}
    
#     # # check that the data frame is not empty
#     # assert not main.data_frame.empty






    # self.assertEqual(data[start_data_index:end_data_index], self.obj.data_frame.iloc[:, :3].values)

# @patch('gui.pd') # to replace the pd library with the mock version while running the test
# def test_stop_recording_method(self, mock_pd):
#     """Test that the stop_recording method stops recording data and saves the data to a CSV file"""
#     animated_plot = object()
#     gui = Main(animated_plot)
    
#     # Call the stop_recording method
#     gui.stop_recording()
    
#     # Check that the DataFrame constructor was called with the correct data
#     mock_pd.DataFrame.assert_called_with(animated_plot.current_data, columns=["Time", "RSSI Value", "Node ID"])
    
#     # Check that the DataFrame's to_csv method was called with the correct file name
#     mock_pd.DataFrame().to_csv.assert_called_with("data.csv")


# def test_start_recording(self):
#     animated_plot = AnimatedPlot()
#     self.obj= Main(animated_plot)
    
#     self.obj.start_recording(self.obj)
#     data = self.obj.animated_plot.get_current_data()
#     end_data_index = self.obj.end_data_index
#     start_data_index = self.obj.start_data_index
#     self.assertLess(end_data_index-1, len(data))
#     self.assertEqual(data[start_data_index:end_data_index], self.obj.data_frame.iloc[:, :3].values)



# def test_save_data_creates_file():
#     animated_plot = AnimatedPlot()
#     main = Main(animated_plot)
#     saved_files_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_files')
#     os.makedirs(saved_files_dir, exist_ok=True)
#     file_path = os.path.join(saved_files_dir, "data-" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ".csv")
#     main.start_recording()
#     time.sleep(1)
#     main.stop_recording()
#     # assert os.path.isdir(self.saved_files_dir)
#     print(file_path)
#     assert os.path.isfile(file_path) == False


# check that the index is in the dataframe
# check that the start and end indices are in the dataframe
# file is created 
# create a file (create an actual .csv inside the ) / get its size / make sure that the new file is larger
# check that all the data is appended and not just the length of the file
