#! /usr/bin/python2.6

# This script finds molcules (by comparing 2 extract all files) that have a log rank difference of grater than a values
#
# Written by Trent E. Balius

import sys
import copy
import math
import matplotlib
import scipy
import numpy
import pylab
#import scipy.cluster.hierarchy as sch
#from scipy.optimize import opt
import scipy.optimize as opt
import scipy.linalg   as la
import scipy.stats    as stats


def read_extract_file(filename):

    file = open(filename)
    lines = file.readlines()
    file.close()

    #idlist = []
    idDict_rank = {}
    idDict_score = {}
    count  = 0
    ## X is the Predicted value (sea_dock)
    ## Y is the accual value (sea)
    #firstline = True
    for line in lines:
        #if firstline == True:
        #   firstline = False
        #   continue
        line = line.strip('\n')
        splitline = line.split()
        id = splitline[2].split('.')[0]
        score = splitline[21]
        print score
        idDict_rank[id] = count
        idDict_score[id] = score
        count = count + 1
    return idDict_rank, idDict_score 

if len(sys.argv) != 4:
   print "error:  This program takes 2 input extrct filename. And a log rank difference value.  "    
   exit()

filename1     = sys.argv[1]
filename2     = sys.argv[2]
lval          = float(sys.argv[3])

print "extrct filename1     = " + filename1
print "extrct filename2     = " + filename2
print " log value           = " + str(lval)

dict1, dictscore1 = read_extract_file(filename1)
dict2, dictscore2 = read_extract_file(filename2)

#count = len(dict1.keys())
count1 = 0

for entry in dict1.keys():
    if not entry in dict2:
       print entry + " not in dictionay 2"
       #dict2[entry] = count
       #count = count+1
       dictscore2[entry] = 5000.0
       dict2[entry] = -1.0
       #exit()
    else:
       count1 = count1+1

#count = len(dict2.keys())
count2 = 0
for entry in dict2.keys():
    if not entry in dict1:
       print entry + " not in dictionay 1"
       #dict1[entry] = count
       #count = count+1
       dictscore1[entry] = 5000.0
       dict1[entry] = -1.0
    else:
       count2 = count2+1
       #exit()

#m = len(dict2.keys())
m = max(count2,count1)
print count2,count1, m  
X = scipy.zeros([m,1])
Y = scipy.zeros([m,1])
Xscore = scipy.zeros([m,1])
Yscore = scipy.zeros([m,1])

count = 0

for entry in dict2.keys():
    if dict1[entry] == -1.0 or dict2[entry] == -1.0:
       print entry
       continue
    X[count] = dict1[entry]
    Y[count] = dict2[entry]
    Xscore[count] = dictscore1[entry]
    Yscore[count] = dictscore2[entry]
    count = count+1

# print all zinc id with large (greater than 2) log rank changes.  

file1 = open("rankchangebetter2.txt",'w')
file2 = open("rankchangebetter1.txt",'w')

file3 = open("rankonly2.txt",'w')
file4 = open("rankonly1.txt",'w')

for entry in dict1.keys():
    if dict1[entry] == -1.0:
       #print entry
       file3.write('%s,%f,%d,%d\n'%(entry,0.0,dict1[entry],dict2[entry]))
       continue
    if dict2[entry] == -1.0:
       file4.write('%s,%f,%d,%d\n'%(entry,0.0,dict1[entry],dict2[entry]))
       continue
    #print entry
    #print entry, dict1[entry], dict2[entry]
    log1 = math.log10(float(dict1[entry]+1.0))
    log2 = math.log10(float(dict2[entry]+1.0))
    difflog = (log1 - log2)
    if abs(difflog) > lval: 
       print entry, difflog, dict1[entry], dict2[entry]
    if difflog > lval: 
       file1.write('%s,%f,%d,%d\n'%(entry, difflog, dict1[entry], dict2[entry]))
    elif difflog < (-1.0 * lval): 
       file2.write('%s,%f,%d,%d\n'%(entry, difflog, dict1[entry], dict2[entry]))

file1.close()
file2.close()
file3.close()
file4.close()


