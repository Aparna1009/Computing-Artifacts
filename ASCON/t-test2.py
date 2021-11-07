#!/usr/bin/python
#This scripts takes raw power trace and calculates the t value for each traces sample wise
import math
import numpy
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import argparse

# Parameters ########
start_ylim = -40
end_ylim = 40
start_xlim = 0
end_xlim = 12000
#####################

#load trace file
#use simple array first
#samples_per_trace = 25000
num_of_traces = 999
#raw_traces0 = numpy.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
#raw_traces1 = numpy.array([[13,24,35,45],[15,61,71,18],[19,110,131,12]])

	
def get_mean(raw_traces):
#Takes trace array (each row is a trace)
#returns a one dimention array with each elemen = the mean of a column of the input 
   mean_array = []
   for sample_no in range(0, samples_per_trace):
      sum = 0
      for trace_no in range(0, num_of_traces):
         sum += raw_traces[trace_no,sample_no]
      mean_array.append(sum/num_of_traces)

   return mean_array


def get_variance(raw_traces, mean_array):
#Takes trace array (each row is a trace)
#returns a one dimention array with each element = the variance of a column of the input 
   var_array = []
   for sample_no in range(0, samples_per_trace):
      sum = 0
      for trace_no in range(0, num_of_traces):
         sum += (raw_traces[trace_no,sample_no] - mean_array[sample_no])**2
      var_array.append(float(sum)/num_of_traces)

   return var_array


def get_t_values(mean_array0, var_array0, mean_array1, var_array1, num_of_traces):
#funtion takes the mean and variance arays and
#calcualtes the t-values (one dimenional array)
   t_array = []
   n0 = num_of_traces
   n1 = num_of_traces
   for i in  range(0, samples_per_trace):
      m0 = mean_array0[i]
      m1 = mean_array1[i]
      s0 = var_array0[i]
      s1 = var_array1[i]
      t = (m0 - m1) / math.sqrt( (s0/n0) + (s1/n1))
      t_array.append(t)
   return t_array


parser = argparse.ArgumentParser()
parser.add_argument("trace_file0", help=".npy file that store traces as MxN Nupmy array", type=str)
parser.add_argument("trace_file1", help=".npy file that store traces as MxN Nupmy array", type=str)
parser.add_argument("plot_file", help="File name to store the output figure", type=str)
args = parser.parse_args()
trace_file0 = args.trace_file0
trace_file1 = args.trace_file1
plot_file = args.plot_file
   
   
raw_traces0 = numpy.load(trace_file0)
raw_traces1 = numpy.load(trace_file1)
#num_of_traces = raw_traces0.shape[0]
samples_per_trace = raw_traces0.shape[1]
#print "num_of_traces=", num_of_traces
print "samples_per_trace=", samples_per_trace
mean_array0 =  get_mean(raw_traces0)
mean_array1 =  get_mean(raw_traces1)
var_array0 = get_variance(raw_traces0, mean_array0)
var_array1 = get_variance(raw_traces1, mean_array1)
t_array = get_t_values(mean_array0,var_array0, mean_array1, var_array1, num_of_traces)
#fig1 = plt.figure()
#fig1.plot(mean_array0)
#fig1.savefig('mean0.png')
#plt.plot(mean_array1)
#plt.plot(var_array0)
#plt.plot(var_array1)
threshold = [4.5] * samples_per_trace
minus_threshold = [-4.5] * samples_per_trace
plt.plot(threshold, color='b')
plt.plot(minus_threshold, color='b')

plt.ylim(start_ylim, end_ylim)
plt.xlim(start_xlim, end_xlim)
plt.xlabel("Sample No.")
plt.ylabel("t-value")
plt.plot(t_array, color='r')
#plt.show()
plt.savefig(plot_file)
###
numpy.save("t-values.npy", numpy.array(t_array).transpose()) ##need to get one row array
####
