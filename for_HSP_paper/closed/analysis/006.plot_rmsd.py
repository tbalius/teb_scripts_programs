

import sys
import copy

import math

import matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running

import scipy, pylab, numpy as np


## Writen by Trent Balius, 2019 


def read_rmsd_dat_file(filehandel):
    # si is the user specified i value
    # sj is the user specified j value
    rmsd = []
    time = []
    for line in filehandel:
        if "Frame" in line: 
            continue
        if "Res" in line:
	    continue
        splitline = line.strip().split()
        time.append(float(splitline[0])/100)
        rmsd.append(float(splitline[1]))
    return rmsd, time



#def heatmap(Mat,label,filename,threshold,heatmap_threshold):
def make_plot(val_array,time_array,title,filename):

     print "Here in make_plot"
     fig = pylab.figure(figsize=(8,8))

     ax1 = fig.add_axes([0.1,0.1,0.6,0.2])
     matplotlib.pyplot.plot(time_array,val_array,'k-') # draws a datshed line where dendogram is cut.
     ax1.set_title(title)
     ax1.set_xlabel("Time (ns)")
     ax1.set_ylabel("RMSD ($\mathrm{\AA}$)")
        
     ax2 = fig.add_axes([0.75,0.1,0.2,0.2])
     val_weights = np.ones_like(val_array)/len(val_array)
     n1_1, bins, patches = ax2.hist(val_array, normed=False, histtype='bar', weights=val_weights, orientation="horizontal")
     ax2.set_yticks([])
     for tick in ax2.get_xticklabels():
       tick.set_rotation(45)
     #fig.show()
     fig.savefig(filename+'.png',dpi=600)   
     return


def main():
  if len(sys.argv) != 4: # if no input
     print "syntax:  rmsd dat file, title of plot, output prefix"
     print "Error:  you have entered the wrong number of inputs:"
     print len(sys.argv)
     exit()

  print "You have entered in %d inputs:"%(len(sys.argv))
  file1name  = sys.argv[1] 
  title     = sys.argv[2] 
  output    = sys.argv[3] 

  #print "input matrix file prefix = " + file1name+'.'+str(i)
  file1handel = open(file1name,'r')
  rv,tv = read_rmsd_dat_file(file1handel)
  file1handel.close()
  make_plot(rv,tv,title,output)
  return
 
main()

