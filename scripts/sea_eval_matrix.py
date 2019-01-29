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

def fill_line(X,Y,num):
    newX = []
    newY = []
    #newX=X
    #newY=Y
    for i in range(1,len(X)):
        vecX = numpy.linspace(X[i-1],X[i],num) # append list with list
        vecY = numpy.linspace(Y[i-1],Y[i],num) # append list with list
        #print X[i-1],X[i]
        #print vecX
        #print Y[i-1],Y[i]
        #print vecY
        for i in range(num):
            x = vecX[i]
            y = vecY[i]
            newX.append(x)
            newY.append(y)
    #return newX,newY
    return newX,newY



if len(sys.argv) != 4:
   print "error:  this program takes 3 inputs matfilename, labelfilename, clusterfilename (this last is writen out by the script)"    
   exit()

matfilename     = sys.argv[1]
labfilename     = sys.argv[2]
clusterfilename = sys.argv[3]

print "matfilename     = " + matfilename
print "labfilename     = " + labfilename
print "clusterfilename = " + clusterfilename

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
Xlog10shift = scipy.zeros([m,n])
Xlog10shiftvec = scipy.zeros(n*(n-1)/2)

shiftval = 500.0

minval = 10000

countline = 0
count2    = 0 
for line in lines:
    line = line.strip('\n')
    splitline = line.split(',')
    if (n != (len(splitline))):
        print "ERROR: n != (len(splitline), inconsitancy in number of elements in rows"
        sys.exit()

    for i in range(0,n):
        val = float(splitline[i])
        X[countline,i] = val
        if val == ZERRO: 
           Xlog10[countline,i] = -1*shiftval;
        else: 
           Xlog10[countline,i] = math.log(val)
           if math.log(val) < minval:
              minval = math.log(val)
        Xlog10shift[countline,i] = Xlog10[countline,i] + shiftval

        if i > countline :
           Xvec[count2] = X[countline,i]

           ## we can not have a negetive distance 
           if Xlog10[countline,i] > (-1*shiftval):
              Xlog10shiftvec[count2] = Xlog10[countline,i] + shiftval
              #print (Xlog10[countline,i] + shiftval) 
           else:
              #print (Xlog10[countline,i] + shiftval) 
              Xlog10shiftvec[count2] = 0
           #print countline,i,'--', count2
           count2 = count2+1
           #print Xvec  
    countline = countline + 1

if -1*minval > shiftval: 
    print "Warrning: " + str(-1*minval) + " is larger than shiftval = " + str(shiftval)
    #exit()

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
threshold  =  shiftval * 9/10 
cthreshold =  shiftval /2.0
#threshold = 5.0
#threshold = 10 
#threshold = 2 
#help(sch.fcluster)
clusters = sch.fcluster(Y, threshold, 'distance')
#clusters = sch.fcluster(Y, threshold, 'inconsistent')
#print clusters

cluster_list  = [] # list of pdb names in each cluster
cluster_sizes = [] # list of the size of each cluster

numOfClusters = clusters.max()

## intialize array that will store the labels for each cluster
for i in range(numOfClusters):
    cluster_list.append('c'+ str(i+1)+' -- ')
    cluster_sizes.append(0)

## fill array with labels by appending the string assosiated with each cluster
for i in range(len(clusters)):
    cluster_list[clusters[i]-1] = cluster_list[clusters[i]-1] + labels[i] + ','
    cluster_sizes[clusters[i]-1] = cluster_sizes[clusters[i]-1] + 1

## write the cluster
#for i in range(numOfClusters):
#    print cluster_list[i]

## write the cluster with more than 3 members
file = open(clusterfilename,'w')
print " larger clusters: "
#file.write(" larger clusters: ")
for i in range(numOfClusters):
    if cluster_sizes[i] > 3:
       print "  " + cluster_list[i]
       file.write("  %s\n" % cluster_list[i])
file.close()

## make a denogram plot
fig0 = pylab.figure(figsize=(8,8))
#ax0 = fig0.add_axes([0.1,0.1,0.6,0.6],polar=True)
#ax0 = fig0.add_axes([0.1,0.1,0.6,0.6],projection='hammer')
ax0 = fig0.add_axes([0.1,0.1,0.6,0.6])
Z1 = sch.dendrogram(Y, color_threshold=threshold,no_plot=False)
fig0.show()
fig0.savefig('dendrogram0.png',dpi=600)
ax0.cla() # clear axis
fig0.clf() # clear figure
#close() # close a figure window

#ax0 = fig0.add_axes([0.1,0.1,0.6,0.6],polar=True)
ax0 = fig0.add_axes([0.1,0.1,0.6,0.6])

# transform dendogram to appear on radial plot
xc = Z1['icoord'] # x-cordenates; format is as follows [x11,x12,x13,x14; . . .; xN1,xN2,xN3,xN4 ]; each U is has four x values
yc = Z1['dcoord'] # y-cordenates; each U is has four y values 
print len(xc)
print len(yc)
#for i in ic:
#    print i
#for d in dc:
#    print d
scalVal = 600 #
spaceVal = 50 #
thresVal = 200 #


