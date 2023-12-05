
import matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running
import sys
import copy
import math
import scipy
import numpy
import pylab



def average(X):
    N = len(X)
    if N == 0: 
       print("X = ", X)
       print("N == 0")
       return 0
    sumX = 0.0
    for i in range(N):
        sumX = sumX + X[i]
    return sumX/N 
        

def sliding_wendow(T,F,wendowsize):
    Fsize = len(F)
    if (Fsize < wendowsize): 
       print ("Fsize < windowsize, set windowsize = 2")
       wendowsize = 2
    avg = []
    time = []
    start = 0
    stop = wendowsize
    for i in range(Fsize - wendowsize):
        time.append(T[i])
        #print(i,start, stop)
        avg.append(average(F[start:stop]))
        start = start+1
        stop = stop+1
        if stop > Fsize: 
           print("Warning. stop > Fsize. This should never happen.")
           stop = Fsize
    return time,avg

def ACF(F,offsetstart):
    # offsetstart is the starting time lag
    Fsize = len(F)
    acf = []
    for offset in range(offsetstart,Fsize-1):
        start1 = 0
        stop1 = Fsize-offset
        start2 = offset
        stop2 = Fsize
        X = F[start1:stop1]
        Y = F[start2:stop2]
        #p = numpy.corrcoef([X,Y])
        p = numpy.corrcoef(X,Y)
        print(p)
        print(p[0,1])
        #acf.append(p)
        acf.append(p[0,1])
    return acf

def BASEM_vs_Blocksize(F):
    Flen = len(F)
    maxsize = int(Flen/2)
    size_array = range(1,maxsize)
    BASEM_array = [] 
    for size in size_array:
         BASEM_val = BASEM_mean(F,size)
         BASEM_array.append(BASEM_val)
    return size_array, BASEM_array

def BASEM_mean(F,blocksize):
    Fsize = len(F)
    if (Fsize < blocksize):
       print ("Fsize < blocksize, set blocksize = 2")
       blocksize = 2
    numofblocks = math.floor(Fsize/blocksize)
    remainder = Fsize%blocksize
    print("size of array = %d\nsize of blocks = %d\nnumber of blocks = %d\nremainder to distribute = %d\n"%(Fsize,blocksize,numofblocks,remainder));
    blocks = []
    start = 0
    stop = 0
    for i in range(numofblocks):
        #start = i * blocksize # when i = 0 then start = 0
        start = stop
        stop = start + blocksize
        if i < remainder:
           stop = stop + 1 # distriute the remainder to the frist blocks.
        mean = numpy.mean(F[start:stop])
        #print(len(F[start:stop]),start,stop,mean)
        blocks.append(mean)
    basem = scipy.stats.sem(blocks)
    print("BASEM = %f"%basem)
    return basem

# this one retruns blocks for ploting
def BASEM(F,blocksize):
    Fsize = len(F)
    if (Fsize < blocksize): 
       print ("Fsize < blocksize, set blocksize = 2")
       blocksize = 2
    numofblocks = math.floor(Fsize/blocksize)
    remainder = Fsize%blocksize
    print("size of array = %d\nsize of blocks = %d\nnumber of blocks = %d\nremainder to distribute = %d\n"%(Fsize,blocksize,numofblocks,remainder));
    blocks = []
    start = 0
    stop = 0
    for i in range(numofblocks):
        #start = i * blocksize # when i = 0 then start = 0
        start = stop 
        stop = start + blocksize
        if i < remainder: 
           stop = stop + 1 # distriute the remainder to the frist blocks.  
        mean = numpy.mean(F[start:stop])
        #print(len(F[start:stop]),start,stop,mean)
        blocks.append(mean)
    basem = scipy.stats.sem(blocks)
    print("BASEM = %f"%basem)
    return blocks

def fit_line(t,F):

   #m, b = numpy.polyfit(x, y, 1)
   m, b = numpy.polyfit(t, F, 1)
   print ("slope = %f, y-intercept=%f"%(m,b))
   Ffit = []
   for tv in t: 
       Ffit.append(m*tv+b)
   return m, b, Ffit

