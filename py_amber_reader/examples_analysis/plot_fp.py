
## uses local version of python on sublime

import sys
import copy
import  matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running
import math, scipy, pylab, numpy

## Writen by Trent Balius in the Shoichet Group


def readmatrix(filehandel):
    matrix = []
    #label1   = []
    #label2   = []
    maxval = -10000.
    minval = 10000.0
    for line in filehandel:
        if ("Frame" in line) or ("AVG" in line): 
            continue
        #line = replace_char(line,'>',' ')
        #line = replace_char(line,';',' ')
        splitline = line.split(',')
        row = []
        for val in splitline:
            #print val, " ",
            fval = float(val)
            if fval > maxval: 
               maxval = fval
            if fval < minval:
               minval = fval
            row.append(fval)
        matrix.append(row)
        #print "\n"
        #label1.append(splitline[0])
        #label2.append(splitline[1])
    print "min, max = ",minval, maxval

    return matrix #,label1,label2

def mat_to_mat(mat):

     m = len(mat)
     n = len(mat[0])
     if n !=1: 
        print "not footprint but heatmap."
        exit()

     mat2 = numpy.zeros([m,n]) 
     vec1 = numpy.zeros(m) 
     vec2 = numpy.zeros(n) 

     for i in range(m):
         for j in range(n):
             mat2[i,j] = mat[i][j]
             vec1[i] = vec1[i] + mat[i][j] 
             vec2[j] = vec2[j] + mat[i][j] 

     return mat2, vec1, vec2

def mat_larger_mag(mat,lab1,lab2,thrsmax,thrsmin):

     m = len(mat)
     n = len(mat[0])
     lm = len(lab1)
     ln = len(lab2)
     print n,m,ln,lm

     for i in range(m):
         for j in range(n):
             #print lab1[i],lab2[j], mat[i][j], thrsmax,thrsmin
             if mat[i][j]>thrsmax or mat[i][j]<thrsmin : 
                print lab1[i],lab2[j], mat[i][j]


#def heatmap(Mat,label,filename,threshold,heatmap_threshold):
def heatmap(Mat0,filename,heatmap_threshold,cmin,cmax,lab1file,lab2file):
     m = len(Mat0)
     n = len(Mat0[0])
     print m,n

     Mat, vec1, vec2 = mat_to_mat(Mat0) 
     #flabel1 = open('../resnames.1.txt','r')
     #flabel2 = open('../resnames.2.txt','r')
     flabel1 = open(lab1file,'r')
     flabel2 = open(lab2file,'r')
     xlabel = []
     for line in flabel2:
          xlabel.append(line.split()[0])
     ylabel = []
     for line in flabel1:
          ylabel.append(line.split()[0])
     flabel1.close()
     flabel2.close()

     mat_larger_mag(Mat0,ylabel,xlabel,cmax,cmin)

     fig = pylab.figure(figsize=(8,8))

     ax2 = fig.add_axes([0.3,0.75,0.6,0.2])
     print vec1
     matplotlib.pyplot.plot(range(0,m),vec1,'k-') # draws a datshed line where dendogram is cut.
     ax2.set_xticks([])
     #ax2.set_yticks([])
     ax2.set_xlim(-0.5, m-0.5)
     ax2.set_ylim(cmin,cmax)
        
     ax2.set_xticks(range(0,m))
     ax2.set_xticklabels(ylabel)
     for i in range(m):
         labels = ax2.xaxis.get_major_ticks()[i].label
         labels.set_fontsize(3)
         labels.set_rotation('vertical')
     # write out vector to file
     print len(vec1), len(ylabel)
     print len(vec2), len(xlabel)

     fh = open(filename+'.vec2.txt','w')
     for i in range(len(vec2)):
         fh.write('%s,%f\n'%(xlabel[i],vec2[i]))
     fh.close()

     fh = open(filename+'.vec1.txt','w')
     for i in range(len(vec1)):
         fh.write('%s,%f\n'%(ylabel[i],vec1[i]))
     fh.close()
 
     fig.savefig(filename,dpi=600)

     return


def main():
  if len(sys.argv) != 7: # if no input
     print "syntax:  filename_prefix, heatmap_threshold heatmap_min heatmap_max label1_filename label2_filename"
     print "Error:  you have entered the wrong number of inputs:"
     print len(sys.argv)

  print "You have entered in 3 inputs:"
  file1name  = sys.argv[1] 
  heatmap_threshold  = float(sys.argv[2])
  vmin               = float(sys.argv[3])
  vmax               = float(sys.argv[4])
  lab1               = sys.argv[5] 
  lab2               = sys.argv[6] 
  print "input matrix file = " + file1name
  file1handel = open(file1name,'r')
  m = readmatrix(file1handel)
  #write_matrix(file2handel,m)
  file1handel.close()
  heatmap(m,file1name+'.png',heatmap_threshold,vmin,vmax,lab1,lab2)
  return
  #SimlesToFingerPrint("CCC") 
  #SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
  ###SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
 
main()

