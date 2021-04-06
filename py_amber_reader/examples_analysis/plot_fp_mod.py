
## uses local version of python on sublime

import sys
import copy
import  matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running
import math, scipy, pylab, numpy

## Writen by Trent Balius in the Shoichet Group


def read_vec(filehandel):
    vec = []
    #label1   = []
    #label2   = []
    maxval = -10000.
    minval = 10000.0
    for line in filehandel:
        if ("Frame" in line) or ("AVG" in line): 
            continue
        splitline = line.split(',')
        val = splitline[0]
        fval = float(val)
        if fval > maxval: 
           maxval = fval
        if fval < minval:
           minval = fval
        vec.append(fval)
    print "min, max = ",minval, maxval

    return vec #,label1,label2


def plot_data(vec1,filename,lab1file):
#def plot_data(vec1,filename):
     m = len(vec1)

     print("open "+lab1file)
     flabel1 = open(lab1file,'r')

     xlabel = []
     for line in flabel1:
          if len(line.split())==0:
              continue
          print(line)
          xlabel.append(line.split()[0])
     flabel1.close()

     fig = pylab.figure(figsize=(8,8))

     #ax2 = fig.add_axes([0.3,0.75,0.6,0.2])
     ax2 = fig.add_axes([0.05,0.5,0.9,0.4])
     print vec1
     matplotlib.pyplot.plot(range(0,m),vec1,'k-') # draws a datshed line where dendogram is cut.
     #ax2.set_xticks([])
     #ax2.set_yticks([])
     ax2.set_xlim(-0.5, m-0.5)
     #ax2.set_ylim(cmin,cmax)
        
     ax2.set_xticks(range(0,m))
     ax2.set_xticklabels(xlabel)
     for i in range(m):
         labels = ax2.xaxis.get_major_ticks()[i].label
         labels.set_fontsize(3)
         labels.set_rotation('vertical')
     ## write out vector to file
     #print len(vec1), len(ylabel)
     #print len(vec2), len(xlabel)

     #fh = open(filename+'.vec2.txt','w')
     #for i in range(len(vec2)):
     #    fh.write('%s,%f\n'%(xlabel[i],vec2[i]))
     #fh.close()

     #fh = open(filename+'.vec1.txt','w')
     #for i in range(len(vec1)):
     #    fh.write('%s,%f\n'%(ylabel[i],vec1[i]))
     #fh.close()
 
     fig.savefig(filename,dpi=600)

     return


def main():
  if len(sys.argv) != 3: # if no input
  #if len(sys.argv) != 2: # if no input
     print "syntax:  filename_prefix, label1_filename"
     #print "syntax:  filename_prefix"
     print "Error:  you have entered the wrong number of inputs:"
     print len(sys.argv)

  print "You have entered in 3 inputs:"
  file1name  = sys.argv[1] 
  lab1               = sys.argv[2] 
  #heatmap_threshold  = float(sys.argv[2])
  #vmin               = float(sys.argv[3])
  #vmax               = float(sys.argv[4])
  #lab1               = sys.argv[5] 
  #lab2               = sys.argv[6] 
  print "input matrix file = " + file1name
  file1handel = open(file1name+'.txt','r')
  m = read_vec(file1handel)
  file1handel.close()
  plot_data(m,file1name+'.png',lab1)
  return
  #SimlesToFingerPrint("CCC") 
  #SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
  ###SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
 
main()

