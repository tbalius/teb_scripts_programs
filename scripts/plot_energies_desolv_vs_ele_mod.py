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
#import scipy.cluster.hierarchy as sch
#from scipy.optimize import opt
import scipy.optimize as opt
import scipy.linalg   as la
import scipy.stats    as stats


def read_extract_file(filename):

    file = open(filename)
    lines = file.readlines()
    file.close()

    #idlist = []
    count  = 0
    es_array = []
    lig_desol = []
    rec_desol = []
    tot_desol = []
    ## X is the Predicted value (sea_dock)
    ## Y is the accual value (sea)
    #firstline = True
    for line in lines:
        #if firstline == True:
        #   firstline = False
        #   continue
        line = line.strip('\n')
        splitline = line.split()
        mid = splitline[2]
        es = float(splitline[12])
        gist = float(splitline[19])
        lig_desolva = float(splitline[15])
        lig_desolvp = float(splitline[16])
        print mid, es, gist, lig_desolva, lig_desolvp 
        es_array.append(es)
        lig_desol.append(lig_desolva+lig_desolvp)
        rec_desol.append(gist)
        tot_desol.append(lig_desolva+lig_desolvp+gist)
        count = count + 1
    return es_array, lig_desol, rec_desol, tot_desol 


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
        print "Arrays are not the same length..."
        exit()

    matrix = scipy.zeros([m,m])
    amin = min([min(array1), min(array2)])
    amax = max([max(array1), max(array2)])
    
    for ind in range(len(array1)):
        a1 = array1[ind]
        a2 = array2[ind]
        j = int(round((a1 - amin)/(amax - amin)*(m-1)))
        i = int(round((a2 - amin)/(amax - amin)*(m-1)))
        if (i == 0) or (j == 0): 
           print i,j 
        matrix[i,j] = matrix[i,j] + 1

    return matrix


def convert_array_to_numpy(X):
    #nX = scipy.zeros([1,len(X)])
    nX = scipy.zeros([len(X)])
    for i,x in enumerate(X):
        #nX[0,i] = x
        nX[i] = x
    return nX


def stats_fig(X,Y,label1,label2,filename,title):

  Xn = convert_array_to_numpy(X)
  Yn = convert_array_to_numpy(Y)

  rp  = stats.pearsonr(X,Y)
  #rps = stats.pearsonr(Xscore,Yscore)
  rs  = stats.spearmanr(X,Y)
  
  Xmax = max(X)
  Xmin = min(X)
  Ymax = max(Y)
  Ymin = min(Y)
  
  print Xmax, Xmin 
  print Ymax, Ymin
  
  print "pearson correlation: r = %6.3f, p-value = %6.3e" % (rp)
  #print "pearson correlation: r = %6.3f, p-value = %6.3e" % (rps)
  print "spearma correlation: r = %6.3f, p-value = %6.3e" % (rs)
  
  print "run optimization"
  
  parms = [0.1, 0.0]
  
  #opt.minimize(obj_func,parms, args=(y_meas, x),)
  #opt.leasesquarts(obj_func,parms, args=(y_meas, x),)
  # y = mx + b --> [x, 1] * [m  b]^T
  print len(Xn)
  print len(Yn)
  #A = numpy.vstack([Xn.T, numpy.ones(len(Xn))]).T
  A = numpy.vstack([Xn, numpy.ones(len(Xn))]).T
  print len(A)
  m, b = la.lstsq(A, Yn)[0]
  Ynew = function_fit([m,b],Xn)
  res2_1 = calc_residuel([m,b],Xn,Yn)
  print "**** y = %6.3f x + %6.3f , res^2 = %6.3f" % (m,b, res2_1)
  
  A2 = numpy.vstack([Xn]).T
  m2 = la.lstsq(A2, Yn)[0]
  Ynew2 = function_fit([m2,0],Xn)
  res2_2 = calc_residuel([m2,0],Xn,Yn)
  #print "****",m2,0,"res^2=",res2_2
  print "**** y = %6.3f x  , res^2 = %6.3f" % (m2, res2_2)

  # Plot distance matrix.
  fig = pylab.figure(figsize=(8,8))
  #axis = fig.add_axes([0.3,0.1,0.6,0.6])
  axis = fig.add_axes([0.1,0.1,0.3,0.3])

  threshold1 = 50
  threshold2 = 0

  lim_min = min(math.floor(Ymin),math.floor(Xmin))
  lim_max = max(math.ceil(Ymax), math.ceil(Xmax))
  im = axis.plot(X,Y,'o',[lim_min,lim_max],[lim_min,lim_max],'k-') #,[0,100],[0,100],'--')
  axis.set_xlabel(label1)
  axis.set_ylabel(label2)
  axis.set_title(title)

  axis.set_ylim(lim_min, lim_max)
  axis.set_xlim(lim_min, lim_max)
  axis.set_ylim(lim_min, lim_max)

  ## new subplot
  axis = fig.add_axes([0.1,0.5,0.3,0.3])

  matrix = mk_matrix(X,Y,50)


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
  #im = axis.imshow(matrix, aspect='auto', origin='lower',interpolation='nearest')
  axcolor = fig.add_axes([0.4,0.55,0.05,0.2])
  pylab.colorbar(im, cax=axcolor)

  fig.savefig(filename,dpi=600)


ZERRO = 0.0


if len(sys.argv) != 3:
   print "error:  this program takes 1 input extrct filename and 1 title.  "    
   exit()

filename1     = sys.argv[1]
title     = sys.argv[2]

print "extrct filename1     = " + filename1

es_array,lds_array,rds_array,tds_array = read_extract_file(filename1)

stats_fig(es_array,tds_array,'es','tot_desol','correlation_es_ds.png',title)
