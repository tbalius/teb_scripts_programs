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
import scipy.cluster.hierarchy as sch

ZERRO = 0.0


if len(sys.argv) != 2:
   print "error:  this program takes 1 input xyfilename.  "    
   exit()

xyfilename     = sys.argv[1]

print "xyfilename     = " + xyfilename

# Import data from matrix file:

file = open(xyfilename)
lines = file.readlines()
file.close()


m = len(lines) -1
print "M = " + str(m)

X = scipy.zeros([m,1])
Y = scipy.zeros([m,1])

countline = 0

## X is the Predicted value (sea_dock)
## Y is the accual value (sea)
firstline = True
for line in lines:
    if firstline == True:
       firstline = False
       continue
    line = line.strip('\n')
    splitline = line.split('\t')
    #print splitline
    X[countline] = float(splitline[0]) # FP rate
    Y[countline] = float(splitline[1]) # TP rate
    countline = countline + 1

Xmax = max(X)
Xmin = min(X)
Ymax = max(Y)
Ymin = min(Y)

print Xmax, Xmin 
print Ymax, Ymin

# Plot distance matrix.
fig = pylab.figure(figsize=(8,8))
#axis = fig.add_axes([0.3,0.1,0.6,0.6])
axis = fig.add_axes([0.1,0.1,0.8,0.8])

threshold1 = 50
threshold2 = 0

im = axis.plot(X,Y,'-',[0,100],[0,100],'--')
#im = axis.plot(X,Y,'.',[threshold1,threshold1],[Ymin,Ymax],'-',[Xmin,Xmax],[threshold2,threshold2],'-')
axis.set_xlabel('FP rate')
axis.set_ylabel('TP rate')

axis.set_ylim(-10, 110)
axis.set_xlim(-10, 110)
#axis.set_yticks([])
#axis.set_xticks([])

#fig.show()
fig.savefig('AUC.png',dpi=600)

