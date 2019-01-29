#! /usr/bin/python2.6
## this uses the version of python on sublime 

## This was adapted from the web:
## http://stackoverflow.com/questions/2982929/plotting-results-of-hierarchical-clustering-ontop-of-a-matrix-of-data-in-python

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
    count  = 1 # rank should start at 1. 
    ## X is the Predicted value (sea_dock)
    ## Y is the accual value (sea)
    #firstline = True
    for line in lines:
        #if firstline == True:
        #   firstline = False
        #   continue
        line = line.strip('\n')
        splitline = line.split()
        id = splitline[2].split('.')[0] # remove to prot id
        score = splitline[21]
        #print score
        idDict_rank[id] = count
        idDict_score[id] = score
        count = count + 1
    return idDict_rank, idDict_score 


if len(sys.argv) != 6:
   print "error:  this program takes 2 input extrct filename.  "    
   exit()

filename1     = sys.argv[1]
filename2     = sys.argv[2]
label1        = sys.argv[3]
label2        = sys.argv[4]
bthres        = float(sys.argv[5])

print "extrct filename1     = " + filename1
print "extrct filename2     = " + filename2
print label1
print label2 

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
#m = max(count2,count1)
count3 = 0
for entry in dict2.keys():
    if (dict1[entry] != -1.0 and dict2[entry] != -1.0):
        count3 = count3+1
m = count3
print count2,count1, m  
X = scipy.zeros([m,1])
Y = scipy.zeros([m,1])
Xscore = scipy.zeros([m,1])
Yscore = scipy.zeros([m,1])
#X = []
#Y = []
#Xscore = []
#Yscore = []

count = 0

fileh = open('in_both.txt','w')

for entry in dict2.keys():

    if dict1[entry] == -1.0 or dict2[entry] == -1.0:
       print entry
       continue
    elif (dict1[entry] < 1000 and dict2[entry] < 1000): 
          fileh.write("%s\n"%entry)
    X[count] = dict1[entry]
    Y[count] = dict2[entry]
    #X.append(dict1[entry])
    #Y.append(dict2[entry])
    Xscore[count] = dictscore1[entry]
    Yscore[count] = dictscore2[entry]
    #Xscore.append(dictscore1[entry])
    #Yscore.append(dictscore2[entry])
    count = count+1

fileh.close()

rp  = stats.pearsonr(X,Y)
rps = stats.pearsonr(Xscore,Yscore)
rs  = stats.spearmanr(X,Y)

Xmax = max(X)
Xmin = min(X)
Ymax = max(Y)
Ymin = min(Y)

print Xmax, Xmin 
print Ymax, Ymin

print "pearson correlation: r = %6.3f, p-value = %6.3e" % (rp)
print "pearson correlation: r = %6.3f, p-value = %6.3e" % (rps)
print "spearma correlation: r = %6.3f, p-value = %6.3e" % (rs)

# Plot rank change
fig = pylab.figure(figsize=(8,8))
#axis = fig.add_axes([0.3,0.1,0.6,0.6])
axis = fig.add_axes([0.15,0.15,0.3,0.3])

im = axis.plot(X,Y,'o') #,[0,100],[0,100],'--')

threshold1 = 50
threshold2 = 0

lim_min = min(math.floor(Ymin),math.floor(Xmin))
lim_max = max(math.ceil(Ymax), math.ceil(Xmax))
#im = axis.plot(X,Y,'-',[0,100],[0,100],'--')
#im = axis.plot(X,Y,'o',X,Ynew,'b-',X,Ynew2,'g-') #,[0,100],[0,100],'--')
#im = axis.plot(X,Y,'o',[lim_min,lim_max],[lim_min,lim_max],'k-') #,[0,100],[0,100],'--')
xlim = axis.get_xlim()
print xlim
#axis.set_xticks(numpy.linspace(lim_min,lim_max,10))
axis.set_xticks(numpy.linspace(xlim[0],xlim[1],10))
axis.set_xlabel("rank1")
axis.set_ylabel("rank2")
for i in range(0,10):
    label = axis.xaxis.get_major_ticks()[i].label
    #label.set_fontsize(3)
    label.set_rotation('vertical')



