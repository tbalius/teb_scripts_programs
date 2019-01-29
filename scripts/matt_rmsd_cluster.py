
## uses local version of python on sublime

import sys

import math, matplotlib, scipy, pylab
import scipy.cluster.hierarchy as sch


## Writen by Trent Balius in the Shoichet Group
## this script reads in a text file with 3 columns 
## label1 label2 RMSD
## The script uses scipy.cluster to perform hierarchal clustering 
## on the RMSD matrix
## this was written to help Matt Merski perform clustering analysis.

def replace_char(string1,char_old,char_new):
    string_new = ''
    for char in string1:
        #print char
        if char != char_old:
           string_new = string_new+char
        else:
           string_new = string_new+char_new
    return string_new    
    

def readrmsd(filehandel):
    rmsdlist = []
    label1   = []
    label2   = []
    for line in filehandel:
        #splitline = line.split()
        #print line
        line = replace_char(line,'>',' ')
        line = replace_char(line,';',' ')
        splitline = line.split()
        rmsdlist.append(float(splitline[2]))
        label1.append(splitline[0])
        label2.append(splitline[1])
        #print splitline[1] 

    N = len(rmsdlist) 
    M = math.sqrt(N)

    ## label = label2[0:M]
    label = []
    for i in range(M):
       label.append(label2[i])
    return rmsdlist, label

# this function reads in a list of lenght N; N = MXM
# And returns a MXM matrix 
def vec_to_mat(rmsdlist):

    N = len(rmsdlist)
    M = math.sqrt(N)
    m = []

    count = 0
    for i in range(M):
        row = []
        for j in range(M):
            row.append(rmsdlist[count])
            count = count + 1
        m.append(row)

    return m

def write_matrix(filehandel,Matrix):
    for i in range(len(Matrix)):
        for j in range(len(Matrix[i])):
            if (j == 0):
                filehandel.write('%f' % (Matrix[i][j]))
            filehandel.write(',%f' % (Matrix[i][j]))
        filehandel.write('\n')

def mat_to_mat(Mat):
    m = len(Mat)
    n = len(Mat[0])

    if (m != n):
        print "inconsitancy in numbers of rows and columns in the matrix."

    print m,n

    X = scipy.zeros([m,n])

    ## converts from a 2D array to Scipy Matrix 
    for i in range(0,m):
        for j in range(0,n):
               ## 1 - tc is more like a distance than tc.
               #X[i,j] = -Mat[i][j] + 1.0 # for tanimoto
               X[i,j] = Mat[i][j]

    return X


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

