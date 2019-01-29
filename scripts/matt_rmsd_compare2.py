
## uses local version of python on sublime

import sys
import copy

import math, matplotlib, scipy, pylab,numpy
import scipy.cluster.hierarchy as sch


## Writen by Trent Balius in the Shoichet Group
## Comare matt Merski matrics to trent's.

def replace_char(string1,char_old,char_new):
    string_new = ''
    for char in string1:
        #print char
        if char != char_old:
           string_new = string_new+char
        else:
           string_new = string_new+char_new
    return string_new    
    

def readrmsd(filehandel):
    rmsdlist = []
    label1   = []
    label2   = []
    for line in filehandel:
        #splitline = line.split()
        #print line
        line = replace_char(line,'>',' ')
        line = replace_char(line,';',' ')
        splitline = line.split()
        rmsdlist.append(float(splitline[2]))
        label1.append(splitline[0])
        label2.append(splitline[1])
        #print splitline[1] 

    #N = len(rmsdlist) 
    #M = round(math.sqrt(N))
    #M = int(math.sqrt(N))

    ## label = label2[0:M]
    #label = []
    #for i in range(M):
    #   label.append(label2[i])

    return rmsdlist,label1,label2


# this function reads in a list of lenght N; N = M(M-1)/2
# And returns a MXM matrix
def vec_to_mat_upper_tirangle(label1,label2,rmsdlist):

    N = len(rmsdlist)

    #       __________
    # M =  / 2*N + 1/4  - 1/2
    #     V        

    M = int(math.sqrt(2*N+1/4)-1/2)
    print N, M
    # inistizes Matrix
    m = []
    for i in range(M+1):
        row = []
        for j in range(M+1):
            row.append(float(0))
        m.append(row)

    #dic of lables
    dic_lab = {}
    count = 0
    for lab in label1:
        if not lab in dic_lab.keys():
           dic_lab[lab]= count
           count = count +1
    # last pdb is not in label1
    # first pdb is not in label2
    for lab in label2:
        if not lab in dic_lab.keys():
           dic_lab[lab]= count
           count = count +1 

    count = 0
    for k in range(N):
        i = dic_lab[label1[k]]
        j = dic_lab[label2[k]]
        #print i, j, k, label1[k], label2[k], rmsdlist[k]
        m[i][j] = float(rmsdlist[k])
        m[j][i] = float(rmsdlist[k])

    label = []
    label.append(label1[0])
    for k in range(M):
    #for k in range(M+1):
        label.append(label2[k])

    return m, label

# this function reads in a list of lenght N; N = MXM
# And returns a MXM matrix 
def vec_to_mat(rmsdlist,label2):

    N = len(rmsdlist)
    #M = math.sqrt(N)
    M = int(math.sqrt(N))
    print N, M 
    m = []

    count = 0
    for i in range(M):
        row = []
        for j in range(M):
            row.append(rmsdlist[count])
            count = count + 1
        m.append(row)

    label = []
    for k in range(M):
        label.append(label2[k])

    return m, label

def write_matrix(filehandel,Matrix):
    for i in range(len(Matrix)):
        for j in range(len(Matrix[i])):
            if (j == 0):
                filehandel.write('%f' % (Matrix[i][j]))
            filehandel.write(',%f' % (Matrix[i][j]))
        filehandel.write('\n')

def mat_to_mat(Mat):
    m = len(Mat)
    n = len(Mat[0])

    if (m != n):
        print "inconsitancy in numbers of rows and columns in the matrix."

    print m,n

    X = scipy.zeros([m,n])

    ## converts from a 2D array to Scipy Matrix 
    for i in range(0,m):
        for j in range(0,n):
               ## 1 - tc is more like a distance than tc.
               #X[i,j] = -Mat[i][j] + 1.0 # for tanimoto
               X[i,j] = Mat[i][j]

    return X

def array_to_vector(array):
    print "In array_to_vector"
    m = len(array)
    print m
    vec = scipy.zeros([m,1])

    ## converts from an array to Scipy vec
    for i in range(0,m):
        vec[i] = array[i]
    print min(vec), max(vec)
    return vec

def mat_to_vector(Mat):
    m = len(Mat)
    n = len(Mat[0])
   
    if (m != n):
        print "inconsitancy in numbers of rows and columns in the matrix."
        sys.exit()
   
    print m,n
   
    X = scipy.zeros([m,n])
    Xvec = scipy.zeros(n*(n-1)/2)
   
    count2    = 0

    ## converts from a 2D array to Scipy Matrix 
    for i in range(0,n):
        for j in range(0,n):
               ## 1 - tc is more like a distance than tc.
               #X[i,j] = -Mat[i][j] + 1.0
               X[i,j] = Mat[i][j] 

    for i in range(0,n):
        for j in range(i+1,n):
               ## 1 - tc is more like a distance than tc.
               #Xvec[count2] = -Mat[i][j] + 1.0
               Xvec[count2] = Mat[i][j] 
               count2 = count2+1

    return X,Xvec

# this function will find the correspondance between to lists.
def find_correspondance(label1,label2):
    dic_labs = {}
    count = 0
    for lab in label2:
        if lab in dic_labs.keys(): 
           continue
        dic_labs[lab] = count 
        count = count +1

    lab1tolab2 = []
    for lab in label1:
        lab1tolab2.append(dic_labs[lab])

    ## l1 -> l2
       
    return lab1tolab2

def main():
  if len(sys.argv) != 4: # if no input
     print "syntax:  matt_rmsd_compare rmsd1.txt rmsd2.txt output"
     print "Error:  you have entered the wrong number of inputs:"
     print len(sys.argv)

  print "You are entered in 2 inputs:"
  file1name  = sys.argv[1] 
  file2name  = sys.argv[2] 
  file3name  = sys.argv[3] 
  print "input rmsdfile = " + file1name
  print "output matrix file = " + file3name
  file1handel = open(file1name,'r')
  file2handel = open(file2name,'r')
  #file3handel = open(file3name,'w')
  rmsdlist,label1,label2 = readrmsd(file1handel)
  rmsdlist2,label21,label22 = readrmsd(file2handel)
  m1, label1 = vec_to_mat_upper_tirangle(label1,label2,rmsdlist)
  m2, label2 = vec_to_mat_upper_tirangle(label21,label22,rmsdlist2)
 #m2, label2 = vec_to_mat(rmsdlist2,label22)
  lab1tolab2 = find_correspondance(label1,label2)
  #for i in range(len(label1)):
  #    print label1[i], label2[lab1tolab2[i]]
  mat1 = mat_to_mat(m1)
  mat2 = mat_to_mat(m2)

  ## sort the matrix2 to be in the same order as matrix1 
  mat2 = mat2[:,lab1tolab2]
  mat2 = mat2[lab1tolab2,:]

  temp, v1 = mat_to_vector(mat1)
  temp, v2 = mat_to_vector(mat2)

  fig = pylab.figure(figsize=(8,8))
  ax = fig.add_axes([0.2,0.2,0.6,0.6])
  matplotlib.pyplot.plot(v1,v2,'k.')
  matplotlib.pyplot.plot([min(v1),max(v1)],[min(v2),max(v2)],'b-')
  fig.show()
  fig.savefig(file3name+'.png',dpi=600)
 

  #write_matrix(file2handel,m)
  file1handel.close()
  file2handel.close()
  #file3handel.close()
  return
  #SimlesToFingerPrint("CCC") 
  #SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
  ###SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
 
main()