log10X = []
log10Y = []
log10diff = []
rankdiff = []
count = 0
for i in range(len(X)):
        #print X[i],Y[i]
        if X[i] == 0 or Y[i] == 0: 
           print X[i],Y[i]
           continue
        
        #log10X.append(numpy.log10(X[i]))
        #log10Y.append(numpy.log10(Y[i]))
        log10X.append(math.log10(X[i]))
        log10Y.append(math.log10(Y[i]))
        #log10diff.append(math.fabs(log10X[count]-log10Y[count])) # calculate the log rank difference.  
        log10diff.append((log10X[count]-log10Y[count])) # calculate the log rank difference.  
        rankdiff.append((X[i][0]-Y[i][0])) # calculate the rank difference.  
        count = count + 1 
#print log10diff
    
axis = fig.add_axes([0.15,0.6,0.3,0.3])
im = axis.plot(log10X,log10Y,'o') #,[0,100],[0,100],'--')

#axis.set_xlabel('file1='+filename1)
#axis.set_ylabel('file2='+filename2)
#axis.set_xlabel(label1)
#axis.set_ylabel(label2)
axis.set_title(label1+" "+label2)
axis.set_xlabel("log10(rank1)")
axis.set_ylabel("log10(rank2)")
#xmax = max(X)
#ymax = max(Y)
#axis.set_xticks([ 0, xmax/ 2,  xmax ])
#axis.set_yticks([ 0, ymax/2,  ymax ])


## new subplot
axis = fig.add_axes([0.6,0.6,0.3,0.3])

n1, bins1, patches1 = pylab.hist(log10diff,100)
#print n1, bins1, patches1

midbin1 = scipy.zeros([len(n1),1])
for i in range(0,len(bins1)-1):
    midbin1[i] = (bins1[i] + bins1[i+1])/2
im = axis.plot(midbin1, n1,'b-') 

# rotate axis tick labels
for item in (axis.xaxis.get_major_ticks()):
    #item.label.set_fontsize(5)
    item.label.set_rotation('vertical')

axis.set_xlabel("log10-rank diff")
axis.set_ylabel("population")
# inset
axis = fig.add_axes([0.79,0.79,0.1,0.1])
#axis.plot(midbin1[10:21], n1[10:21])

midbin1_gt_thres = []
n1_gt_thres = []
for b in range(len(midbin1)):
    if midbin1[b] > bthres:
       print b, midbin1[b], n1[b] 
       midbin1_gt_thres.append(midbin1[b])
       n1_gt_thres.append(n1[b])
       

axis.plot(midbin1_gt_thres, n1_gt_thres)
#axis.set_ylim([0,100])
for item in (axis.xaxis.get_major_ticks()):
    #print item.label
    item.label.set_fontsize(5)
    item.label.set_rotation('vertical')

for item in (axis.yaxis.get_major_ticks()):
    #print item.label
    item.label.set_fontsize(5)
    #item.label.set_rotation('vertical')

print len(rankdiff)
print max(rankdiff)


## new subplot

axis = fig.add_axes([0.6,0.15,0.3,0.3])

#n2, bins2, patches2 = pylab.hist(rankdiff,bins=numpy.linspace(-100,100,201))
n2, bins2, patches2 = pylab.hist(rankdiff,100)
#print n2, bins2, patches2

midbin2 = scipy.zeros([len(n2),1])
for i in range(0,len(bins2)-1):
    midbin2[i] = (bins2[i] + bins2[i+1])/2
im = axis.plot(midbin2, n2,'b-')

for item in (axis.xaxis.get_major_ticks()):
    #print item.label
    #item.label.set_fontsize(5)
    item.label.set_rotation('vertical')

axis.set_xlabel("rank diff")
axis.set_ylabel("population")

fig.savefig('fig.png',dpi=600)
matplotlib.pyplot.close("all")


########################################
########################################

