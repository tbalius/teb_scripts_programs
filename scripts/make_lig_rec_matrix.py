#! /usr/bin/python2.6
## this is the version of python on sublime 

## This was adapted from the web:
## http://stackoverflow.com/questions/2982929/plotting-results-of-hierarchical-clustering-ontop-of-a-matrix-of-data-in-python

import sys
import scipy
#import array
#import numpy
import matplotlib
import pylab
import scipy.cluster.hierarchy as sch


class sumIndex:
    def __init__(self, sumVal, index):
        self.sumVal = float(sumVal)
        self.index = int(index)
    def __cmp__(self, other):
        return cmp(self.sumVal, other.sumVal)

def getIndex(S):
    #indexvec = scipy.zeros(len(S))
    #indexvec = array.array('i',(0 for i in range(0,len(S))))
    indexvec = scipy.array([0 for i in range(0,len(S))])
    for i in range(len(S)):
        print S[i].index
        indexvec[i] = S[i].index
    return indexvec

# this defines a compares two DATA by comparing the two scores
# it is sorted in decinding order.
def bySum(x, y):
   return cmp(x.sumVal, y.sumVal)

def distance(X,Y,threshold):
    dist2 = 0

    if len(X) !=len(Y): 
        print "ERROR: distance: len(X) !=len(Y)"
        print "len(X) = " + str(len(X))
        print "len(Y) = " + str(len(Y))
        sys.exit()

    for i  in range(len(X)):
        if (X[i] > threshold):
            X[i] = threshold
        if (Y[i] > threshold):
            Y[i] = threshold
        dist2 = (X[i]-Y[i])**2
#        print X[i] , Y[i] 
    return float(dist2**(0.5))
    #return dist2

def mat_to_vector(Mat):
    ## 1 - tc is more like a distance than tc.
    m = len(Mat)
    n = len(Mat[0])

    if (m != n):
        print "inconsitancy in numbers of rows and columns in the matrix."
        sys.exit()

    print m,n

    X = scipy.zeros([m,n])
    Xvec = scipy.zeros(n*(n-1)/2)

    count2    = 0

    ## converts from a 2D array to Scipy Matrix 
    for i in range(0,n):
        for j in range(0,n):
               #X[i,j] = -Mat[i][j] + 1.0
               X[i,j] = Mat[i][j] 

    for i in range(0,n):
        for j in range(i+1,n):
               #Xvec[count2] = -Mat[i][j] + 1.0
               Xvec[count2] = Mat[i][j] 
               count2 = count2+1

    return X,Xvec

    

# Import data from file:

#file = open('/raid9/tbalius/Projects/ProteomicDOCKing/out.csv')
file = open('output.csv')
#file = open('output_temp.csv')
lines = file.readlines()
file.close()

m = len(lines)
#n = len(lines[0].split(','))-1
n = len(lines[0].split(','))-2

#m = 20
#n = 20

X = scipy.zeros([m,n])
labels = []

count = 0
for line in lines:
#    if count == m:
#       break;
 
    line = line.strip('\n')
    splitline = line.split(',')
    if (n != (len(splitline)-2)):
        print "ERROR: n != (len(splitline)-1, inconsitancy in number of elements in rows"
        sys.exit()
    for i in range(0,n):
        X[count,i] = float(splitline[i+2]) ## frist column is the zinc id. the second column is a id number
    labels.append(splitline[0])
    count = count + 1

# Generate random features and distance matrix.

#x = scipy.rand(40)
D = scipy.zeros([n,n])
for i in range(n):
    print "i =" , i
    for j in range(n):
        #D[i,j] = distance(X[:,i], X[:,j],200)
        D[i,j] = distance(X[:,i], X[:,j],10)
        #if i == j:
        #   print D[i,j]
    #print " "

#S = scipy.zeros([1,m])
#for i in range(m):
#    S[i] = sum(X[i,:]
#
#S.sort()
S = []
for i in range(m):
    tempS = sumIndex(sum(X[i,:]),i)
    S.append(tempS)
S.sort(bySum)

idsum = getIndex(S)

# Compute and plot first dendrogram.
Dmat, Dvec = mat_to_vector(D)
#Y = sch.linkage(Dvec, method='centroid')
Y = sch.linkage(Dvec, method='single')
#Y = sch.linkage(D, method='single')

fig = pylab.figure(figsize=(8,8))
ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
Z1 = sch.dendrogram(Y, orientation='right')
ax1.set_xticks([])
ax1.set_yticks([])

# Compute and plot second dendrogram.
ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
Z2 = sch.dendrogram(Y)
ax2.set_xticks([])
ax2.set_yticks([])

# Plot distance matrix.
axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
idx1 = Z1['leaves']
idx2 = Z2['leaves']
D = D[idx1,:]
D = D[:,idx2]
im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap=pylab.cm.YlGnBu)
im.set_clim(-100.0, 200.0)
axmatrix.set_xticks([])
axmatrix.set_yticks([])

# Plot colorbar.
axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
pylab.colorbar(im, cax=axcolor)
fig.show()
fig.savefig('dendrogram.png')


## show data clustered/sorted by columns
fig = pylab.figure(figsize=(8,8))

ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
Z2 = sch.dendrogram(Y)
ax2.set_xticks([])
ax2.set_yticks([])

#X = X[:,idx1]
print idsum
print idx1

sort_labels = []

for i in idsum:
    sort_labels.append(labels[i])
    
N = 10
for i in range(N):
    print sort_labels[i]

X = X[idsum,:]
X = X[:,idx1]

topN = range(0,N)

Xshort = X[topN,:]

axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])



cdict = {'red': ((0.0, 0.0, 0.0),
                  (0.0, 0.0, 0.0),
                  (1.0, 1.0, 1.0)),
          'green': ((0.0, 0.0, 0.0),
                    (0.0, 0.0, 0.0),
                    (1.0, 1.0, 1.0)),
          'blue': ((0.0, 0.0, 0.0),
                   (0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0))}


my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,100)

#im = axmatrix.imshow(X, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)
im = axmatrix.imshow(Xshort, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)



#im = axmatrix.matshow(X, aspect='auto', origin='lower', cmap=pylab.cm.YlGnBu,interpolation='nearest')
#pylab.clim( [-100,200])
im.set_clim(-100.0, 10.0)
axmatrix.set_xticks([])
axmatrix.set_yticks([])

axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
pylab.colorbar(im, cax=axcolor)
fig.show()
fig.savefig('heatmap.png')

# fig = pylab.figure()
# pylab.imshow(arr,interpolation='nearest')
# pylab.colorbar()
# pylab.clim([0.5,0.8])
# pylab.show()


