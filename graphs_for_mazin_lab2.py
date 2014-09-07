#make graphs for mazin lab stuff
#22/5/2014 
# Today I made a class. I dunno if this is the best way to do this, but it makes it easy to output different graphs.
# Regardless if this is proper OOP implementation, now I can do normalized, baseline corrected graphs AND untouched graphs
"""
04/09/2014
Coming back to this after a long time. 
This summer I made a dope plotting class that has nice features.
I'm trying to implement it here. 
"""
import csv
import matplotlib.pyplot as plt 
import numpy as np 
from numpy import random
from plotting_tools import Graphs
#how do you put in optional arguments?

class Plots(object):
	def __init__(self, name_of_file,well_dic=None,title='ThT Assay'):
		"""
		Name of file is the .csv file in question
		well_dic is a python dictionary connecting the name of the wells to 
		the contents of the well
		"""
		self.title = title
		self.dic = well_dic
		self.name = str(name_of_file)
		self.colors = [] #declaring these as global variables that I can use over and over
		self.master_list = []
		self.list_of_lists = []
		with open(self.name, 'rU') as csvfile: #'rU' is universal file something or other
			reader = csv.reader(csvfile)
			for row in reader:
				# del row[1] #we don't care about temperature values
				self.master_list.append(row)
			
			names = self.master_list[0]
			self.names = names[1:len(names)+1] #here are all the names for the wells

			# Below I change the names of the wells to the names in the well_dic dictionary
			if well_dic != None:
				for index in xrange(0,len(self.names)):
					well_name = self.names[index]
					self.names[index] = well_dic[str(well_name)]

			for j in xrange(0,len(self.names)+1):
				self.list_of_lists.append([])
			for j in xrange(0,len(self.names)+1):
				for i in xrange(1,len(self.master_list)):
					row = self.master_list[i]
					dummy = self.list_of_lists[j] #cause I don't think you can do list1[i].append()
					if j == 0:
						time = row[j]
						time1 = time.split(":")
						dummy1 = 0
						for h in xrange(0,len(time1)-1):
							dummy1 += float(time1[h])*(60**(len(time1)-1-h))
						dummy.append(dummy1)
						dummy1 = 0
					else:
						dummy.append(float(row[j]))

		self.x_data = self.list_of_lists[0] #time data
		y_data = []

		for i in xrange(1, len(self.names)+1):
			y_data.append(self.list_of_lists[i])
		self.y_data = y_data
					
	def graph_no_correct(self):

		no_correct = Graphs(title=self.title,xlabel="Time in Seconds",ylabel="Absorbance",y_names=list(self.names))
		fig, ax = no_correct.basic_plot(x_data=self.x_data,y_data=self.y_data)
		plt.show()
	
	def graph_corrected_normalized(self):

		if self.dic == None:
			baseline = raw_input("Which well had the baseline? ")
			for i in xrange(0,len(self.names)):
				if baseline == self.names[i]:
					baseline_number = i 
				else:
					pass
		elif self.dic != None:
			for index, name in enumerate(self.names):
				if name.lower() == 'baseline':
					baseline_number = index
		new_names = self.names
		new_names.pop(baseline_number)
	
		baseline_list = self.y_data[baseline_number]

		y_data_baseline = []

		for i in xrange(0,len(self.y_data)):
			y_dat = self.y_data[i]
			if i == baseline_number:
				pass
			else: 
				for j in xrange(0,len(y_dat)):
					y_dat[j] = y_dat[j] - baseline_list[j]
				y_data_baseline.append(y_dat)

		y_data_normalized = []

		for i in xrange(0,len(y_data_baseline)):
			y_dat = y_data_baseline[i]
			normalizer = y_dat[0]
			for j in xrange(0,len(y_dat)):
				y_dat[j] = y_dat[j] - normalizer
			y_data_normalized.append(y_dat)
			
		no_correct = Graphs(title=self.title,xlabel="Time in Seconds",ylabel="Absorbance",y_names=new_names)
		fig, ax = no_correct.basic_plot(x_data=self.x_data,y_data=y_data_normalized)
		plt.show()
		

dic1 = {
	'G9':'Baseline',
	'A11':"Abeta low concentration",
	'A12':"p53 low concentration",
	'B11':"Abeta high concentration",
	'B12':"p53 high concentration",
}
example = Plots('10-4.csv',well_dic=dic1,title="ThT Assay 10-4-2014, PBS only")

# example.graph_no_correct()
example.graph_corrected_normalized()
# example.graph_corrected_normalized()
#example.graph_no_correct()