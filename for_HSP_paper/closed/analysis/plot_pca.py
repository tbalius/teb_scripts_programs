#! /usr/bin/python2.6
## this uses the version of python on sublime 

## This was adapted from the web:
## http://stackoverflow.com/questions/2982929/plotting-results-of-hierarchical-clustering-ontop-of-a-matrix-of-data-in-python

import matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running
import sys
import copy
import math
import scipy
import numpy
import pylab
#import scipy.cluster.hierarchy as sch
#from scipy.optimize import opt
import scipy.optimize as opt
import scipy.linalg   as la
import scipy.stats    as stats


def read_file(filename):
    print("read in file")
    file = open(filename)
    lines = file.readlines()
    file.close()

    X = []
    Y = []
    firstline = True
    for line in lines:
        if firstline == True:
           firstline = False
           continue
        line = line.strip('\n')
        splitline = line.split()
        frame = int(splitline[0])
        X.append(float(splitline[1]))
        Y.append(float(splitline[2]))
        Z = float(splitline[3])

    Xnew = numpy.ones(len(X))
    Ynew = numpy.ones(len(Y))
    for i in range(len(X)):
       Xnew[i] = X[i]
       Ynew[i] = Y[i]

    return Xnew, Ynew 


# this is the function that we are fiting
def function_fit(parms,xvec):
    l = len(xvec)
    m = parms[0]
    b = parms[1]
    #print l
    yvec = scipy.zeros([l,1])
    for i in range(l):
        yvec[i] = m*xvec[i]+b
        #print yvec[i]
    return yvec

def calc_residuel(parms,xvec,yvec_d):
    # xvec 
    # yvec_d -- data
    # yvec_f -- function
    # res2   -- the sum of the square of the residuales
    yvec_f = function_fit(parms,xvec)
    res2 = 0
    for i in range(len(xvec)):
        res2= res2 + (yvec_f[i]-yvec_d[i])**2
    return res2

def mk_matrix(array1,array2,m):

    if (len(array1) != len(array2)):
        print ("Arrays are not the same length...")
        exit()

    matrix = scipy.zeros([m,m])
    #amin = min([min(array1), min(array2)])
    #amax = max([max(array1), max(array2)])
    a1min = min(array1)
    a1max = max(array1)
    a2min = min(array2)
    a2max = max(array2)
    
    for ind in range(len(array1)):
        a1 = array1[ind]
        a2 = array2[ind]
        #j = int(round((a1 - amin)/(amax - amin)*(m-1)))
        #i = int(round((a2 - amin)/(amax - amin)*(m-1)))
        j = int(round((a1 - a1min)/(a1max - a1min)*(m-1)))
        i = int(round((a2 - a2min)/(a2max - a2min)*(m-1)))
        if (i == 0) or (j == 0): 
           print (i,j)
        matrix[i,j] = matrix[i,j] + 1
    
    l1 = []
    l1.append("%6.2f"%a1min)
    l1.append("%6.2f"%a1max)
    l2 = []
    l2.append("%6.2f"%a2min)
    l2.append("%6.2f"%a2max)
    #return matrix, [a1min,a1max], [a2min,a2max]
    return matrix, l1, l2

ZERRO = 0.0


if len(sys.argv) != 2:
   print ("error:  this program takes 1 input filename.  ")    
   exit()

filename1     = sys.argv[1]

print ("extrct filename1     = " + filename1)

X,Y = read_file(filename1)

rp  = stats.pearsonr(X,Y)

Xmax = max(X)
Xmin = min(X)
Ymax = max(Y)
Ymin = min(Y)

print (Xmax, Xmin) 
print (Ymax, Ymin)

print ("pearson correlation: r = %6.3f, p-value = %6.3e" % (rp))

print ("run optimization")

parms = [0.1, 0.0]

#opt.minimize(obj_func,parms, args=(y_meas, x),)
#opt.leasesquarts(obj_func,parms, args=(y_meas, x),)
# y = mx + b --> [x, 1] * [m  b]^T
A = numpy.vstack([X.T, numpy.ones(len(X))]).T
#print A
m, b = la.lstsq(A, Y)[0]
Ynew = function_fit([m,b],X)
res2_1 = calc_residuel([m,b],X,Y)
print ("**** y = %6.3f x + %6.3f , res^2 = %6.3f" % (m,b, res2_1))

#m2 = la.lstsq(X, Y)[0]
#Ynew2 = function_fit([m2,0],X)
#res2_2 = calc_residuel([m2,0],X,Y)
##print "****",m2,0,"res^2=",res2_2
#print ("**** y = %6.3f x  , res^2 = %6.3f" % (m2, res2_2))

