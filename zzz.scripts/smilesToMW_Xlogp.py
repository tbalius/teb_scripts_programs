
## uses local version of python on sublime

import sys, pybel, openbabel

import math, matplotlib, scipy, pylab
import scipy.cluster.hierarchy as sch


## Writen by Trent Balius in the Shoichet Group
## note that open babel must be installed to run this script
## take as input a sets of smiles converts them to a MACS fingerprint and 
## calculates the tanimoto matrix. 
## it will produce hemaps.

def SimlesToFingerPrint(string):
   ## this funtion calculates fingerprints using 
   ## open babel.
   mol = pybel.readstring('smi',string)
   fp = mol.calcfp('MACCS')
#   fp = mol.calcfp('FP2')
   return fp

def makeFingerPrintArray(filehandel):
  lines = filehandel.readlines()
  fplist = []
  smileslist = []
  for line in lines:
      #smiles = line.strip()  ## remove white space and new lines
      smiles = line.split(';')[0] 
      fp = SimlesToFingerPrint(smiles)
      fplist.append(fp)
      smileslist.append(smiles)
  return fplist

def makeTanimotoMatrixSquare(fingerprints):
    if len(fingerprints) == 1:
        print "fingerprints is size 1"

    ## intialize matrix
    matrix = []
    for i in range(len(fingerprints)):
        row = []
        for j in range(len(fingerprints)):
            row.append(0)
        matrix.append(row)

    ## fill matrix
    for i in range(len(fingerprints)):
        matrix[i][i] = fingerprints[i] | fingerprints[i]
        #matrix[i][i] = 1
        for j in range(i,len(fingerprints)):
            tc = fingerprints[i] | fingerprints[j]
            matrix[i][j] = tc
            matrix[j][i] = tc #fingerprints[j] | fingerprints[i]
    return matrix    

def makeTanimotoMatrix(fingerprints1,fingerprints2):
    if len(fingerprints1) == 1 or len(fingerprints2) == 1:
        print "fingerprints is size 1"

    ## intialize matrix
    print "makeing a " + str(len(fingerprints1)) + "X" + str(len(fingerprints1)) + "Matrix. "
    matrix = []
    for i in range(len(fingerprints1)):
        row = []
        for j in range(len(fingerprints2)):
            row.append(0)
        matrix.append(row)

    ## fill matrix
    for i in range(len(fingerprints1)):
        for j in range(len(fingerprints2)):
            tc = fingerprints1[i] | fingerprints2[j]
            matrix[i][j] = tc
    return matrix



def write_matrix(filehandel,Matrix):
    for i in range(len(Matrix)):
        for j in range(len(Matrix[i])):
            if (j == 0):
                filehandel.write('%f' % (Matrix[i][j]))
            filehandel.write(',%f' % (Matrix[i][j]))
        filehandel.write('\n')

def mat_to_mat(Mat):
    #print "I AM HERE in mat_to_mat(Mat)"
    ## 1 - tc is more like a distance than tc.
    m = len(Mat)
    n = len(Mat[0])

    if (m != n):
        print "inconsitancy in numbers of rows and columns in the matrix."

    print m,n

    X = scipy.zeros([m,n])

    ## converts from a 2D array to Scipy Matrix 
    for i in range(0,m):
        for j in range(0,n):
               X[i,j] = -Mat[i][j] + 1.0

    return X


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
               X[i,j] = -Mat[i][j] + 1.0

    for i in range(0,n):
        for j in range(i+1,n):
               Xvec[count2] = -Mat[i][j] + 1.0
               count2 = count2+1

    return X,Xvec

def heatmap_sym(Mat,filename):
     m = len(Mat)
     n = len(Mat[0])
     print m,n

     xlabel = [] 
     for i in range(0,m):
        xlabel.append('lig_'+str(i+1))
     ylabel = []
     for i in range(0,n):
        ylabel.append('lig_'+str(i+1))

     fig = pylab.figure(figsize=(8,8))

     Mat, Matvec = mat_to_vector(Mat)
     Y = sch.linkage(Matvec, method='single')
     threshold = 0.2
     clusters = sch.fcluster(Y, threshold, 'distance')
     print clusters

     ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
     Z1 = sch.dendrogram(Y, orientation='right')
     #help(sch.dendrogram)
     ax1.set_xticks([])
     ax1.set_yticks([])
    
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
     Mat = Mat[idx1,:]
     Mat = Mat[:,idx2]
     #xlabel[:] = xlabel[idx2]
     xlabel_new = []
     for i in range(len(idx2)):
         xlabel_new.append(xlabel[idx2[i]])
     del xlabel[:]
     xlabel = xlabel_new

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
    
     im = axmatrix.imshow(Mat, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)

     v = range(0,n)
     axmatrix.plot(v,v,'yo',markersize=2)
         

     im.set_clim(0,1)
     axmatrix.set_xlim(-0.5, n-0.5)
     axmatrix.set_ylim(-0.5, n-0.5)
     axmatrix.set_xticks(range(0,m))
     axmatrix.set_xticklabels(xlabel)

     axmatrix.set_yticks([])
     
     for i in range(0,m):
         label = axmatrix.xaxis.get_major_ticks()[i].label
         label.set_fontsize(4)
         label.set_rotation('vertical')
    
     # Plot colorbar.
     axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
     pylab.colorbar(im, cax=axcolor)
     fig.show()
     fig.savefig(filename,dpi=600)

     return idx1 

