
## uses local version of python on sublime

import sys
import copy

import math, matplotlib, scipy, pylab,numpy
import scipy.cluster.hierarchy as sch


## Writen by Trent Balius in the Shoichet Group
## this script reads in a text file with 3 columns 
## label1 label2 RMSD
## The script uses scipy.cluster to perform hierarchal clustering 
## on the RMSD matrix
## this was written to help Matt Merski perform clustering analysis.

class INDEX_FLOAT:
    def __init__(self, index, float_val):
        self.index = index
        self.float_val =  float_val
    def __cmp__(self, other):
        return cmp(self.float_val, other.float_val)
# this defines a compares two LIG_DATA by comparing the two scores
# it is sorted in decinding order.
def byScore(x, y):
    return cmp(x.float_val, y.float_val)


def replace_char(string1,char_old,char_new):
    string_new = ''
    for char in string1:
        #print char
        if char != char_old:
           string_new = string_new+char
        else:
           string_new = string_new+char_new
    return string_new    
    

def readindex(filehandel):
    index   = []
    for line in filehandel:
        splitline = line.split()
        index.append(int(splitline[0]))
        #print splitline[1]
    return index


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
    #M = round(math.sqrt(N))
    M = int(math.sqrt(N))

    ## label = label2[0:M]
    label = []
    for i in range(M):
       label.append(label2[i])
    return rmsdlist, label

# this function reads in a list of lenght N; N = MXM
# And returns a MXM matrix 
def vec_to_mat(rmsdlist):

    N = len(rmsdlist)
    #M = math.sqrt(N)
    M = int(math.sqrt(N))
    print N, M 
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

def array_to_vector(array):
    print "In array_to_vector"
    m = len(array)
    print m
    vec = scipy.zeros([m,1])

    ## converts from an array to Scipy vec
    for i in range(0,m):
        vec[i] = array[i]
    print min(vec), max(vec)
    return vec

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

def heatmap(Mat,label,bool_sort,filename,threshold,heatmap_threshold,IND):
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

     print IND
     print "#### index"
     count = 0
     for i in IND:
         print i
     print "#####"

     if (bool_sort):
         Mat, Matvec = mat_to_vector(Mat)
         Mat = mat_to_mat(Mat)
         xlabel_new = []
         print "#######"
         write_matrix(sys.stdout,Mat) 
         Mat = Mat[IND,:]
         Mat = Mat[:,IND]
         print "#######"
         write_matrix(sys.stdout,Mat) 
         #info_rmsd = info_rmsd[:,IND]
         for i in range(len(IND)):
             xlabel_new.append(xlabel[IND[i]])
         axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])

     #cmin = 0.0
     #cmax = 4.0 
     cmin = 1.0
     cmax = 3.0 
     #mp  = (threshold - cmin) / (cmax - cmin)  # midpoint is where the white will appear
     mp  = (heatmap_threshold - cmin) / (cmax - cmin)  # midpoint is where the white will appear
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

 
 
     my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,100)
    
     im = axmatrix.imshow(Mat, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)

     if (bool_sort):
         v = range(0,n)
         axmatrix.plot(v,v,'yo',markersize=2)
         

     im.set_clim(cmin,cmax)
     axmatrix.set_xlim(-0.5, n-0.5)
     axmatrix.set_ylim(-0.5, n-0.5)
     axmatrix.set_xticks(range(0,m))
     axmatrix.set_xticklabels(xlabel_new)
     axmatrix.set_yticks(range(0,m))
     axmatrix.set_yticklabels(xlabel_new)

#     if (not bool_sort):
#         axmatrix.set_yticks(range(0,n))
#         axmatrix.set_yticklabels(ylabel)
#         for i in range(0,n):
#             labels = axmatrix.yaxis.get_major_ticks()[i].label
#             labels.set_fontsize(4)
#     else:
#         axmatrix.set_yticks([])
     
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
     fig.savefig(filename,dpi=600)

     return



def main():
  if len(sys.argv) != 6: # if no input
     print "syntax:  matt_rmsd_cluster.py rmsd.txt index.txt matrix threshold (cut dendogram) threshold (color_heatmap)"
     print "Error:  you have entered the wrong number of inputs:"
     print len(sys.argv)

  print "You are entered in 5 inputs:"
  file1name  = sys.argv[1] 
  file2name  = sys.argv[2] # index 
  file3name  = sys.argv[3] 
  threshold  = float(sys.argv[4])
  heatmap_threshold  = float(sys.argv[5])
  file3name = file3name+"_t"+str(threshold) ## add the treshold to filename
  print "input rmsdfile     = " + file1name
  print "input index file   = " + file2name
  print "output matrix file = " + file3name
  file1handel = open(file1name,'r')
  file2handel = open(file2name,'r')
  file3handel = open(file3name,'w')
  rmsdlist,label = readrmsd(file1handel)
  index = readindex(file2handel)
  m = vec_to_mat(rmsdlist)
  write_matrix(file3handel,m)
  file1handel.close()
  file2handel.close()
  file3handel.close()
  heatmap(m,label,True,file3name+'.png',threshold,heatmap_threshold,index)
  return
main()