# Plot distance matrix.
fig = pylab.figure(figsize=(8,8))
#axis = fig.add_axes([0.3,0.1,0.6,0.6])
axis = fig.add_axes([0.1,0.1,0.3,0.3])

threshold1 = 50
threshold2 = 0

lim_min = min(math.floor(Ymin),math.floor(Xmin))
lim_max = max(math.ceil(Ymax), math.ceil(Xmax))
#im = axis.plot(X,Y,'o',[lim_min,lim_max],[lim_min,lim_max],'k-') #,[0,100],[0,100],'--')
im = axis.plot(X,Y,'.') #,[0,100],[0,100],'--')
xlim = axis.get_xlim()
ylim = axis.get_ylim()
print xlim, ylim 
#axis.set_xlabel('file1='+filename1)
#axis.set_ylabel('file2='+filename2)
for tick in axis.get_xticklabels():
  tick.set_rotation(45)

axis = fig.add_axes([0.5,0.1,0.3,0.3])
#im = axis.plot(X[1:10000],Y[1:10000],'r.',X[10001:20000],Y[10001:20000],'b.',X[20001:30000],Y[20001:30000],'g.') #,[0,100],[0,100],'--')
im = axis.plot(X[1:25000],    Y[1:25000],    'r.')
im = axis.plot(X[25001:50000],Y[25001:50000],'b.')
im = axis.plot(X[50001:75000],Y[50001:75000],'g.')
im = axis.plot(X[75001:100000],Y[75001:100000],'m.')
#im = axis.plot( X[30001:40000],Y[30001:40000],color='purple',marker='.')
#im = axis.plot( X[40001:50000],Y[40001:50000],color='cyan',marker='.')
#im = axis.plot( X[50001:60000],Y[50001:60000],color='orange',marker='.')
#im = axis.plot( X[60001:70000],Y[60001:70000],color='gray',marker='.')
#im = axis.plot( X[70001:80000],Y[70001:80000],color='olive',marker='.') 
#im = axis.plot( X[80001:90000],Y[80001:90000],color='pink',marker='.') 
for tick in axis.get_xticklabels():
  tick.set_rotation(45)

axis = fig.add_axes([0.7,0.5,0.1,0.1])
im = axis.plot(X[1:25000],Y[1:25000],'r.') #,[0,100],[0,100],'--')
#im = axis.plot(X[1:10000],Y[1:10000],'r.') #,[0,100],[0,100],'--')
im = axis.plot( X[1],Y[1],color='black',marker='+') 
im = axis.plot( X[25000-1],Y[25000-1],color='black',marker='x') 
#im = axis.plot( X[10000-1],Y[10000-1],color='black',marker='x') 
axis.set_xlim(xlim)
axis.set_ylim(ylim)
for tick in axis.get_xticklabels():
  tick.set_rotation(90)
  tick.set_fontsize('x-small')

axis = fig.add_axes([0.5,0.5,0.1,0.1])
im = axis.plot(X[25001:50000],Y[25001:50000],'b.') #,[0,100],[0,100],'--')
#im = axis.plot(X[10001:20000],Y[10001:20000],'b.') #,[0,100],[0,100],'--')
im = axis.plot( X[25001],Y[25001],color='black',marker='+') 
#im = axis.plot( X[10001],Y[10001],color='black',marker='+') 
im = axis.plot( X[50000-1],Y[50000-1],color='black',marker='x') 
#im = axis.plot( X[20000-1],Y[20000-1],color='black',marker='x') 
axis.set_xlim(xlim)
axis.set_ylim(ylim)
for tick in axis.get_xticklabels():
  tick.set_rotation(90)
  tick.set_fontsize('x-small')

axis = fig.add_axes([0.5,0.7,0.1,0.1])
im = axis.plot(X[50001:75000],Y[50001:75000],'g.') #,[0,100],[0,100],'--')
#im = axis.plot(X[20001:30000],Y[20001:30000],'g.') #,[0,100],[0,100],'--')
im = axis.plot( X[50001],Y[50001],color='black',marker='+') 
#im = axis.plot( X[20001],Y[20001],color='black',marker='+') 
im = axis.plot( X[75000-1],Y[75000-1],color='black',marker='x') 
#im = axis.plot( X[30000-1],Y[30000-1],color='black',marker='x') 
axis.set_xlim(xlim)
axis.set_ylim(ylim)
for tick in axis.get_xticklabels():
  tick.set_rotation(90)
  tick.set_fontsize('x-small')

