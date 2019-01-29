#! /usr/bin/python2.6
## this is the version of python on sublime 

## This was adapted from the web:
## http://stackoverflow.com/questions/2982929/plotting-results-of-hierarchical-clustering-ontop-of-a-matrix-of-data-in-python

import sys
import math
import matplotlib
import scipy
import pylab
import scipy.cluster.hierarchy as sch

ZERRO = 0.0

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


if len(sys.argv) != 3:
   print "error"    
   exit()

matfilename = sys.argv[1]
labfilename = sys.argv[2]

# import the label information

file = open(labfilename)
lines = file.readlines()
file.close()

m_lab = len(lines)
labels = []

for line in lines:
    splitline = line.split(',')
    labels.append(splitline[1].strip())
    #print splitline[0], splitline[1]


# Import data from matrix file:

file = open(matfilename)
lines = file.readlines()
file.close()


m = len(lines)
n = len(lines[0].split(','))

if (m_lab != m):
    print "labels and matrix have different number of rows"
    sys.exit()
if (m != n):
    print "inconsitancy in numbers of rows and columns in the matrix."
    sys.exit()

print m,n

if m != n:
   print 'Error: m!=n'
   exit()

#m = 20
#n = 20

X = scipy.zeros([m,n])
Xvec = scipy.zeros(n*(n-1)/2)
Xlog10 = scipy.zeros([m,n])
Xlog10shiftvec = scipy.zeros(n*(n-1)/2)

countline = 0
count2    = 0 
for line in lines:
#    if count == m:
#       break;
 
    line = line.strip('\n')
    splitline = line.split(',')
    if (n != (len(splitline))):
        print "ERROR: n != (len(splitline), inconsitancy in number of elements in rows"
        sys.exit()

    for i in range(0,n):
        val = float(splitline[i])
        X[countline,i] = val
        if val == ZERRO: 
           Xlog10[countline,i] = -1000.0;
        else: 
           Xlog10[countline,i] = math.log(val)
        if i > countline :
           Xvec[count2] = X[countline,i]
           Xlog10shiftvec[count2] = Xlog10[countline,i] + 1000.0
           print countline,i,'--', count2
           count2 = count2+1
           #print Xvec  
    countline = countline + 1

# Generate random features and distance matrix.

##x = scipy.rand(40)
#D = scipy.zeros([n,n])
#for i in range(n):
#    print "i =" , i
#    for j in range(n):
#        D[i,j] = distance(X[:,i], X[:,j],200)
#        #if i == j:
#        #   print D[i,j]
#    #print " "

# Compute and plot first dendrogram.
#Y = sch.linkage(Xvec, method='centroid')
#Y = sch.linkage(Xvec, method='median')
#Y = sch.linkage(Xvec, method='average')
#Y = sch.linkage(Xvec, method='single')
#Y = sch.linkage(Xvec, method='complete')
#Y = sch.linkage(Xlog10shiftvec, method='single')
#Y = sch.linkage(Xlog10shiftvec, method='average')
Y = sch.linkage(Xlog10shiftvec, method='complete')
#help(sch.linkage)
#threshold = 10**(Xlog10.min()/4)
#print (Xlog10.min())
#threshold = 1
#threshold = Xlog10shiftvec.max() * 2.0/3.0 
threshold = -200 + 1000
#help(sch.fcluster)
clusters = sch.fcluster(Y, threshold, 'distance')
#clusters = sch.fcluster(Y, threshold, 'inconsistent')
print clusters

cluster_list = []

numOfClusters = clusters.max()

## intialize array that will store the labels for each cluster
for i in range(numOfClusters):
    cluster_list.append('c'+ str(i+1)+' -- ')

## fill array with labels by appending the string assosiated with each cluster
for i in range(len(clusters)):
    cluster_list[clusters[i]-1] = cluster_list[clusters[i]-1] + labels[i] + ','
## write the cluster
for i in range(numOfClusters):
    print cluster_list[i]

fig = pylab.figure(figsize=(8,8))
ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
Z1 = sch.dendrogram(Y, orientation='right')
#help(sch.dendrogram)
ax1.set_xticks([])
ax1.set_yticks([])
#print ax1.get_ylim()
#ax1.set_ylim(-1, n)

# Compute and plot second dendrogram.
ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
Z2 = sch.dendrogram(Y)
ax2.set_xticks([])
ax2.set_yticks([])
#ax2.set_xlim(-1, n)

# Plot distance matrix.
axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
idx1 = Z1['leaves']
idx2 = Z2['leaves']
Xlog10 = Xlog10[idx1,:]
Xlog10 = Xlog10[:,idx2]
#X = X[idx1,:]
#X = X[:,idx2]

#labels_sort = labels[idx1]
# make sorted label list
labels_sort = []
for i in idx1:
  #labels_sort.append(labels[i])
  #labels_sort.append('c'+str(clusters[i]))
  #labels_sort.append(labels[i]+'--c'+str(clusters[i]))
  labels_sort.append('c'+str(clusters[i]) + '-'+ labels[i])
#help(axmatrix.imshow)

# cdict = {'red': ((0.0, 0.0, 0.0),
#                  (0.0, 0.0, 0.0),
#                  (0.0, 0.0, 0.0)),
#          'green': ((0.0, 0.0, 0.0),
#                    (0.5, 1.0, 0.0),
#                    (1.0, 1.0, 1.0)),
#          'blue': ((0.0, 0.0, 0.0),
#                   (0.5, 1.0, 0.0),
#                   (1.0, 0.5, 1.0))}

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

im = axmatrix.imshow(Xlog10, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)
#im = axmatrix.imshow(Xlog10, aspect='auto', origin='lower',interpolation='nearest', cmap=pylab.cm.YlGnBu)
#im = axmatrix.imshow(X, aspect='auto', origin='lower',interpolation='nearest', cmap=pylab.cm.YlGnBu)


v = range(0,n)
#for i in range(0,n):
#    v[i] = v[i] 

axmatrix.plot(v,v,'yo',markersize=1)
im.set_clim(-300,10)
#im.set_clim(0,0.1)
#axmatrix.set_xlim(-1, n)
#axmatrix.set_ylim(-1, n)
axmatrix.set_xlim(-0.5, n-0.5)
axmatrix.set_ylim(-0.5, n-0.5)
axmatrix.set_xticks(range(0,n))
axmatrix.set_yticks([])
axmatrix.set_xticklabels(labels_sort)
#label.set_rotation('vertical')

#label = axes.yaxis.get_major_ticks().label
for i in range(0,m_lab):
  label = axmatrix.xaxis.get_major_ticks()[i].label
  #label.set_fontsize(size)
  label.set_fontsize(4)
  label.set_rotation('vertical')

# Plot colorbar.
axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
pylab.colorbar(im, cax=axcolor)
fig.show()
fig.savefig('dendrogram.png',dpi=600)

