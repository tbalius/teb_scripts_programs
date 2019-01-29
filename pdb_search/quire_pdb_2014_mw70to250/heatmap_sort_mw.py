#! /raid1/people/tbalius/zzz.virtualenvs/sgehead_python_env/bin/python

## Writen by Trent E. Balius in B. Shoichet group

## This was adapted from the web:
## http://stackoverflow.com/questions/2982929/plotting-results-of-hierarchical-clustering-ontop-of-a-matrix-of-data-in-python

import sys, os
import copy
import math
import matplotlib
import scipy
import numpy
import pylab
import scipy.cluster.hierarchy as sch


def getlabel(labfilename):
  # import the label information
  
  file = open(labfilename)
  lines = file.readlines()
  file.close()
  
  #m_lab = len(lines)
  labels = []
  
  for line in lines:
      splitline = line.split(',')
      labels.append(splitline[0].strip())
      #print splitline[0], splitline[1]
  return labels

def getmw(labfilename):
  # import the label information

  file = open(labfilename)
  lines = file.readlines()
  file.close()

  #m_lab = len(lines)
  dic = {} 

  for line in lines:
      splitline = line.split()
      ligname = splitline[0].strip()
      mw      = splitline[1]
      if not (ligname in dic):
          dic[ligname] = mw
      #print splitline[0], splitline[1]
  return dic



def mat_to_vector(Mat):
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
               ## 1 - tc is more like a distance than tc.
               #X[i,j] = -Mat[i][j] + 1.0
               X[i,j] = Mat[i][j]

    for i in range(0,n):
        for j in range(i+1,n):
               ## 1 - tc is more like a distance than tc.
               #Xvec[count2] = -Mat[i][j] + 1.0
               Xvec[count2] = Mat[i][j]
               count2 = count2+1

    return X,Xvec

def get_cluster(X,labels,threshold,dirname):
    print "in function get_cluster"
    if len(X) != len(labels):
       print "len(X) != len(labels)"
       print len(X), len(labels)
       exit()

    Xnew,Xvec = mat_to_vector(X)

    #Y = sch.linkage(Xvec, method='complete')
    Y = sch.linkage(Xvec, method='single')
    clusters = sch.fcluster(Y, threshold, 'distance')
    print clusters
    cluster_list  = [] # list of pdb names in each cluster
    cluster_sizes = [] # list of the size of each cluster

    numOfClusters = clusters.max()

    ## intialize array that will store the labels for each cluster
    for i in range(numOfClusters):
        cluster_list.append('c'+ str(i+1)+' -- ')
        cluster_sizes.append(0)
    #
    ## fill array with labels by appending the string assosiated with each cluster
    for i in range(len(clusters)):
        cluster_list[clusters[i]-1] = cluster_list[clusters[i]-1] + labels[i] + ','
        cluster_sizes[clusters[i]-1] = cluster_sizes[clusters[i]-1] + 1

    ## write the cluster
    for i in range(numOfClusters):
        print cluster_list[i]

    ## write the cluster with more than 3 members
#    os.system('rm -rf   large_clusters'+dirname)
#    os.system('mkdir -p large_clusters'+dirname)
#    os.chdir('large_clusters'+dirname)

    # this file stores a represenitive molecule from each cluster.
    filename = "cluster_rep.txt"
    fh_rep = open(filename,'w')
    print " larger clusters: "
    for i in range(numOfClusters):
       filename = "cluster" + str(i+1) + ".txt"
       fh = open(filename,'w')
       fh.write(cluster_list[i].replace(' ','').replace(',','\n').replace('-','\n'))
       fh.close()
       fh_rep.write(cluster_list[i].replace(' ','').split(',')[0].split('-')[2]+'\n') # print the frist guy in the cluster. 

       if cluster_sizes[i] > 3:
           print "  " + cluster_list[i]
#           name = cluster_list[i].split('--')[0].replace(' ','')
#           mols = cluster_list[i].split('--')[1].split(',')
           ## get images from zinc
#           os.system('mkdir -p '+ name)
#           os.chdir(name)
#           fout = open( name+"_info.txt",'w')
#           for mol in mols:
#               print mol
#               fout.write(mol+'\n')
#               os.system('wget http://zinc.docking.org/img/sub/' + mol.replace('C','').replace(' ','')+'.gif')
#               #os.system('wget http://zinc.docking.org/substance/' + mol.replace('C','').replace(' ','')+'')
#           fout.close()
#           os.chdir('../')
#    os.chdir('../')
    fh_rep.close()
              
    return Y


def import_data(datafilename):
     # Import data from matrix file:
     file = open(datafilename)
     lines = file.readlines()
     file.close()
     
     ligdic = {}
     count = 0
     vector_tv = [] 
     vec_lig1 = []
     vec_lig2 = []
     label = []
     
     for line in lines:
         splitline = line.split(',')
         lig1 = splitline[0]
         lig2 = splitline[1]
         dist = splitline[2]

         vector_tv.append(dist)
         vec_lig1.append(lig1)
         vec_lig2.append(lig2)

         if not lig1 in ligdic:
            label.append(lig1)
            ligdic[lig1] = count
            count = count + 1
         if not lig2 in ligdic:
            label.append(lig2)
            ligdic[lig2] = count
            count = count + 1

     m = len(ligdic.keys())
     n = m

     X = scipy.ones([m,n])
     Xvec = scipy.zeros(n*(n-1)/2)
    
     countline = 0
     count2    = 0

     for i in range(m):
         X[i,i] = 0.0
 
     for i in range(len(vector_tv)):
         j = int(ligdic[vec_lig1[i]])
         k = int(ligdic[vec_lig2[i]])
         val = float(vector_tv[i])

         X[j,k] = 1-val 
         X[k,j] = 1-val 
     return X ,n, m, label 