for index in range(len(xc)):
    # normalize x-axis to be 0 to 360
    xc[index][0] = xc[index][0]/(10*len(labels))*2*numpy.pi
    xc[index][1] = xc[index][1]/(10*len(labels))*2*numpy.pi
    xc[index][2] = xc[index][2]/(10*len(labels))*2*numpy.pi
    xc[index][3] = xc[index][3]/(10*len(labels))*2*numpy.pi
    # reverse the y-axis so that 0 maps to 30; and 30 to zero
    yc[index][0] = scalVal - yc[index][0]
    yc[index][1] = scalVal - yc[index][1]
    yc[index][2] = scalVal - yc[index][2]
    yc[index][3] = scalVal - yc[index][3]


for index in range(len(xc)):
    ##if max(yc[index]) > 10: # do not print leafs at the bottom of the dendogram.
    ##if min(yc[index]) > thresVal: # do not print leafs at the bottom of the dendogram.
    ##if max(yc[index]) > thresVal and min(yc[index]) > thresVal: # do not print leafs at the bottom of the dendogram.
    ##if max(yc[index]) > 1.5*thresVal : # do not print leafs at the bottom of the dendogram.
    if min(yc[index]) < scalVal -1.5*thresVal :
       x = xc[index]
       y = yc[index]
       x,y = fill_line(xc[index],yc[index],100)
       matplotlib.pyplot.plot(x,y,'b.')
       #ax0.plot(xc[index],yc[index],'ro')
       ##ax0.plot(xc[index],yc[index],'ro-')

# put all the curcles on top of the dots
for index in range(len(xc)):
    if min(yc[index]) < scalVal -1.5*thresVal :
       ax0.plot(xc[index],yc[index],'ro')
       #ax0.plot(xc[index],yc[index],'ro-')

#ax0.invert_yaxis()
ax0.set_ylim(0,scalVal-thresVal)
ax0.set_yticks(range(0, scalVal-thresVal, spaceVal))                   # Define the yticks
ax0.set_yticklabels(map(str, range(scalVal, thresVal, -spaceVal)))   # Change the labels

print Y[4][1]
print list(Y)[4:10]
fig0.show()
fig0.savefig('radial_dendrogram.png',dpi=600)

fig = pylab.figure(figsize=(8,8))
ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
#Z1 = sch.dendrogram(Y, orientation='right')
Z1 = sch.dendrogram(Y, orientation='right',color_threshold=threshold)
matplotlib.pyplot.plot([threshold,threshold],[0,10*len(labels)],'k--') # draws a datshed line where dendogram is cut.
#help(sch.dendrogram)
ax1.set_xticks([])
ax1.set_yticks([])
#exit()
#print ax1.get_ylim()
#ax1.set_ylim(-1, n)

# Compute and plot second dendrogram.
ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
#Z2 = sch.dendrogram(Y)
Z2 = sch.dendrogram(Y,color_threshold=threshold)
matplotlib.pyplot.plot([0,10*len(labels)],[threshold,threshold],'k--') # draws a datshed line where dendogram is cut.
ax2.set_xticks([])
ax2.set_yticks([])
#ax2.set_xlim(-1, n)

# Plot distance matrix.
axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
idx1 = Z1['leaves']
idx2 = Z2['leaves']
Xlog10shift = Xlog10shift[idx1,:]
Xlog10shift = Xlog10shift[:,idx2]
Xlog10 = Xlog10[idx1,:]
Xlog10 = Xlog10[:,idx2]
X = X[idx1,:]
X = X[:,idx2]

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


my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,20)

#im = axmatrix.imshow(Xlog10,     aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)
#im = axmatrix.imshow(Xlog10,     aspect='auto', origin='lower',interpolation='nearest', cmap=pylab.cm.YlGnBu)
#im = axmatrix.imshow(X,          aspect='auto', origin='lower',interpolation='nearest', cmap=pylab.cm.YlGnBu)
#im = axmatrix.imshow(X,          aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)
im = axmatrix.imshow(Xlog10shift, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)


#v = range(0,n)
#for i in range(0,n):
#    v[i] = v[i] 

#axmatrix.plot(v,v,'yo',markersize=1)
#im.set_clim(-300,10)
#im.set_clim(0,400)
im.set_clim(0,cthreshold)
#im.set_clim(0,0.1)
#axmatrix.set_xlim(-1, n)
#axmatrix.set_ylim(-1, n)
axmatrix.set_ylim(-0.5, n-0.5)
axmatrix.set_xlim(-0.5, n-0.5)
axmatrix.set_yticks([])
axmatrix.set_xticks([])
#axmatrix.set_xticks(range(0,n))
#axmatrix.set_xticklabels(labels_sort)
#label.set_rotation('vertical')

##label = axes.yaxis.get_major_ticks().label
#for i in range(0,m_lab):
#  label = axmatrix.xaxis.get_major_ticks()[i].label
#  #label.set_fontsize(size)
#  label.set_fontsize(4)
#  label.set_rotation('vertical')

#axmatrix.set_axisbelow(b=False)
#axmatrix.xticks(ticks, fontsize=1)

# Plot colorbar.
axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
pylab.colorbar(im, cax=axcolor)
fig.show()
fig.savefig('dendrogram.png',dpi=600)

