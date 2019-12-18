
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
        #line = replace_char(line,'>',' ')
        #line = replace_char(line,';',' ')
        splitline = line.split(',')
        row = []
        for val in splitline:
            print val, " ",
            fval = float(val)
            if fval > maxval: 
               maxval = fval
            if fval < minval:
               minval = fval
            row.append(fval)
        matrix.append(row)
        print "\n"
        #label1.append(splitline[0])
        #label2.append(splitline[1])
    print "min, max = ",minval, maxval

    return matrix #,label1,label2

def mat_to_mat(mat):

     m = len(mat)
     n = len(mat[0])

     mat2 = numpy.zeros([m,n]) 
     vec1 = numpy.zeros(m) 
     vec2 = numpy.zeros(n) 

     for i in range(m):
         for j in range(n):
             #print i,j,
             #print mat[i][j]
             #print mat[j][i]
             mat2[i,j] = mat[i][j]
             vec1[i] = vec1[i] + mat[i][j] 
             vec2[j] = vec2[j] + mat[i][j] 

     return mat2, vec1, vec2

#def heatmap(Mat,label,filename,threshold,heatmap_threshold):
def heatmap(Mat0,filename,heatmap_threshold,cmin,cmax):
     m = len(Mat0)
     n = len(Mat0[0])
     print m,n

     Mat, vec1, vec2 = mat_to_mat(Mat0) 
     #xlabel = label
     #ylabel = label

     fig = pylab.figure(figsize=(8,8))

     ax1 = fig.add_axes([0.04,0.1,0.2,0.6])
     matplotlib.pyplot.plot(vec1,range(0,m),'k-') # draws a datshed line where dendogram is cut.
     #ax1.set_xticks([])
     ax1.set_yticks([])
     ax1.set_ylim(-0.5, m-0.5)
        
     ax2 = fig.add_axes([0.3,0.75,0.6,0.2])
     matplotlib.pyplot.plot(range(0,n),vec2,'k-') # draws a datshed line where dendogram is cut.
     ax2.set_xticks([])
     #ax2.set_yticks([])
     ax2.set_xlim(-0.5, n-0.5)
        
         # Plot distance matrix.
     axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])

     #cmin = -1.0
     #cmax = 1.0 
     #mp  = (threshold - cmin) / (cmax - cmin)  # midpoint is where the white will appear
     mp  = (heatmap_threshold - cmin) / (cmax - cmin)  # midpoint is where the white will appear
     tol = 0.02
     if mp > 0.9 or mp < 0.1:
         print "threshold = " + str(heatmap_threshold) + "is too high or low" 
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

     #v = range(0,n)
     #axmatrix.plot(v,v,'yo',markersize=2)
         

     im.set_clim(cmin,cmax)
     axmatrix.set_xlim(-0.5, n-0.5)
     axmatrix.set_ylim(-0.5, m-0.5)
     #axmatrix.set_xticks(range(0,m))
     #axmatrix.set_xticklabels(xlabel)

     #   labels = axmatrix.xaxis.get_major_ticks()[i].label
     #   labels.set_fontsize(3)
     #   labels.set_rotation('vertical')
    
     # Plot colorbar.
     axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
     pylab.colorbar(im, cax=axcolor)
     fig.show()
     fig.savefig(filename,dpi=600)

     return


def main():
  if len(sys.argv) != 5: # if no input
     print "syntax:  filename_prefix, heatmap_threshold heatmap_min heatmap_max"
     print "Error:  you have entered the wrong number of inputs:"
     print len(sys.argv)

  print "You are entered in 3 inputs:"
  file1name  = sys.argv[1] 
  heatmap_threshold  = float(sys.argv[2])
  vmin               = float(sys.argv[3])
  vmax               = float(sys.argv[4])
  print "input matrix file = " + file1name
  file1handel = open(file1name+'.txt','r')
  m = readmatrix(file1handel)
  #write_matrix(file2handel,m)
  file1handel.close()
  heatmap(m,file1name+'.png',heatmap_threshold,vmin,vmax)
  return
  #SimlesToFingerPrint("CCC") 
  #SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
  ###SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
 
main()

