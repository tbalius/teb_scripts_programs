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
        id = splitline[2].split('.')[0] # remove to prot id
        score = splitline[21]
        #print score
        idDict_rank[id] = count
        idDict_score[id] = score
        count = count + 1
    return idDict_rank, idDict_score 


# this is the function that we are fiting
def function_fit(parms,xvec):
    l = len(xvec)
    m = parms[0]
    b = parms[1]
    #print l
    yvec = scipy.zeros([l,1])
    for i in range(l):
        yvec[i] = m*xvec[i]+b
        #print yvec[i]
    return yvec

def calc_residuel(parms,xvec,yvec_d):
    # xvec 
    # yvec_d -- data
    # yvec_f -- function
    # res2   -- the sum of the square of the residuales
    yvec_f = function_fit(parms,xvec)
    res2 = 0
    for i in range(len(xvec)):
        res2= res2 + (yvec_f[i]-yvec_d[i])**2
    return res2

def mk_matrix(array1,array2,m):

    if (len(array1) != len(array2)):
        print "Arrays are not the same length..."
        exit()

    matrix = scipy.zeros([m,m])
    amin = min([min(array1), min(array2)])
    amax = max([max(array1), max(array2)])
    
    for ind in range(len(array1)):
        a1 = array1[ind]
        a2 = array2[ind]
        j = int(round((a1 - amin)/(amax - amin)*(m-1)))
        i = int(round((a2 - amin)/(amax - amin)*(m-1)))
        #if (i == 0) or (j == 0): 
        #   print i,j 
        matrix[i,j] = matrix[i,j] + 1

    return matrix

ZERRO = 0.0


if len(sys.argv) != 3:
   print "error:  this program takes 2 input extrct filename.  "    
   exit()

filename1     = sys.argv[1]
filename2     = sys.argv[2]

print "extrct filename1     = " + filename1
print "extrct filename2     = " + filename2

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
1percent = intm * 0.01
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

'''*************************
ppprint "run optimization"
  
ppparms = [0.1, 0.0]
  
###opt.minimize(obj_func,parms, args=(y_meas, x),)
###opt.leasesquarts(obj_func,parms, args=(y_meas, x),)
### y = mx + b --> [x, 1] * [m  b]^T
AAA = numpy.vstack([X.T, numpy.ones(len(X))]).T
###print A
mmm, b = la.lstsq(A, Y)[0]
YYYnew = function_fit([m,b],X)
rrres2_1 = calc_residuel([m,b],X,Y)
ppprint "**** y = %6.3f x + %6.3f , res^2 = %6.3f" % (m,b, res2_1)
  
mmm2 = la.lstsq(X, Y)[0]
YYYnew2 = function_fit([m2,0],X)
rrres2_2 = calc_residuel([m2,0],X,Y)
###print "****",m2,0,"res^2=",res2_2
ppprint "**** y = %6.3f x  , res^2 = %6.3f" % (m2, res2_2)
***************************'''

# Plot distance matrix.
fig = pylab.figure(figsize=(8,8))
#axis = fig.add_axes([0.3,0.1,0.6,0.6])
axis = fig.add_axes([0.1,0.1,0.3,0.3])

threshold1 = 50
threshold2 = 0

lim_min = min(math.floor(Ymin),math.floor(Xmin))
lim_max = max(math.ceil(Ymax), math.ceil(Xmax))
#im = axis.plot(X,Y,'-',[0,100],[0,100],'--')
#im = axis.plot(X,Y,'o',X,Ynew,'b-',X,Ynew2,'g-') #,[0,100],[0,100],'--')
#im = axis.plot(X,Y,'o',[lim_min,lim_max],[lim_min,lim_max],'k-') #,[0,100],[0,100],'--')