fig2 = pylab.figure(figsize=(8,8))


## new subplot
axis = fig.add_axes([0.6,0.15,0.3,0.3])
Xmax = max(Xscore)
Xmin = min(Xscore)
Ymax = max(Yscore)
Ymin = min(Yscore)

#print Xmax, Xmin 
#print Ymax, Ymin

lim_min = min(math.floor(Ymin),math.floor(Xmin))
lim_max = max(math.ceil(Ymax), math.ceil(Xmax))

im = axis.plot(Xscore,Yscore,'o',[lim_min,lim_max],[lim_min,lim_max],'k-') #,[0,100],[0,100],'--')

axis.set_xlim(lim_min, lim_max)
axis.set_xticks([ lim_min, (lim_min+lim_max)/ 2, lim_max ])
axis.set_yticks([ lim_min, (lim_min+lim_max)/ 2, lim_max ])
axis.set_xlabel("energy1 (kcal/mol)")
axis.set_ylabel("energy2 (kcal/mol)")

fig2.savefig('fig2.png',dpi=600)
matplotlib.pyplot.close("all")
#fig2.close()

## histogram figures
#fig2 = pylab.figure(figsize=(8,8))
#axis = fig2.add_axes([0.1,0.1,0.3,0.2])
#n1, bins1, patches1 = pylab.hist(Xscore,20)
#midbin1 = scipy.zeros([len(n1),1])
#for i in range(0,len(bins1)-1):
#    midbin1[i] = (bins1[i] + bins1[i+1])/2
##print len(n1)
##print len(bins1)
#axis = fig2.add_axes([0.1,0.4,0.3,0.2])
#im = axis.plot(midbin1, n1,'r-') #,[0,100],[0,100],'--')
##panal
#axis = fig2.add_axes([0.5,0.1,0.3,0.2])
#n2, bins2, patches2 = pylab.hist(Yscore,20)
#midbin2 = scipy.zeros([len(n2),1])
#for i in range(0,len(bins2)-1):
#    midbin2[i] = (bins2[i] + bins2[i+1])/2
##print len(n2)
##print len(bins2)
#axis = fig2.add_axes([0.5,0.4,0.3,0.2])
#im = axis.plot(midbin2, n2,'b-') #,[0,100],[0,100],'--')
#
#axis = fig2.add_axes([0.5,0.7,0.3,0.2])
#im = axis.plot(midbin1, n1,'r-',midbin2, n2,'b-') #,[0,100],[0,100],'--')

#fig3 = pylab.figure(figsize=(8,8))
#
#ymax = max(Y_top)
#xmax = max(X_top)
#
#axis = fig3.add_axes([0.1,0.1,0.3,0.3])
#im = axis.plot(X_top,Y_top,'o') #,[0,100],[0,100],'--')
#axis.set_xlim(0, 1000)
#axis.set_ylim(0, 1000)
#axis.set_xticks([0, 500 ,1000])
#axis.set_yticks([0, 500 ,1000])
#
#axis = fig3.add_axes([0.5,0.1,0.3,0.3])
#im = axis.plot(X_top,Y_top,'o') #,[0,100],[0,100],'--')
#axis.set_xlim( 1000, xmax )
#axis.set_ylim(0, 1000)
#axis.set_xticks([ 1000, (xmax+1000)/ 2,  xmax ])
#axis.set_yticks([0, 500 ,1000])
#
#axis = fig3.add_axes([0.1,0.5,0.3,0.3])
#im = axis.plot(X_top,Y_top,'o') #,[0,100],[0,100],'--')
#axis.set_xlim( 0, 1000)
#axis.set_ylim( 1000, ymax )
#axis.set_xticks([0, 500 ,1000])
#axis.set_yticks([ 1000, (ymax+1000)/2,  ymax ])
#
#fig.show()
#fig.savefig('fig.png',dpi=600)

#fig2.show()
#fig2.savefig('fig2.png',dpi=600)

##fig3.show()
#fig3.savefig('fig3.png',dpi=600)