def heatmap(Mat,label,bool_sort,filename,threshold):
     m = len(Mat)
     n = len(Mat[0])
     print m,n

     #xlabel = [] 
     #for i in range(0,m):
     #   xlabel.append('lig_'+str(i+1))
     #ylabel = []
     #for i in range(0,n):
     #   ylabel.append('lig_'+str(i+1))
     xlabel = label
     ylabel = label

     fig = pylab.figure(figsize=(8,8))

     if (bool_sort):
         Mat, Matvec = mat_to_vector(Mat)
        #Y = sch.linkage(Matvec, method='single')
        #Y = sch.linkage(Matvec, method='average')
         Y = sch.linkage(Matvec, method='complete')
        #Y = sch.linkage(Matvec, method='centroid')
        #Y = sch.linkage(Matvec, method='median')
         #help(sch.linkage)
         #threshold = 1.0 # good for single
         #threshold = 0.5 # good for single
         #threshold = 1.5 # good for average
         #threshold = 2.35 # good for complete
         #threshold = 3.0 # good for complete
         #threshold = 2.0 # good for complete
         clusters = sch.fcluster(Y, threshold, 'distance')
         print clusters
         for i in range(len(label)):
             print label[i] + " " + str(clusters[i])
 

         ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
         Z1 = sch.dendrogram(Y, orientation='right',color_threshold=threshold)
         matplotlib.pyplot.plot([threshold,threshold],[0,10*len(label)],'k--') # draws a datshed line where dendogram is cut.
         #help(sch.dendrogram)
         ax1.set_xticks([])
         ax1.set_yticks([])
        
         # Compute and plot second dendrogram.
         ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
         Z2 = sch.dendrogram(Y,color_threshold=threshold)
         matplotlib.pyplot.plot([0,10*len(label)],[threshold,threshold],'k--') # draws a datshed line where dendogram is cut.
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
         clusters_new = []
         for i in range(len(idx2)):
             xlabel_new.append(xlabel[idx2[i]])
             clusters_new.append(clusters[idx2[i]])
         del xlabel[:]
         xlabel = xlabel_new

         print "systems sorted:"
         for i in range(len(xlabel)):
             print xlabel[i] + " " + str(clusters_new[i]) 

     else:
         Mat = mat_to_mat(Mat)
         axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])

     #cdict = {'red': ((0.0, 0.0, 0.0),
     #                  (0.0, 0.0, 0.0),
     #                  (1.0, 1.0, 1.0)),
     #          'green': ((0.0, 0.0, 0.0),
     #                    (0.0, 0.0, 0.0),
     #                    (1.0, 1.0, 1.0)),
     #          'blue': ((0.0, 0.0, 0.0),
     #                   (0.0, 0.0, 0.0),
     #                   (1.0, 1.0, 1.0))}
     
     #cdict = {'red':   [(0.0,  0.0, 0.0),
     #              (0.5,  1.0, 1.0),
     #              (1.0,  1.0, 1.0)],
     #
     #    'green': [(0.0,  0.0, 0.0),
     #              (0.25, 0.0, 0.0),
     #              (0.75, 1.0, 1.0),
     #              (1.0,  1.0, 1.0)],
     #
     #    'blue':  [(0.0,  0.0, 0.0),
     #              (0.5,  0.0, 0.0),
     #              (1.0,  1.0, 1.0)]}  


     ## red - white - blue
     # colorbar is from 0 to 5
     # I want the white to appare at the threshold value 
     # midpoint  : threshodl
     # 0.0       =  0.0
     # 0.2       = ~1.0
     # 0.5       =  2.5
     # 0.8       = ~4.0
     # 1.0       =  5.0
     cmin = 1.0
     cmax = 3.0 
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

     ## blue - purple - red
     #cdict = {'red': [(0.0,  0.0, 0.0),
     #                 (0.5,  0.5, 0.5),
     #                 (1.0,  1.0, 1.0)],
     #
     #       'green': [(0.0,  0.0, 0.0),
     #                 (1.0,  0.0, 0.0)],
     #
     #       'blue':  [(0.0,  1.0, 1.0),
     #                 (0.5,  0.5, 0.5),
     #                 (1.0,  0.0, 0.0)]}

 
 
     my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,100)
    
     im = axmatrix.imshow(Mat, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)

     if (bool_sort):
         v = range(0,n)
         axmatrix.plot(v,v,'yo',markersize=2)
         

     im.set_clim(cmin,cmax)
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
         label.set_fontsize(3)
         label.set_rotation('vertical')
    
     # Plot colorbar.
     axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
     pylab.colorbar(im, cax=axcolor)
     fig.show()
     fig.savefig(filename,dpi=600)


def main():
  if len(sys.argv) != 4: # if no input
     print "Error:  you have entered the wrong number of inputs:"
     print len(sys.argv)
     print "syntax:  matt_rmsd_cluster.py rmsd.txt matrix threshold (cut dendogram)"

  print "You are entered in 2 inputs:"
  file1name  = sys.argv[1] 
  file2name  = sys.argv[2] 
  threshold  = float(sys.argv[3])
  file2name = file2name+"_t"+str(threshold) ## add the treshold to filename
  print "input rmsdfile = " + file1name
  print "output matrix file = " + file2name
  file1handel = open(file1name,'r')
  file2handel = open(file2name,'w')
  rmsdlist,label = readrmsd(file1handel)
  m = vec_to_mat(rmsdlist)
  write_matrix(file2handel,m)
  file1handel.close()
  file2handel.close()
  heatmap(m,label,True,file2name+'.png',threshold)
  return
  #SimlesToFingerPrint("CCC") 
  #SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
  ###SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
 
main()

