

import sys
import copy

import math

import matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running

import scipy, pylab, numpy
from matplotlib import cm


## Writen by Trent Balius, 2019 


def read_rmsd_dat_file(filehandel):
    # si is the user specified i value
    # sj is the user specified j value
    rmsd = []
    time = []
    for line in filehandel:
        if "Frame" in line: 
            continue
        splitline = line.strip().split()
        time.append(float(splitline[0]))
        rmsd.append(float(splitline[1]))
    return rmsd, time



#def heatmap(Mat,label,filename,threshold,heatmap_threshold):
def make_plot(val_array,time_array,title,filename):

     print "Here in make_plot"
     fig = pylab.figure(figsize=(8,8))

     minv = min(val_array)
     maxv = max(val_array)
     if (minv !=0.0): 
         print("Error, min cluster name should be 0")
         exit()
     count = []
     dE = []
     for i in range(0,int(maxv)+1):
         count.append(0)
         dE.append(0.0)
     for v in val_array:
         count[int(v)] = count[int(v)] + 1

     Kb=0.001985875; # kcal/mol/kelvin
     temp=298.15; # Kelvin

     for i in range(0,int(maxv)+1):
         dE[i] = Kb*temp*math.log(float(count[0])/float(count[i]))
         

     ax1 = fig.add_axes([0.1,0.1,0.4,0.4])
     #matplotlib.pyplot.plot(time_array,val_array,'k.') # draws a datshed line where dendogram is cut.
     cmapval = cm.get_cmap('rainbow', max(val_array))
     #ax1.scatter(time_array,val_array,c=val_array,cmap=cmapval,marker='.') #,[0,100],[0,100],'--')
     ax1.bar(range(0,int(maxv)+1),count) #,[0,100],[0,100],'--')
     ax1.set_title(title)
        
     ax2 = fig.add_axes([0.5,0.1,0.4,0.4])
     print int(max(val_array))
     ax2.plot(range(0,int(maxv)+1),dE,'-o')
     ax2.yaxis.tick_right()
     #ax2.set_yticks([])
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

