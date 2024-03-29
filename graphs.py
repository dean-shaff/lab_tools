import matplotlib.pyplot as plt
import numpy as np 
from numpy import linalg
from matplotlib import rc
import os
import subprocess
import scipy.stats as stats

class Graphs(object):
	def __init__(self,title=r"Graph of $f\left(x\right)$",xlabel=0,ylabel=0,y_names=None,y_error_names=None):
		self.title = title
		# if title != 0:
		# 	self.title = title
		# else:
		# 	self.title = r"Graph of $f\left(x\right)$"
		if xlabel != 0:
			self.xlabel = str(xlabel)
		else:
			self.xlabel = "$x$"
		if ylabel != 0:
			self.ylabel = str(ylabel)
		else:
			self.ylabel = r"$f\left(x\right)$"
		if y_names != None:
			self.y_names = list(y_names)
		elif y_names == 0:
			pass
		if y_error_names != 0:
			self.y_error_names = str(y_error_names)
		elif y_error_names == 0:
			pass
	def create_figure_logxory(self,x_data,y_data=0,y_lim=[0,0],x_lim=[0,0],xlog=False,ylog=False,error_ydata=0,x_error=0,y_error=0):
		rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
		rc('text', usetex=True)
		x_data = np.array(x_data)
		fig = plt.figure(figsize=(16,8))
		ax = fig.add_subplot(111)
		ax.set_title(self.title,fontsize=24)
		ax.set_xlabel(self.xlabel, fontsize=20)
		ax.set_ylabel(self.ylabel, fontsize=20)
		list_of_color = []
		if y_data != 0:
			increment = float(1/float(len(y_data)+1))
			y_data = list(y_data)
			if len(y_data) == 1:
				plt.plot(x_data,y_data[0],color='g',linewidth=2,label=self.y_names[0])
			elif len(y_data) != 1:
				for i in xrange(1,len(y_data)+1):
					multiplier = float(i*increment)
					r = float(1 - multiplier)
					g = float(0 + multiplier)
					b = float(0.15 + (multiplier)/2)
					color = [r,g,b]
					list_of_color.append(color)
				for i in xrange(0,len(y_data)):
					col = tuple(list_of_color[i])
					y_names_list = self.y_names
					label = str(y_names_list[i])
					plt.plot(x_data,y_data[i],color=col,linewidth=2,label=label)
		#error plotting ===========	
		if x_error != 0:
			x_error = np.array(x_error)
			error_ydata = np.array(error_ydata)
			plt.errorbar(x_data,error_ydata,xerr = x_error,fmt='.',color='k',ecolor='b')
		elif y_error != 0:
			y_error = np.array(y_error)
			error_ydata = np.array(error_ydata)
			ax.errorbar(x_data,error_ydata,yerr=y_error,fmt='.',color='k',ecolor='b',label=self.y_error_names)
		elif y_error != 0 and x_error != 0:
			x_error = np.array(x_error)
			y_error = np.array(y_error)
			error_ydata = np.array(error_ydata)
			ax.errorbar(x_data,error_ydata,xerr=x_error,yerr=y_error,fmt='.',color='k',ecolor='b')
		#==========================
		ax.legend(bbox_to_anchor=(1.1,1.02))
		if y_lim[0] != 0 or y_lim[1] != 0:
			ax.set_ylim(y_lim)
		if x_lim[0] != 0 or x_lim[1] != 0:
			ax.set_xlim(x_lim)
		if xlog == True:
			ax.set_xscale('log')
		if ylog == True:
			ax.set_yscale('log')
		plt.grid(True)
		#plt.show()		
		return fig, ax
	def basic_plot(self,x_data=0,y_data=0,y_lim=[0,0],x_lim=[0,0]):
		rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
		rc('text', usetex=True)
		fig = plt.figure(figsize=(16,8))
		ax = fig.add_subplot(111)
		ax.set_title(self.title,fontsize=20)
		ax.set_xlabel(self.xlabel, fontsize=16)
		ax.set_ylabel(self.ylabel, fontsize=16)
		list_of_color = []	
		if y_data != 0 and x_data != 0:
			y_data = list(y_data)
			increment = float(1.0/float(len(y_data)))
			if len(y_data) == 1:
				plt.plot(x_data,y_data[0],'r.')
			elif len(y_data) > 1:
				# Making colors:
				for i in xrange(1,len(y_data)+1):
					multiplier = float(i*increment)
					r = float(0 + multiplier)
					g = float(1 - multiplier)
					b = float(0.2 + (multiplier)/1.5)
					color = [r,g,b]
					list_of_color.append(color)
				# Making Plots
				for i in xrange(0,len(y_data)):
					col = tuple(list_of_color[i])
					dummy = y_data[i]
					if self.y_names != None:
						plt.plot(x_data,dummy,c=col,linewidth=3,label=self.y_names[i])
					else:
						plt.plot(x_data,dummy,color=col,linewidth=2)

			if y_lim[0] != 0 or y_lim[1] != 0:
				ax.set_ylim(y_lim)
			if x_lim[0] != 0 or x_lim[1] != 0:
				ax.set_xlim(x_lim)
			ax.legend(bbox_to_anchor=(1.1,1.12))
		return fig, ax




