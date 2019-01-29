#! /usr/bin/python2.6
## this uses the version of python on sublime 

## This was adapted from the web:
## http://stackoverflow.com/questions/2982929/plotting-results-of-hierarchical-clustering-ontop-of-a-matrix-of-data-in-python

import sys
import copy
import math
import matplotlib
import scipy
import numpy
import pylab
import matplotlib.pyplot as plt


def read_dat(filename):

   fi = open(filename)
   time = []
   rmsd1 = []
   rmsd2 = []
   rmsd3 = []
   count = 0
   for line in fi: 
       splitline = line.split()
       if count == 0: # check if frist line
          print line
          lab1 = splitline[1]
          lab2 = splitline[2]
          lab3 = splitline[3]
          count = 1
          continue
       time.append(int(splitline[0]))
       rmsd1.append(float(splitline[1]))
       rmsd2.append(float(splitline[2]))
       rmsd3.append(float(splitline[3]))
   return rmsd1, rmsd2, rmsd3, lab1, lab2, lab3    


ZERRO = 0.0


if len(sys.argv) != 3:
   print "error:  this program takes 2 inputs: a filename of a list of rmsd files and a title.  "    
   exit()

filename     = sys.argv[1]
title     = sys.argv[2]
xlim      = [-0.1, 4.1]
ylim      = [-0.1, 4.1]

print "file of files     = " + filename

# Import data from matrix file:

file = open(filename)
lines = file.readlines()
N = len(lines)
cmap = plt.cm.get_cmap('hsv', N)
fig = pylab.figure(figsize=(8,8))
axis1 = fig.add_axes([0.1,0.1,0.3,0.3])
axis2 = fig.add_axes([0.1,0.5,0.3,0.3])
axis3 = fig.add_axes([0.5,0.1,0.3,0.3])
axis4 = fig.add_axes([0.5,0.5,0.3,0.3])
    
i = 0
for line in lines: 
    print line
    rmsdfilename = line.strip()
    X,Y,Z,labX,labY,labZ = read_dat(rmsdfilename) 
    m = len(X) -1
    print "M = " + str(m)
    im = axis1.plot(X,Y,'-o',c=cmap(i))
    im = axis2.plot(X,Z,'-o',c=cmap(i))
    im = axis3.plot(Y,Z,'-o',c=cmap(i))
    i = i + 1
axis1.set_xlabel(labX)
axis1.set_ylabel(labY)
axis1.set_xlim(xlim)
axis1.set_ylim(ylim)
axis1.set_title(title)
axis2.set_xlabel(labX)
axis2.set_ylabel(labZ)
axis2.set_xlim(xlim)
axis2.set_ylim(ylim)
axis3.set_xlabel(labY)
axis3.set_ylabel(labZ)
axis3.set_xlim(xlim)
axis3.set_ylim(ylim)
    
fig.savefig('rmsd_'+title+'.png',dpi=600)
file.close()
