import os
import numpy as np 
import pandas as pd 

class CSVReader(object):
	def __init__(self, datafile):
		self.datafile = datafile

		# strcols = ['gender', 'hand dominant', 'center']

	def loadcsv(self):
		data = pd.read_csv(self.datafile)

		# first off convert all columns to lower case
		data.columns = map(str.lower, data.columns)

		# loop through columns and cast to lowercase if they are strings
		# ASSUMING: no columns have mixed numbers / strings
		for col in data:
		    try:
		        data[col] = data[col].str.lower()
		    except AttributeError as e:
	        	print(col, " has an attribute error when casting to strings.")

		self.data = data
		return data

	def loadcsv_aslist(self):
	    data = np.genfromtxt(self.datafile, delimiter=',', 
	    	skip_header=1, converters={0: lambda s: str(s)})
	    return data.tolist()

	def _map_colvals(self):
		pass
		# self.data.replace('N/A')

