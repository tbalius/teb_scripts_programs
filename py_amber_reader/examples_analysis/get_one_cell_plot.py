
## uses local version of python on sublime

import sys
import copy

#import math, matplotlib, scipy, pylab, numpy

import  matplotlib

matplotlib.use('Agg')  # allows you to not have an x-server running

import math, scipy, pylab, numpy

## Writen by Trent Balius in the Shoichet Group


def readmatrix_one_cell(filehandel,si,sj):
    # si is the user specified i value
    # sj is the user specified j value
    print "Here in readmatrix_one_cell"
    i = 0
    fval = 0.0
    flagfound = False
    flagfirst = True
    for line in filehandel:
        if flagfirst:
            print line
            flagfirst=False
            continue
        splitline = line.split(',')
        j = 0
        for val in splitline:
            #print val, " ",
            fval = float(val)
            if (i == (si-1) and j == (sj-1)):
                print i,j,fval 
                flagfound = True
                return fval # if we find it we can stop, and break out of the function. 
            j = j + 1
        i = i + 1
    if not flagfound:
       print "i==%d and j ==%d not found"%(si,sj)

    return fval #,label1,label2



#def heatmap(Mat,label,filename,threshold,heatmap_threshold):
def make_plot(val_array,title,filename,start,stop):

     print "Here in make_plot"
     fig = pylab.figure(figsize=(8,8))

     #timearray = numpy.linspace(1,50000,num=len(val_array))
     timearray = numpy.linspace(1,len(val_array),num=len(val_array))
     print timearray[start-1]
     print timearray[stop-1]
     ax1 = fig.add_axes([0.1,0.1,0.6,0.2])
     matplotlib.pyplot.plot(timearray,val_array,'k-') # draws a datshed line where dendogram is cut.
     #ax1.set_xticks([])
     #ax1.set_yticks([])
     ax1.set_title(title)
     #ax1.set_ylim(-0.5, m-0.5)
        
     #axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
     ax2 = fig.add_axes([0.75,0.1,0.2,0.2])
     #hist(val_array)
     n1_1, bins, patches = ax2.hist(val_array, normed=1, histtype='bar',orientation="horizontal")
     #n1_1, bins, patches = ax2.hist(cluster1_1_sci, inbins, normed=1, histtype='bar')
     #matplotlib.pyplot.plot(range(0,n),vec2,'k-') # draws a datshed line where dendogram is cut.
     #ax2.set_xticks([])
     ax2.set_yticks([])
     #ax2.set_xlim(-0.5, n-0.5)
     #fig.show()
     fig.savefig(filename+'.png',dpi=600)   
     return


def main():
  if len(sys.argv) != 8: # if no input
     print "syntax:  filename_prefix, frame start, frame stop, row number, column number, title, output file"
     print "Error:  you have entered the wrong number of inputs:"
     print len(sys.argv)
     exit()

  print "You have entered in %d inputs:"%(len(sys.argv))
  file1name  = sys.argv[1] 
  start     = int(sys.argv[2])
  stop      = int(sys.argv[3])
  row_n     = int(sys.argv[4])
  col_n     = int(sys.argv[5])
  title     = sys.argv[6] 
  output    = sys.argv[7] 

  val_array = []
  for i in range(start,stop+1):
      print "input matrix file prefix = " + file1name+'.'+str(i)
      file1handel = open(file1name+'.'+str(i),'r')
      val = readmatrix_one_cell(file1handel,row_n,col_n)
      file1handel.close()
      val_array.append(val)
  make_plot(val_array,title,output,start,stop)
  #heatmap(m,file1name+'.png',heatmap_threshold,vmin,vmax,lab1,lab2)
  return
  #SimlesToFingerPrint("CCC") 
  #SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
  ###SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
 
main()

