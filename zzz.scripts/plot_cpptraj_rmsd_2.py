#! /usr/bin/python2.6
## this uses the version of python on sublime 

## This was adapted from the web:
## http://stackoverflow.com/questions/2982929/plotting-results-of-hierarchical-clustering-ontop-of-a-matrix-of-data-in-python

import sys
import copy
import math
import matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running
import scipy
import numpy
import pylab
import matplotlib.pyplot as plt


def read_dat(filename):

   fi = open(filename)
   time = []
   rmsd1 = []
   rmsd2 = []
   #rmsd3 = []
   count = 0
   for line in fi: 
       splitline = line.split()
       if count == 0: # check if frist line
          print line
          lab1 = splitline[1]
          lab2 = splitline[2]
          #lab3 = splitline[3]
          count = 1
          continue
       time.append(int(splitline[0]))
       rmsd1.append(float(splitline[1]))
       rmsd2.append(float(splitline[2]))
       #rmsd3.append(float(splitline[3]))
   #return rmsd1, rmsd2, rmsd3, lab1, lab2, lab3    
   return rmsd1, rmsd2, lab1, lab2     


ZERRO = 0.0


if len(sys.argv) != 3:
   print "error:  this program takes 2 inputs: a filename of a list of rmsd files and a title.  "    
   exit()

filename     = sys.argv[1]
title     = sys.argv[2]

print "file of files     = " + filename

# Import data from matrix file:

file = open(filename)
lines = file.readlines()
N = len(lines)
cmap = plt.cm.get_cmap('hsv', N)
fig = pylab.figure(figsize=(8,8))
axis = fig.add_axes([0.1,0.1,0.8,0.8])
    
i = 0
for line in lines: 
    print line
    rmsdfilename = line.strip()
    #X,Y,Z,labX,labY,labZ = read_dat(rmsdfilename) 
    X,Y,labX,labY = read_dat(rmsdfilename) 
    m = len(X) -1
    print "M = " + str(m)
    im = axis.plot(X,Y,'-o',c=cmap(i))
    i = i + 1
axis.set_xlabel(labX)
axis.set_ylabel(labY)
axis.set_title(title)
    
fig.savefig('rmsd_'+title+'.png',dpi=600)
file.close()