X_top = []
Y_top = []
count_Xlte1000 = 0
count_Ylte1000 = 0
count_Xlte1000_Ylte1000 = 0
count_Yonly = 0
count_Xonly = 0
for i in range(len(X)):
    
    if (X[i] < 1000 ):
        count_Xlte1000 = count_Xlte1000 + 1
    if (Y[i] < 1000 ):
        count_Ylte1000 = count_Ylte1000 + 1
    if (X[i] < 1000 and Y[i] >= 1000):
        count_Xonly = count_Xonly + 1
    if (X[i] >= 1000 and Y[i] < 1000):
        count_Yonly = count_Yonly + 1
    if (X[i] < 1000 and Y[i] < 1000):
        count_Xlte1000_Ylte1000 = count_Xlte1000_Ylte1000 + 1

    if (X[i] < 1000 or Y[i] < 1000):
        X_top.append(X[i])
        Y_top.append(Y[i])
    
print '%d,%d,%d,%d,%d\n' % (count_Xlte1000, count_Ylte1000, count_Xlte1000_Ylte1000, count_Xonly, count_Yonly)
print "size X_top  = " + str(len(X_top))



im = axis.plot(X,Y,'o') #,[0,100],[0,100],'--')

#im = axis.plot(X,Y,'.',[threshold1,threshold1],[Ymin,Ymax],'-',[Xmin,Xmax],[threshold2,threshold2],'-')
#axis.set_xlabel('file1='+filename1.split('/')[-4])
#axis.set_ylabel('file2='+filename2.split('/')[-4])
axis.set_xlabel('file1='+filename1)
axis.set_ylabel('file2='+filename2)
#axis.set_title('file='+xyfilename)

#axis.set_ylim(lim_min, lim_max)
#axis.set_xlim(lim_min, lim_max)
#axis.set_ylim(math.floor(Ymin),math.ceil(Ymax))
#axis.set_xlim(math.floor(Xmin),math.ceil(Xmax))
#axis.set_ylim(-10, 110)
#axis.set_xlim(-10, 110)
#axis.set_yticks([])
#axis.set_xticks([])
#axis.set_ylim(lim_min, lim_max)
xmax = max(X)
ymax = max(Y)
axis.set_xticks([ 0, xmax/ 2,  xmax ])
axis.set_yticks([ 0, ymax/2,  ymax ])

## new subplot
axis = fig.add_axes([0.1,0.5,0.3,0.3])

matrix = mk_matrix(X,Y,50)


cdict = {'red': [(0.0,      1.0, 1.0),
                 (0.1,  1.0, 1.0),
                 (0.5,      0.8, 0.8),
                 (0.8,  0.7, 0.7),
                 (1.0,      0.0, 0.0)],

       'green': [(0.0,      1.0, 1.0),
                 (0.1,  0.0, 0.0),
                 (0.5,      0.0, 0.0),
                 (0.8,  0.0, 0.0),
                 (1.0,      0.0, 0.0)],

       'blue':  [(0.0,      1.0, 1.0),
                 (0.1,  0.0, 0.0),
                 (0.5,      1.0, 1.0),
                 (0.8,  1.0, 1.0),
                 (1.0,      1.0, 1.0)]}

my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,150)

im = axis.imshow(matrix, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)
#im = axis.imshow(matrix, aspect='auto', origin='lower',interpolation='nearest')
axis.set_xticks([  ])
axis.set_yticks([  ])

axcolor = fig.add_axes([0.4,0.55,0.05,0.2])
pylab.colorbar(im, cax=axcolor)


## new subplot
axis = fig.add_axes([0.5,0.1,0.3,0.3])
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

## new subplot
axis = fig.add_axes([0.5,0.5,0.3,0.3])

matrix = mk_matrix(Xscore,Yscore,50)


cdict = {'red': [(0.0,      1.0, 1.0),
                 (0.1,  1.0, 1.0),
                 (0.5,      0.8, 0.8),
                 (0.8,  0.7, 0.7),
                 (1.0,      0.0, 0.0)],

       'green': [(0.0,      1.0, 1.0),
                 (0.1,  0.0, 0.0),
                 (0.5,      0.0, 0.0),
                 (0.8,  0.0, 0.0),
                 (1.0,      0.0, 0.0)],

       'blue':  [(0.0,      1.0, 1.0),
                 (0.1,  0.0, 0.0),
                 (0.5,      1.0, 1.0),
                 (0.8,  1.0, 1.0),
                 (1.0,      1.0, 1.0)]}

