#make graphs for mazin lab stuff
#22/5/2014 
# Today I made a class. I dunno if this is the best way to do this, but it makes it easy to output different graphs.
# Regardless if this is proper OOP implementation, now I can do normalized, baseline corrected graphs AND untouched graphs
"""
04/09/2014
Coming back to this after a long time. 
This summer I made a dope plotting class that has nice features.
I'm trying to implement it here. 
11/09/2014
I got this to play friendly with my plotting tools! 
Also I got it to do averages as well
"""

import csv
import matplotlib.pyplot as plt 
import numpy as np 
from numpy import random
from graphs import Graphs
#how do you put in optional arguments?

class Lab_Plots(object):
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
			for index,row in enumerate(reader):
				# del row[1] #we don't care about temperature values
				self.master_list.append(row)
			
			names = self.master_list[0]
			self.wellnames = names[1:len(names)+1] #here are all the names for the wells
			# Below I change the names of the wells to the names in the well_dic dictionary
			names = []
			if well_dic != None:
				for index in xrange(0,len(self.wellnames)):
					well_name = self.wellnames[index]
					names.append(well_dic[str(well_name)])
			self.names = names
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
		"""
		Below I construct the arrays (lists) of the average values! 
		"""
		if self.dic != None:
			names1 = list()
			for index, name in enumerate(self.wellnames):
				if self.dic.has_key(name): #don't want time
					names1.append(self.dic[name])
				else:
					pass
			#below I maintain the order of "names1"
			unique_names = list(set(names1))
			averages = []
			for unique in unique_names:
				index_list = []
				for i,name in enumerate(names1):
					if name == unique:
						index_list.append(i)
				average_values = [list() for i in self.y_data[0]]
				for j in index_list:
					for i in xrange(0,len(self.y_data[0])):
						average_values[i].append(self.y_data[j][i])
				for i in xrange(0,len(average_values)):
					average_values[i] = sum(average_values[i])/len(average_values[i])
				averages.append(average_values)
				average_values = []
				index_list=[]
			self.unique_names = unique_names
			self.averages = averages
	
	def graph_no_correct(self,average=False):	
		if average == True:		
			no_correct = Graphs(title=self.title,xlabel="Time in Seconds",ylabel="Absorbance",y_names=self.unique_names)
			fig, ax = no_correct.basic_plot(x_data=self.x_data,y_data=self.averages)
			plt.show()
		elif average == False:
			no_correct = Graphs(title=self.title,xlabel="Time in Seconds",ylabel="Absorbance",y_names=list(self.names))
			fig, ax = no_correct.basic_plot(x_data=self.x_data,y_data=self.y_data)
			plt.show()
	def graph_corrected_normalized(self,average=False):

		if self.dic == None and average == False:
			baseline = raw_input("Which well had the baseline? ")
			for i in xrange(0,len(self.names)):
				if baseline == self.names[i]:
					baseline_number = i 
				else:
					pass
		elif self.dic != None and average == False:
			for index, name in enumerate(self.names):
				if name.lower() == 'baseline':
					baseline_number = index
			new_names = self.names
			new_names.pop(baseline_number)
			baseline_list = self.y_data[baseline_number]
			data = self.y_data
			y_data_baseline = []

		elif self.dic != None and average == True:
			for index, name in enumerate(self.unique_names):
				if name.lower() == 'baseline':
					baseline_number = index
			new_names = self.unique_names
			new_names.pop(baseline_number)
			baseline_list = self.averages[baseline_number]
			data = self.averages
			y_data_baseline = []

		for i in xrange(0,len(data)):
			y_dat = data[i]
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
		

