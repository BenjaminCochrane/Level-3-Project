"""
Data Mocking as a class
"""

import os

import pandas as pd

class Mock():
    """Class to mock data for graph"""

    def __init__(self):
        """Constructor function for Mock class,
        try/except block accounts for local testing and Docker testing"""

        try:
            path = os.path.abspath(os.path.join(os.path.dirname('data.csv'),'data.csv'))
            self.data = pd.read_csv(path)
        except FileNotFoundError:
            path = os.path.abspath(os.path.join(os.path.dirname('data.csv'),'..','data.csv'))
            self.data = pd.read_csv(path)

        self.counter = 0
        self.count = self.data.count().min()
        self.data = self.data[0:self.data.count().min()]

    def get_latest(self) -> tuple:
        """Returns a tuple containing the nodeID , time (x) , and RSSI (y)"""

        node_id = self.__class__.__name__
        time = self.data["Time"][min(self.counter, self.count-1)]
        sensor = self.data["Diff"][self.counter % self.count]
        self.counter += 1
        if self.counter > self.count:
            time += (self.counter-self.count) * self.data["Time"][0]
        return (float(time),float(sensor),node_id)

    def __str__(self):
        """Return data as a string"""
        return repr(self.data)

if __name__ == "__main__":
    a = Mock()
    print(a.get_latest())