axis = fig.add_axes([0.7,0.7,0.1,0.1])
im = axis.plot(X[75001:100000],Y[75001:100000],'m.') #,[0,100],[0,100],'--')
im = axis.plot( X[75001],Y[75001],color='black',marker='+')
im = axis.plot( X[100000-1],Y[100000-1],color='black',marker='x')
axis.set_xlim(xlim)
axis.set_ylim(ylim)
for tick in axis.get_xticklabels():
  tick.set_rotation(90)
  tick.set_fontsize('x-small')

#axis = fig.add_axes([0.65,0.5,0.1,0.1])
#im = axis.plot( X[30001:40000],Y[30001:40000],color='purple',marker='.')
#im = axis.plot( X[30001],Y[30001],color='black',marker='+') 
#im = axis.plot( X[40000-1],Y[40000-1],color='black',marker='x') 
#axis.set_xlim(xlim)
#axis.set_ylim(ylim)
#
#axis = fig.add_axes([0.65,0.65,0.1,0.1])
#im = axis.plot( X[40001:50000],Y[40001:50000],color='cyan',marker='.')
#im = axis.plot( X[40001],Y[40001],color='black',marker='+') 
#im = axis.plot( X[50000-1],Y[50000-1],color='black',marker='x') 
#axis.set_xlim(xlim)
#axis.set_ylim(ylim)
#
#axis = fig.add_axes([0.65,0.8,0.1,0.1])
#im = axis.plot( X[50001:60000],Y[50001:60000],color='orange',marker='.')
#im = axis.plot( X[50001],Y[50001],color='black',marker='+') 
#im = axis.plot( X[60000-1],Y[60000-1],color='black',marker='x') 
#axis.set_xlim(xlim)
#axis.set_ylim(ylim)
#
#axis = fig.add_axes([0.8,0.5,0.1,0.1])
#im = axis.plot( X[60001:70000],Y[60001:70000],color='gray',marker='.')
#im = axis.plot( X[60001],Y[60001],color='black',marker='+') 
#im = axis.plot( X[70000-1],Y[70000-1],color='black',marker='x') 
#axis.set_xlim(xlim)
#axis.set_ylim(ylim)
#
#axis = fig.add_axes([0.8,0.65,0.1,0.1])
#im = axis.plot( X[70001:80000],Y[70001:80000],color='olive',marker='.') 
#im = axis.plot( X[70001],Y[70001],color='black',marker='+') 
#im = axis.plot( X[80000-1],Y[80000-1],color='black',marker='x') 
#axis.set_xlim(xlim)
#axis.set_ylim(ylim)
#
#axis = fig.add_axes([0.8,0.8,0.1,0.1])
#im = axis.plot( X[80001:90000],Y[80001:90000],color='pink',marker='.') 
#im = axis.plot( X[80001],Y[80001],color='black',marker='+') 
#im = axis.plot( X[90000-1],Y[90000-1],color='black',marker='x') 
#axis.set_xlim(xlim)
#axis.set_ylim(ylim)
#
#axis.set_ylim(lim_min, lim_max)
#axis.set_xlim(lim_min, lim_max)

## new subplot
axis = fig.add_axes([0.1,0.5,0.3,0.3])

msize = 50
matrix,lab1,lab2 = mk_matrix(X,Y,msize)


cdict = {'red': [(0.0,      1.0, 1.0),
                 (0.1,  1.0, 1.0),
                 (0.5,      0.8, 0.8),
                 (0.8,  0.7, 0.7),
                 (1.0,      0.0, 0.0)],

       'green': [(0.0,      1.0, 1.0),
                 (0.1,  0.0, 0.0),
                 (0.5,      0.0, 0.0),
                 (0.8,  0.0, 0.0),
                 (1.0,      0.0, 0.0)],

       'blue':  [(0.0,      1.0, 1.0),
                 (0.1,  0.0, 0.0),
                 (0.5,      1.0, 1.0),
                 (0.8,  1.0, 1.0),
                 (1.0,      1.0, 1.0)]}

my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,150)

im = axis.imshow(matrix, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)

val_yticks = axis.get_yticks()
print (val_yticks)
axis.set_xticks([0,msize-1])
axis.set_yticks([0,msize-1])
axis.set_xticklabels(lab1)
axis.set_yticklabels(lab2)

#fig.show()
fig.savefig('fig.png',dpi=600)


