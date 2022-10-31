"""
Data Mocking as a class
"""

import pandas as pd

class Mock():
	def __init__(self):
		"""Constructor function for Mock class"""

		self.data = pd.read_csv("../data.csv")
		self.counter = 0
		self.data = self.data[0:self.data.count().min()]

	def get_latest(self) -> tuple:
		"""Returns a tuple containing the nodeID , time (x) , and RSSI (y)"""

		nodeID = self.__class__.__name__
		x = self.data["Time"][self.counter]
		y = self.data["Sensor"][self.counter]
		self.counter += 1
		return (x,y,nodeID)
	
	def __str__(self):
		"""Return data as a string"""
		return repr(self.data)

if __name__ == "__main__":
	a = Mock()
	print(a.get_latest())