my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,150)

im = axis.imshow(matrix, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)
#im = axis.imshow(matrix, aspect='auto', origin='lower',interpolation='nearest')
axcolor = fig.add_axes([0.8,0.55,0.05,0.2])
pylab.colorbar(im, cax=axcolor)
axis.set_xticks([  ])
axis.set_yticks([  ])

# histogram figures
fig2 = pylab.figure(figsize=(8,8))
axis = fig2.add_axes([0.1,0.1,0.3,0.2])
n1, bins1, patches1 = pylab.hist(Xscore,20)
midbin1 = scipy.zeros([len(n1),1])
for i in range(0,len(bins1)-1):
    midbin1[i] = (bins1[i] + bins1[i+1])/2
#print len(n1)
#print len(bins1)
axis = fig2.add_axes([0.1,0.4,0.3,0.2])
im = axis.plot(midbin1, n1,'r-') #,[0,100],[0,100],'--')
#panal
axis = fig2.add_axes([0.5,0.1,0.3,0.2])
n2, bins2, patches2 = pylab.hist(Yscore,20)
midbin2 = scipy.zeros([len(n2),1])
for i in range(0,len(bins2)-1):
    midbin2[i] = (bins2[i] + bins2[i+1])/2
#print len(n2)
#print len(bins2)
axis = fig2.add_axes([0.5,0.4,0.3,0.2])
im = axis.plot(midbin2, n2,'b-') #,[0,100],[0,100],'--')

axis = fig2.add_axes([0.5,0.7,0.3,0.2])
im = axis.plot(midbin1, n1,'r-',midbin2, n2,'b-') #,[0,100],[0,100],'--')

fig3 = pylab.figure(figsize=(8,8))

ymax = max(Y_top)
xmax = max(X_top)

axis = fig3.add_axes([0.1,0.1,0.3,0.3])
im = axis.plot(X_top,Y_top,'o') #,[0,100],[0,100],'--')
axis.set_xlim(0, 1000)
axis.set_ylim(0, 1000)
axis.set_xticks([0, 500 ,1000])
axis.set_yticks([0, 500 ,1000])

axis = fig3.add_axes([0.5,0.1,0.3,0.3])
im = axis.plot(X_top,Y_top,'o') #,[0,100],[0,100],'--')
axis.set_xlim( 1000, xmax )
axis.set_ylim(0, 1000)
axis.set_xticks([ 1000, (xmax+1000)/ 2,  xmax ])
axis.set_yticks([0, 500 ,1000])

axis = fig3.add_axes([0.1,0.5,0.3,0.3])
im = axis.plot(X_top,Y_top,'o') #,[0,100],[0,100],'--')
axis.set_xlim( 0, 1000)
axis.set_ylim( 1000, ymax )
axis.set_xticks([0, 500 ,1000])
axis.set_yticks([ 1000, (ymax+1000)/2,  ymax ])

axis = fig3.add_axes([0.5,0.5,0.3,0.3])
#mk_venn( count_Xlte1000_Ylte1000, count_Xonly, count_Yonly)
circle1=matplotlib.pyplot.Circle((0.5,0.3),.3,color='r',alpha=0.5)
circle2=matplotlib.pyplot.Circle((0.5,0.7),.3,color='b',alpha=0.5)
axis.add_artist(circle1)
axis.add_artist(circle2)
#fig.gca().add_artist(circle3)
axis.text(0.4, 0.3,str(count_Xonly))
axis.text(0.4, 0.5,str(count_Xlte1000_Ylte1000))
axis.text(0.4, 0.7,str(count_Yonly))
axis.set_xticks([])
axis.set_yticks([])


#fig.show()
fig.savefig('fig.png',dpi=600)

#fig2.show()
fig2.savefig('fig2.png',dpi=600)

#fig3.show()
fig3.savefig('fig3.png',dpi=600)


