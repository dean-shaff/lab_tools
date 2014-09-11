import numpy as np

class Stats_Stuff(object):
	def __init__(self,data1,data2):
		self.data1 = list(data1)
		self.data2 = list(data2)
	def chi_squared(self):
		try:
			chi_squared = np.array([(i[0]-i[1])**2 for i in zip(self.data1,self.data2)])
			return float(np.sum(chi_squared))
		except ValueError:
			print("data sets are of unequal length")