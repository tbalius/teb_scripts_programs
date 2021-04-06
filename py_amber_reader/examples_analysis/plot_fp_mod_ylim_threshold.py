
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

def plot_data_subplot(vec1,xlabel1, ylim_val, ax1):
     m = len(vec1)
     matplotlib.pyplot.plot(range(0,m),vec1,'k-o') # draws a datshed line where dendogram is cut.
     ax1.set_xlim(-0.5, m+0.5)
     ax1.set_ylim(-ylim_val,ylim_val)
        
     ax1.set_xticks(range(0,m))
     ax1.set_xticklabels(xlabel1)
     for i in range(m):
         labels = ax1.xaxis.get_major_ticks()[i].label
         labels.set_fontsize(8)
         labels.set_rotation('vertical')
     ## write out vector to file
     #print len(vec1), len(ylabel)
     #print len(vec2), len(xlabel)

     #fh = open(filename+'.vec2.txt','w')

def plot_data(vec1,index,filename,lab1file, ylim_val):
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
     ax1 = fig.add_axes([0.1,0.5,0.9,0.4])
     sub_vec1 = []
     sub_lab1 = []     
     for i in index:
         sub_vec1.append(vec1[i])
         sub_lab1.append(xlabel[i])
     plot_data_subplot(sub_vec1,sub_lab1, ylim_val, ax1)

     #ax2 = fig.add_axes([0.5,0.5,0.4,0.4])
     #sub_vec2 = []
     #sub_lab2 = []     
     #for i in range(start2-1,stop2):
     #    sub_vec2.append(vec1[i])
     #    sub_lab2.append(xlabel[i])
     #plot_data_subplot(sub_vec2,sub_lab2, ylim_val, ax2)
     #ax2.set_yticklabels("")
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
  if len(sys.argv) != 5: # if no input
  #if len(sys.argv) != 2: # if no input
     print "syntax:  filename_prefix, label1_filename, y-axis_max_val threshold"
     #print "syntax:  filename_prefix"
     print "Error:  you have entered the wrong number of inputs:"
     print len(sys.argv)

  print "You have entered in 3 inputs:"
  file1name  = sys.argv[1] 
  lab1       = sys.argv[2] 
  ylim_v     = float(sys.argv[3])
  threshold   = float(sys.argv[4])
  if ylim_v < 0: 
     print("error: ylim_v < 0. ")
     exit()
  #heatmap_threshold  = float(sys.argv[2])
  #vmin               = float(sys.argv[3])
  #vmax               = float(sys.argv[4])
  #lab1               = sys.argv[5] 
  #lab2               = sys.argv[6] 

  

  print "input matrix file = " + file1name
  file1handel = open(file1name+'.txt','r')
  m = read_vec(file1handel)

  index = []
  for i in range(len(m)):
       if (math.fabs(m[i])>threshold):
          index.append(i)

  file1handel.close()
  plot_data(m,index,file1name+'thres.png',lab1,ylim_v)
  return
  #SimlesToFingerPrint("CCC") 
  #SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
  ###SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
 
main()