ZERRO = 0.0

datafilename  = sys.argv[1]
mwfilename = sys.argv[2]

print "data_filename = "+ datafilename  
print "mw_filename = "+ mwfilename  



dic_lig_to_mw = getmw(mwfilename)
#labels1 = getlabel(labfilename)
#labels2 = getlabel(lab2filename)

X,n,m,labels1 = import_data(datafilename)
#dist_mat1,n1,m1 = import_mat(dist_mat1_fn)

mw = []
mw_index = []

print dic_lig_to_mw

count = 0
for lig in labels1:
    print lig
    print dic_lig_to_mw[lig]
    if not (lig in dic_lig_to_mw):
        print "ligand"+lig+" not in dictionary . . ."
        exit()
    mw.append(float(dic_lig_to_mw[lig]))
    ele = [float(dic_lig_to_mw[lig]),count]
    mw_index.append(ele)
    count = count+1

sorted_mw_index = sorted(mw_index)

idx1 = []
for ele in sorted_mw_index:
    idx1.append(ele[1])
    print ele[1]

#threshold =  0.7
#threshold = 0.51
#threshold =  0.47
#threshold =  0.4
#threshold =  0.31
threshold =  0.5
## create a distance matrix --> dendogram by comparing all rows
#Y1 = get_cluster(X,labels1,threshold,'set2')

#
fig = pylab.figure(figsize=(8,8))
#ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
##Z1 = sch.dendrogram(Y, orientation='right')
#Z1 = sch.dendrogram(Y1, orientation='right',color_threshold=threshold)
#matplotlib.pyplot.plot([threshold,threshold],[0,10*m],'k--') # draws a datshed line where dendogram is cut.
##help(sch.dendrogram)
#ax1.set_xticks([])
#ax1.set_yticks([])
##exit()
##print ax1.get_ylim()
##ax1.set_ylim(-1, n)

## Plot distance matrix.
axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
#idx1 = Z1['leaves']
#idx2 = Z2['leaves']
#X = X[idx1,:]
#X = X[:,idx1]
#X = X[:,idx2]

##labels_sort = labels[idx1]
## make sorted label list
labels_sort = []
for i in idx1:
  labels_sort.append( labels1[i])

#cdict = {'red': ((0.0, 0.0, 0.0),
#                  (0.0, 0.0, 0.0), 
#                  (1.0, 1.0, 1.0)),
#          'green': ((0.0, 0.0, 0.0),
#                    (0.0, 0.0, 0.0),
#                    (1.0, 1.0, 1.0)),
#          'blue': ((0.0, 0.0, 0.0),
#                   (0.0, 0.0, 0.0),
#                   (1.0, 1.0, 1.0))}

cmin = 0.0
cmax = 1.0
#mp  = (threshold - cmin) / (cmax - cmin)  # midpoint is where the white will appear
mp  = (threshold - cmin) / (cmax - cmin)  # midpoint is where the white will appear
tol = 0.02
if mp > 0.9 or mp < 0.1:
    print "threshold = " + str(threshold) + "is too high or low"
    exit()

cdict = {'red': [(0.0,      1.0, 1.0),
                 ( mp-tol,  1.0, 1.0),
                 ( mp,      1.0, 1.0),
                 ( mp+tol,  0.7, 0.7),
                 (1.0,      0.0, 0.0)],

       'green': [(0.0,      0.0, 0.0),
                 ( mp-tol,  0.7, 0.7),
                 ( mp,      1.0, 1.0),
                 ( mp+tol,  0.7, 0.7),
                 (1.0,      0.0, 0.0)],

       'blue':  [(0.0,      0.0, 0.0),
                 ( mp-tol,  0.7, 0.7),
                 ( mp,      1.0, 1.0),
                 ( mp+tol,  1.0, 1.0),
                 (1.0,      1.0, 1.0)]}


my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,20)

im = axmatrix.imshow(X, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)


#im.set_clim(0,threshold)
#im.set_clim(threshold,1)
im.set_clim(cmin,cmax)
axmatrix.set_ylim(-0.5, m-0.5)
axmatrix.set_xlim(-0.5, n-0.5)
#axmatrix.set_yticks([])
#axmatrix.set_xticks([])

axmatrix.set_xticks(range(0,m))
axmatrix.set_xticklabels(labels_sort)
axmatrix.set_yticks(range(0,m))
axmatrix.set_yticklabels(labels_sort)

for i in range(0,m):
    labels = axmatrix.xaxis.get_major_ticks()[i].label
    labels.set_fontsize(10)
    labels.set_rotation('vertical')
    labels = axmatrix.yaxis.get_major_ticks()[i].label
    labels.set_fontsize(10)





# Plot colorbar.
axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
pylab.colorbar(im, cax=axcolor)
fig.show()
#fig.show()
fig.savefig('dendrogram.png',dpi=600)

