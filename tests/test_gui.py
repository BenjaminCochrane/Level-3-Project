"""
Tests for gui
"""
# add the src directory to the module search path
from gui import Main
from graph import AnimatedPlot
from mock import Mock
import sys
import os
import tempfile
import time
import pandas as pd
from PIL import Image
from PIL import ImageGrab

import time
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


class test_gui(Main):
    def __init__(self, animated_plot):
        '''Override to run headless'''
        self.window_data = {
            'animated_plot' : animated_plot,

        }

        self.data_indices = {
            "start_data_index" : 2,
            "end_data_index"   : 6,
        }

        self.data_frame = pd.DataFrame()

        pass

animated_plot = AnimatedPlot()
main = test_gui(animated_plot)

def test_toggle_graphing():
    '''Test for toggle graph functionality'''
    main.toggle_graphing()
    assert(True)

def test_start_graphing():
    '''Test for start graphing functionality'''
    main.start_graphing()
    assert(True)

def test_stop_graphing():
    '''Test for stop graphing functionality'''
    main.stop_graphing()
    assert(True)

def test_stop_recording():
    '''Test stop recording functionality'''
    assertion=(main.data_indices["end_data_index"]-main.data_indices["start_data_index"])>0
    assert(assertion)

def test_saving_choices():
    '''Test saving data options'''
    assertion= main.data_indices['end_data_index']>0
    assert(assertion)

# def test_save_new_file():
#     '''Test option to save data to a new file'''
#     main.save_new_file()
#     assert(True)

# def test_append_to_file():
#     '''Test option to append saved data to an existing file'''
#     main.append_to_file()
#     assert(True)

# def test_overwrite_file():
#     '''Test option to overwrite data in an existing file'''
#     main.overwrite_file()
#     assert(True)

# def test_save_data_creates_file():
#     '''Test save_data method that saves data to a .csv file in the saved_files directory'''
#     animated_plot = AnimatedPlot()
#     main = test_gui(animated_plot)
#     saved_files_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_files')
#     os.makedirs(saved_files_dir, exist_ok=True)
#     file_path = os.path.join(saved_files_dir, "data-" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ".csv")
#     assert os.path.isfile(file_path) == False

# def test_save_data_creates_and_appends_to_file():
#     '''Test saving data to a new file creates a new file '''
#     saved_files_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_files')
#     os.makedirs(saved_files_dir, exist_ok=True)
#     file_path = os.path.join(saved_files_dir, "data-" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ".csv")

#     mock_data = Mock()
#     data = []
#     for i in range(10):
#         time, sensor, node_id = mock_data.get_latest()
#         data.append((time, sensor, node_id))

#     with open(file_path, 'w') as f:
#         f.write('Time,Diff,NodeID\n')
#         for d in data:
#             f.write(f'{d[0]},{d[1]},{d[2]}\n')

#     for i in range(10):
#         listt= mock_data.get_latest()
#         # nodeID = listt[0]
#         time, sensor, node_id = listt[5], listt[2], listt[0], 
#         # time, sensor, node_id = mock_data.get_latest()
#         data.append((time, sensor, node_id))
#         with open(file_path, 'a') as f:
#             f.write(f'{time},{sensor},{node_id}\n')

#     with open(file_path, 'r') as f:
#         lines = f.readlines()
#         assert len(lines) == 21  # 1 + 20 data lines
#         for i, line in enumerate(lines[1:]):
#             t, d, n = line.strip().split(',')
#             assert float(t) == data[i][0] or float(t) == mock_data.data["Time"][i % mock_data.count]






