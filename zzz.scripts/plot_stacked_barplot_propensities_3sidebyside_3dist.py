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
#import scipy.cluster.hierarchy as sch
#from scipy.optimize import opt

def read_file(filename):

    file = open(filename)
    lines = file.readlines()
    file.close()
    m = len(lines)-1
    n = len(lines[0].split(','))-1
    print m,n
    x = scipy.zeros([m,n])#positive values
    labels = []
    i = 0
    legand = []
    for line in lines:
        line = line.strip('\n')
        splitline = line.split(',')
        if (i == 0): 
           legand = splitline[1:n+1]
        else:
           labels.append(splitline[0])
           for ind in range(0,n):
              val = float(splitline[ind+1])
              print val
              x[i-1,ind] =  val
        i = i+1
    
    return legand, labels, x, n, m



if len(sys.argv) != 6:
   print "error:  this program takes 3 input filename and title.  "    
   exit()

filename1     = sys.argv[1]
filename2     = sys.argv[2]
filename3     = sys.argv[3]
title         = sys.argv[4]
disttype      = sys.argv[5]

print "filename1     = " + filename1
print "filename2     = " + filename2
print "filename3     = " + filename3

legands, labels_text, x, n, m = read_file(filename1)
legands2, labels_text2, x2, n2, m2 = read_file(filename2)
legands3, labels_text3, x3, n3, m3 = read_file(filename3)
print legands,legands2,legands3
print x
ind = numpy.arange(m)    # the x locations for the groups
#width = 0.35       # the width of the bars: can also be len(x) sequence
width = 0.2      # the width of the bars: can also be len(x) sequence
gap   = 0.05

dist_vec1 = []
dist_vec2 = []

for i in range(m):
    dist1 = 0
    dist2 = 0
    mandist1 = 0
    mandist2 = 0
    for j in range(n):
        dist1 = dist1 + (x[i,j]-x2[i,j])**2.0
        dist2 = dist2 + (x[i,j]-x3[i,j])**2.0
        mandist1 = mandist1 + math.fabs(x[i,j]-x2[i,j])
        mandist2 = mandist2 + math.fabs(x[i,j]-x3[i,j])
    rmsd1 = (dist1/3)**(1.0/2.0)
    rmsd2 = (dist2/3)**(1.0/2.0)
    dist1 = dist1**(1.0/2.0)
    dist2 = dist2**(1.0/2.0)

    if disttype == 'euc':
      dist_vec1.append(dist1)
      dist_vec2.append(dist2)
    elif disttype == 'man':
      dist_vec1.append(mandist1)
      dist_vec2.append(mandist2)
    elif disttype == 'rmsd':
      dist_vec1.append(rmsd1)
      dist_vec2.append(rmsd2)



fig = pylab.figure(figsize=(8,8))
axis = fig.add_axes([0.1,0.2,0.6,0.3])

#colors = ['r','b','c','y','m']
colors = ['#9933FF','#808080', '#FF9900']

offset1 = scipy.zeros([m])
offset2 = scipy.zeros([m])
offset3 = scipy.zeros([m])
for i in range(n):
    #for j in range(m)
    p1 = plt.bar(ind-width-gap, x[:,i],   width, color=colors[i],label=legands[i], bottom=offset1, edgecolor = "none")
    p1 = plt.bar(ind, x2[:,i],   width, color=colors[i], bottom=offset2, edgecolor = "none")
    p1 = plt.bar(ind+width+gap, x3[:,i],   width, color=colors[i], bottom=offset3, edgecolor = "none")
    offset1 = offset1 + x[:,i]
    offset2 = offset2 + x2[:,i]
    offset3 = offset3 + x3[:,i]
    #print offset1
    pylab.ylabel('propensity')
    pylab.title(title)
    #for j in range(m):
    #    offset1[j,0] = offset1[j,0] + xp[j,i]

#axis = fig.add_axes([0.1,0.4,0.6,0.2])
#offset2 = scipy.zeros([m])
#for i in range(cn):
#    p1 = plt.bar(ind, xn[:,i],   width, color=colors[i],label=legands[i], bottom=offset2, edgecolor = "none")
#    offset2 = offset2 + xn[:,i]
#    #for j in range(m):
#    #    offset2[j,0] = offset2[j,0] + xn[j,i]
#    pylab.title(title)
#    pylab.ylabel('negetive')

xticks_range = []
for i in range(0,m):
    xticks_range.append(i+0.5*width)
    #xticks_range.append(i)

axis.set_xticks(range(0,m))
axis.set_xticks(xticks_range)
axis.set_xticklabels(labels_text)
#axis.set_xlim([0-width,m+width])
axis.set_xlim([0-1,m+1])
axis.set_ylim([0,1])

for i in range(0,m):
    labels = axis.xaxis.get_major_ticks()[i].label
    labels.set_fontsize(6)
    labels.set_rotation('vertical')
#axis.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
axis.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


axis = fig.add_axes([0.1,0.6,0.6,0.2])
p1 = plt.bar(ind-width, dist_vec1,   width)
p1 = plt.bar(ind+width, dist_vec2,   width)
axis.set_xticks(range(0,m))
axis.set_xticks(xticks_range)
axis.set_xticklabels([])
axis.set_xlim([0-1,m+1])
#axis.set_ylim([0,1])
pylab.ylabel(disttype)


fig.show()
fig.savefig(title+'fig.png',dpi=600)