def heatmap_not_sym(Mat,filename,idx1,idx2):
     m = len(Mat)
     n = len(Mat[0])
     print m,n

     #print 'test',len(idx1),len(idx2)

     ylabel = []
     xlabel = [] 
     for i in range(0,m):
        ylabel.append('lig_'+str(idx1[i]+1))
     for i in range(0,n):
        xlabel.append('lig_'+str(idx2[i]+1))

     fig = pylab.figure(figsize=(8,8))

     Mat = mat_to_mat(Mat)
     Mat = Mat[idx1,:]
     Mat = Mat[:,idx2]

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
    
     im = axmatrix.imshow(Mat, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)

     im.set_clim(0,1)
     axmatrix.set_xlim(-0.5, n-0.5)
     axmatrix.set_ylim(-0.5, n-0.5)
     axmatrix.set_xticks(range(0,n))
     axmatrix.set_xticklabels(xlabel)

     axmatrix.set_yticks(range(0,m))
     axmatrix.set_yticklabels(ylabel)
     for i in range(0,m):
         label = axmatrix.yaxis.get_major_ticks()[i].label
         label.set_fontsize(4)
     
     for i in range(0,n):
         label = axmatrix.xaxis.get_major_ticks()[i].label
         label.set_fontsize(4)
         label.set_rotation('vertical')
    
     # Plot colorbar.
     axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
     pylab.colorbar(im, cax=axcolor)
     fig.show()
     fig.savefig(filename,dpi=600)


def heatmap(Mat,bool_sort,filename):
     m = len(Mat)
     n = len(Mat[0])
     print m,n

     xlabel = [] 
     for i in range(0,m):
        xlabel.append('lig_'+str(i+1))
     ylabel = []
     for i in range(0,n):
        ylabel.append('lig_'+str(i+1))

     fig = pylab.figure(figsize=(8,8))

     if (bool_sort):
         Mat, Matvec = mat_to_vector(Mat)
         Y = sch.linkage(Matvec, method='single')
         threshold = 0.2
         clusters = sch.fcluster(Y, threshold, 'distance')
         print clusters

         ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
         Z1 = sch.dendrogram(Y, orientation='right')
         #help(sch.dendrogram)
         ax1.set_xticks([])
         ax1.set_yticks([])
        
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
         Mat = Mat[idx1,:]
         Mat = Mat[:,idx2]
         #xlabel[:] = xlabel[idx2]
         xlabel_new = []
         for i in range(len(idx2)):
             xlabel_new.append(xlabel[idx2[i]])
         del xlabel[:]
         xlabel = xlabel_new

     else:
         Mat = mat_to_mat(Mat)
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
    
     im = axmatrix.imshow(Mat, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)

     if (bool_sort):
         v = range(0,n)
         axmatrix.plot(v,v,'yo',markersize=2)
         

     im.set_clim(0,1)
     axmatrix.set_xlim(-0.5, n-0.5)
     axmatrix.set_ylim(-0.5, n-0.5)
     axmatrix.set_xticks(range(0,m))
     axmatrix.set_xticklabels(xlabel)

     if (not bool_sort):
         axmatrix.set_yticks(range(0,n))
         axmatrix.set_yticklabels(ylabel)
         for i in range(0,n):
             label = axmatrix.yaxis.get_major_ticks()[i].label
             label.set_fontsize(4)
     else:
         axmatrix.set_yticks([])
     
     for i in range(0,m):
         label = axmatrix.xaxis.get_major_ticks()[i].label
         label.set_fontsize(4)
         label.set_rotation('vertical')
    
     # Plot colorbar.
     axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
     pylab.colorbar(im, cax=axcolor)
     fig.show()
     fig.savefig(filename,dpi=600)


def main():
  if len(sys.argv) == 3: # if no input
     print "You are entered in 2 inputs:"
     file1name  = sys.argv[1] 
     file2name  = sys.argv[2] 
     print "input smilesfile = " + file1name
     print "output matrix file = " + file2name
     file1handel = open(file1name,'r')
     file2handel = open(file2name,'w')
     fplist = makeFingerPrintArray(file1handel)
     m = makeTanimotoMatrixSquare(fplist)
     write_matrix(file2handel,m)
     file1handel.close()
     file2handel.close()
     heatmap(m,True,file2name+'.png')
  elif len(sys.argv) == 4:
     print "You are entered in 3 inputs:"
     file1name  = sys.argv[1]
     file2name  = sys.argv[2]
     file3name  = sys.argv[3]
     print "input smilesfile1 = " + file1name
     print "input smilesfile2 = " + file2name
     print "output matrix file = " + file3name
     file1handel = open(file1name,'r')
     file2handel = open(file2name,'r')
     file3handel = open(file3name,'w')
     fplist1 = makeFingerPrintArray(file1handel)
     fplist2 = makeFingerPrintArray(file2handel)
     m = makeTanimotoMatrix(fplist1,fplist2)
     write_matrix(file3handel,m)
     file1handel.close()
     file2handel.close()
     file3handel.close()
     heatmap(m,False,file3name+'.png')

     m1  = makeTanimotoMatrixSquare(fplist1)
     id1 = heatmap_sym(m1,file3name+'.1.png')
     m2  = makeTanimotoMatrixSquare(fplist2)     
     id2 = heatmap_sym(m2,file3name+'.2.png')
     heatmap_not_sym(m,file3name+'.3.png',id1,id2)

  else:
     print "Error:  you have entered the wrong number of inputs:"
     print len(sys.argv)
     print "syntax:  smilesToFPMatrix.py smiles.txt matrix.txt"
     print "syntax:  smilesToFPMatrix.py smiles1.txt smiles2.txt matrix.txt"
  return

  #SimlesToFingerPrint("CCC") 
  #SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
  ###SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
 
main()

