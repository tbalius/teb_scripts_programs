
## uses local version of python on sublime

import sys
import copy

#import math, matplotlib, scipy, pylab, numpy

import  matplotlib

matplotlib.use('Agg')  # allows you to not have an x-server running

import math, scipy, pylab, numpy

## Writen by Trent Balius in the Shoichet Group


def readmatrix_sum(filehandel):
    print ("Here in readmatrix_sum")
    sum_v = 0.0
    flagfound = False
    flagfirst = True
    count = 0
    for line in filehandel:
        #if flagfirst:
        #    flagfirst=False
        #    continue
        splitline = line.strip().split(',')
        for val in splitline:
            #print (val, float(val))
            #sum_v = sum_v + (float(val)/2.0)
            sum_v = sum_v + (float(val))
            count = count + 1
    
    print ("sum = %f"%sum_v)        
    print (math.sqrt(count))
    return 



def main():
  if len(sys.argv) != 2: # if no input
     print ("syntax:  filename")
     print ("Error:  you have entered the wrong number of inputs:")
     print (len(sys.argv))
     exit()

  print ("You have entered in %d inputs:"%(len(sys.argv)))
  file1name  = sys.argv[1] 

  file1handel = open(file1name,'r')
  val = readmatrix_sum(file1handel)
  file1handel.close()
  return
 
main()

