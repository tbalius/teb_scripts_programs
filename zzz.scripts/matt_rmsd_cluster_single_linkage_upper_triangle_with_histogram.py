
## uses local version of python on sublime

import sys
import copy

import math 

import matplotlib 
matplotlib.use('Agg')  # allows you to not have an x-server running

import scipy, pylab,numpy
import scipy.cluster.hierarchy as sch


## Writen by Trent Balius in the Shoichet Group
## this script reads in a text file with 3 columns 
## label1 label2 RMSD
## The script uses scipy.cluster to perform hierarchal clustering 
## on the RMSD matrix
## this was written to help Matt Merski perform clustering analysis.
## updated to python3 TEB, 2024/05/29

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
        line = replace_char(line,',',' ')
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
    print (N, M)
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
    #label.append(label1[0])
    #for k in range(M):
    ##for k in range(M+1):
    #    label.append(label2[k])
    for k in range(M+1):
        label.append('')
    for key in dic_lab.keys():
        i = dic_lab[key]
        label[i] = key


    return m, label

# this function reads in a list of lenght N; N = MXM
# And returns a MXM matrix 
def vec_to_mat(rmsdlist):

    N = len(rmsdlist)
    #M = math.sqrt(N)
    M = int(math.sqrt(N))
    print (N, M)
    m = []

    count = 0
    for i in range(M):
        row = []
        for j in range(M):
            row.append(rmsdlist[count])
            count = count + 1
        m.append(row)

    return m

def write_matrix(filehandel,Matrix):
    for i in range(len(Matrix)):
        for j in range(len(Matrix[i])):
            if (j == 0):
                filehandel.write('%f' % (Matrix[i][j]))
            else: 
                filehandel.write(',%f' % (Matrix[i][j]))
        filehandel.write('\n')

def mat_to_mat(Mat):
    m = len(Mat)
    n = len(Mat[0])

    if (m != n):
        print ("inconsitancy in numbers of rows and columns in the matrix.")

    print (m,n)

    #X = scipy.zeros([m,n])
    X = numpy.zeros([m,n])

    ## converts from a 2D array to Scipy Matrix 
    for i in range(0,m):
        for j in range(0,n):
               ## 1 - tc is more like a distance than tc.
               #X[i,j] = -Mat[i][j] + 1.0 # for tanimoto
               X[i,j] = Mat[i][j]

    return X

def array_to_vector(array):
    print ("In array_to_vector")
    m = len(array)
    print (m)
    #vec = scipy.zeros([m,1])
    vec = numpy.zeros([m,1])

    ## converts from an array to Scipy vec
    for i in range(0,m):
        vec[i] = array[i]
    print (min(vec), max(vec))
    return vec

def mat_to_vector(Mat):
    m = len(Mat)
    n = len(Mat[0])
   
    if (m != n):
        print ("inconsitancy in numbers of rows and columns in the matrix.")
        sys.exit()
   
    print (m,n)
   
    #X = scipy.zeros([m,n])
    #Xvec = scipy.zeros(n*(n-1)/2)
    X = numpy.zeros([m,n])
    Xvec = numpy.zeros(int(n*(n-1)/2))
   
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

def heatmap(Mat,label,bool_sort,filename,threshold,heatmap_threshold):
     m = len(Mat)
     n = len(Mat[0])
     print (m,n)

     #xlabel = [] 
     #for i in range(0,m):
     #   xlabel.append('lig_'+str(i+1))
     #ylabel = []
     #for i in range(0,n):
     #   ylabel.append('lig_'+str(i+1))
     xlabel = label
     ylabel = label

     fig = pylab.figure(figsize=(8,8))

     if (bool_sort):
         Mat, Matvec = mat_to_vector(Mat)
         Mat_copy = copy.copy(Mat)
         Y = sch.linkage(Matvec, method='single')
        #Y = sch.linkage(Matvec, method='average')
        #Y = sch.linkage(Matvec, method='complete')
        #Y = sch.linkage(Matvec, method='centroid')
        #Y = sch.linkage(Matvec, method='median')
         #help(sch.linkage)
         #threshold = 1.0 # good for single
         #threshold = 0.5 # good for single
         #threshold = 1.5 # good for average
         #threshold = 2.35 # good for complete
         #threshold = 3.0 # good for complete
         #threshold = 2.0 # good for complete
         clusters = sch.fcluster(Y, threshold, 'distance')
         print (clusters)
         for i in range(len(label)):
             print (label[i] + " " + str(clusters[i]))

         ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
         sch.set_link_color_palette(['k','k','k','k','c','m','g'])
         Z1 = sch.dendrogram(Y, orientation='right',color_threshold=threshold)
         matplotlib.pyplot.plot([threshold,threshold],[0,10*len(label)],'k--') # draws a datshed line where dendogram is cut.
         #help(sch.dendrogram)
         ax1.set_xticks([])
         ax1.set_yticks([])
        
         # Compute and plot second dendrogram.
         ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
         Z2 = sch.dendrogram(Y,color_threshold=threshold)
         matplotlib.pyplot.plot([0,10*len(label)],[threshold,threshold],'k--') # draws a datshed line where dendogram is cut.
         ax2.set_xticks([])
         ax2.set_yticks([])
         #ax2.set_xlim(-1, n)
        
         # Plot distance matrix.
         axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
         idx1 = Z1['leaves']
         idx2 = Z2['leaves']
         print ("#### index ")
         for i in idx1:
             print (i)
         print ("####")
         Mat = Mat[idx1,:]
         Mat = Mat[:,idx2]
         #xlabel[:] = xlabel[idx2]
         xlabel_new = []
         clusters_new = []
         for i in range(len(idx2)):
             xlabel_new.append(xlabel[idx2[i]])
             clusters_new.append(clusters[idx2[i]])
         del xlabel[:]
         xlabel = xlabel_new

         cluster_dic = {}

         print ("systems sorted:")
         for i in range(len(xlabel)):
             print (xlabel[i] + " " + str(clusters_new[i]) )
             if clusters_new[i] in cluster_dic.keys():
                cluster_dic[clusters_new[i]] = cluster_dic[clusters_new[i]] +" "+ xlabel[i]
             else: 
                cluster_dic[clusters_new[i]] = xlabel[i]
         for key in cluster_dic.keys():
             print ("cluster " +str(key) + ":" + cluster_dic[key])

     else:
         Mat = mat_to_mat(Mat)
         axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])

     #cdict = {'red': ((0.0, 0.0, 0.0),
     #                  (0.0, 0.0, 0.0),
     #                  (1.0, 1.0, 1.0)),
     #          'green': ((0.0, 0.0, 0.0),
     #                    (0.0, 0.0, 0.0),
     #                    (1.0, 1.0, 1.0)),
     #          'blue': ((0.0, 0.0, 0.0),
     #                   (0.0, 0.0, 0.0),
     #                   (1.0, 1.0, 1.0))}
     
     #cdict = {'red':   [(0.0,  0.0, 0.0),
     #              (0.5,  1.0, 1.0),
     #              (1.0,  1.0, 1.0)],
     #
     #    'green': [(0.0,  0.0, 0.0),
     #              (0.25, 0.0, 0.0),
     #              (0.75, 1.0, 1.0),
     #              (1.0,  1.0, 1.0)],
     #
     #    'blue':  [(0.0,  0.0, 0.0),
     #              (0.5,  0.0, 0.0),
     #              (1.0,  1.0, 1.0)]}  


     ## red - white - blue
     # colorbar is from 0 to 5
     # I want the white to appare at the threshold value 
     # midpoint  : threshodl
     # 0.0       =  0.0
     # 0.2       = ~1.0
     # 0.5       =  2.5
     # 0.8       = ~4.0
     # 1.0       =  5.0
     cmin = 0.5
     cmax = 3.0 
     #mp  = (threshold - cmin) / (cmax - cmin)  # midpoint is where the white will appear
     mp  = (heatmap_threshold - cmin) / (cmax - cmin)  # midpoint is where the white will appear
     tol = 0.02
     if mp > 0.9 or mp < 0.1:
         print ("threshold = " + str(threshold) + "is too high or low" )
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

     ## blue - purple - red
     #cdict = {'red': [(0.0,  0.0, 0.0),
     #                 (0.5,  0.5, 0.5),
     #                 (1.0,  1.0, 1.0)],
     #
     #       'green': [(0.0,  0.0, 0.0),
     #                 (1.0,  0.0, 0.0)],
     #
     #       'blue':  [(0.0,  1.0, 1.0),
     #                 (0.5,  0.5, 0.5),
     #                 (1.0,  0.0, 0.0)]}

 
 
     my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,100)
    
     im = axmatrix.imshow(Mat, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)

     if (bool_sort):
         v = range(0,n)
         axmatrix.plot(v,v,'yo',markersize=2)
         

     im.set_clim(cmin,cmax)
     axmatrix.set_xlim(-0.5, n-0.5)
     axmatrix.set_ylim(-0.5, n-0.5)
     axmatrix.set_xticks(range(0,m))
     axmatrix.set_xticklabels(xlabel)

     if (not bool_sort):
         axmatrix.set_yticks(range(0,n))
         axmatrix.set_yticklabels(ylabel)
         for i in range(0,n):
             labels = axmatrix.yaxis.get_major_ticks()[i].label1
             labels.set_fontsize(3)
     else:
         axmatrix.set_yticks([])
     
     for i in range(0,m):
         labels = axmatrix.xaxis.get_major_ticks()[i].label1
         labels.set_fontsize(3)
         labels.set_rotation('vertical')
    
     # Plot colorbar.
     axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
     pylab.colorbar(im, cax=axcolor)
     fig.show()
     fig.savefig(filename,dpi=600)

##   # make histograms
##   if not (bool_sort):
##       return
##
##   # this see how many clusters and how big they are
##   min_clust = min(clusters)
##   max_clust = max(clusters)
##   for i in range(min_clust,max_clust+1):
##       count = 0
##       for j in range(len(clusters)):
##           if i == clusters[j]:
##              count = count+1
##       print "cluster_"+str(i)+" has " + str(count) + " elements."

     ## if you do not want to gerenate the histograms 
     ## comment back in the return
     return

     cluster1_1 = []
     cluster2_2 = []
     cluster3_3 = []
     cluster1_2 = []
     cluster1_3 = []
     cluster2_3 = []

     ## 
     ## Looking at the heatmap we I denified the non 
     ## singlton clusters.

     clustnum1 = 8 # closed
     clustnum2 = 7 # intermediate
     clustnum3 = 13 # open

     clustname = ["closed", "intermediate", "open"]


     print ("Number of sytems = "+str(len(xlabel)))

     for i in range(len(xlabel)):
         for j in range(i,len(xlabel)): 
             ## Note that this is for a threshold of 2.0
             ## Looking at the heatmap we I denified the non 
             ## singlton clusters.
             #if clusters[i] == 1 and clusters[j] == 1:
             if clusters[i] == clustnum1 and clusters[j] == clustnum1 \
             or clusters[j] == clustnum1 and clusters[i] == clustnum1:
                cluster1_1.append(Mat_copy[i,j])
             #elif clusters[i] == 2 and clusters[j] == 2:
             elif clusters[i] == clustnum2 and clusters[j] == clustnum2 \
               or clusters[j] == clustnum2 and clusters[i] == clustnum2:
                cluster2_2.append(Mat_copy[i,j])
             #elif clusters[i] == 3 and clusters[j] == 3:
             elif clusters[i] == clustnum3 and clusters[j] == clustnum3 \
               or clusters[j] == clustnum3 and clusters[i] == clustnum3:
                cluster3_3.append(Mat_copy[i,j])
             #elif clusters[i] == 1 and clusters[j] == 2:
             elif clusters[i] == clustnum1 and clusters[j] == clustnum2 \
               or clusters[j] == clustnum1 and clusters[i] == clustnum2:
                cluster1_2.append(Mat_copy[i,j])
             #elif clusters[i] == 1 and clusters[j] == 3:
             elif clusters[i] == clustnum1 and clusters[j] == clustnum3 \
               or clusters[j] == clustnum1 and clusters[i] == clustnum3:
                cluster1_3.append(Mat_copy[i,j])
             #elif clusters[i] == 2 and clusters[j] == 3:
             elif clusters[i] == clustnum2 and clusters[j] == clustnum3 \
               or clusters[j] == clustnum2 and clusters[i] == clustnum3:
                print (clusters[i], clusters[j], Mat_copy[i,j])
                cluster2_3.append(Mat_copy[i,j])
             #else:
             #   print clusters[i], clusters[j]
             #print clusters[i], clusters[j]
     cluster1_1_sci = array_to_vector(cluster1_1)
     cluster1_2_sci = array_to_vector(cluster1_2)
     cluster1_3_sci = array_to_vector(cluster1_3)
     cluster2_2_sci = array_to_vector(cluster2_2)
     cluster2_3_sci = array_to_vector(cluster2_3)
     cluster3_3_sci = array_to_vector(cluster3_3)
     fig = pylab.figure(figsize=(8,8))
     inbins = numpy.linspace(0,4,50)
     pbins = numpy.linspace(0.05,3.95,49) 
     #inbins = [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]
     #pbins = [0.25,0.75,1.25,1.75,2.25,2.75,3.25,3.75,4.25,4.75]
     #n, bins, patches = matplotlib.pylab.hist(cluster2_2_sci, inbins, normed=1, histtype='bar')
     axis = fig.add_axes([0.1,0.1,0.3,0.1])
     n1_1, bins, patches = axis.hist(cluster1_1_sci, inbins, normed=1, histtype='bar')
     #p1 = pylab.plot(pbins,n1_1,'k-') #.
     axis.set_xlim(0.0,  4.0)
     #axis.set_ylim(0.0, 10.0)
     axis.set_ylim(0.0, 5.0)

     axis = fig.add_axes([0.1,0.3,0.3,0.1])
     n2_2, bins, patches = axis.hist(cluster2_2_sci, inbins, normed=1, histtype='bar')
     axis.set_xlim(0.0,  4.0)
     axis.set_ylim(0.0, 5.0)

     axis = fig.add_axes([0.1,0.5,0.3,0.1])
     n3_3, bins, patches = axis.hist(cluster3_3_sci, inbins, normed=1, histtype='bar')
     axis.set_xlim(0.0,  4.0)
     axis.set_ylim(0.0, 5.0)

     axis = fig.add_axes([0.5,0.1,0.3,0.1])
     n1_2, bins, patches = axis.hist(cluster1_2_sci, inbins, normed=1, histtype='bar')
     axis.set_xlim(0.0,  4.0)
     axis.set_ylim(0.0, 5.0)

     axis = fig.add_axes([0.5,0.3,0.3,0.1])
     n1_3, bins, patches = axis.hist(cluster1_3_sci, inbins, normed=1, histtype='bar')
     axis.set_xlim(0.0,  4.0)
     axis.set_ylim(0.0, 5.0)

     axis = fig.add_axes([0.5,0.5,0.3,0.1])
     n2_3, bins, patches = axis.hist(cluster2_3_sci, inbins, normed=1, histtype='bar')
     axis.set_xlim(0.0,  4.0)
     axis.set_ylim(0.0, 5.0)
     
     fig.show()
     #fig.savefig("single_hist1.png",dpi=600)
     fig.savefig("single_hist1_"+filename,dpi=600)
     fig = pylab.figure(figsize=(8,8))
     #print n, bins, patches
     axis = fig.add_axes([0.3,0.1,0.6,0.6])
     #axis = fig.add_axes([0.1,0.4,0.1,0.6])
     #matplotlib.pyplot.plot(pbins,n1_1,'y-o',pbins,n2_2,'b-o',pbins,n3_3,'r-o',pbins,n1_2,'g-o',pbins,n1_3,'m-o',pbins,n2_3,'k-o') #.
     #matplotlib.pyplot.plot(pbins,n1_1,'y-',label='1_1') #.
     p1 = pylab.plot(pbins,n1_1,'m-') #.
     p2 = pylab.plot(pbins,n2_2,'c-') #.
     p3 = pylab.plot(pbins,n3_3,'g-') #.
     p4 = pylab.plot(pbins,n1_2,'r-') #.
     p5 = pylab.plot(pbins,n1_3,'b-') #.
     p6 = pylab.plot(pbins,n2_3,'y-') #.
     #pylab.legend([p1[0],p2[0],p3[0],p4[0],p5[0],p6[0]],['1_1','2_2','3_3','1_2','1_3','2_3'])
     pylab.legend([p1[0],p2[0],p3[0],p4[0],p5[0],p6[0]],[ clustname[0]+'_'+clustname[0], clustname[1]+'_'+clustname[1], clustname[2]+'_'+clustname[2], \
                                                          clustname[0]+'_'+clustname[1],clustname[0]+'_'+clustname[2],clustname[1]+'_'+clustname[2]], \
                                                          bbox_to_anchor=(0., 1.02, 1., .102), loc=3)
                                                         # loc=[0.3,0.8])

     pylab.xlabel("RMSD (angstroms)")
     pylab.ylabel("Normlized Count")
     fig.show()
     #fig.savefig("single_hist2.png",dpi=600)
     fig.savefig("single_hist2_"+filename,dpi=600)
     return



def main():
  if len(sys.argv) != 5: # if no input
     print ("syntax:  matt_rmsd_cluster.py rmsd.txt matrix threshold (cut dendogram) threshold (color_heatmap)")
     print ("Error:  you have entered the wrong number of inputs:")
     print (len(sys.argv))

  print ("You are entered in 3 inputs:")
  file1name  = sys.argv[1] 
  file2name  = sys.argv[2] 
  threshold  = float(sys.argv[3])
  heatmap_threshold  = float(sys.argv[4])
  file2name = file2name+"_t"+str(threshold) ## add the treshold to filename
  print ("input rmsdfile = " + file1name)
  print ("output matrix file = " + file2name)
  file1handel = open(file1name,'r')
  file2handel = open(file2name,'w')
  rmsdlist,label1,label2 = readrmsd(file1handel)
  m, label = vec_to_mat_upper_tirangle(label1,label2,rmsdlist)
  write_matrix(file2handel,m)
  file1handel.close()
  file2handel.close()
  heatmap(m,label,True,file2name+'.png',threshold,heatmap_threshold)
  return
  #SimlesToFingerPrint("CCC") 
  #SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
  ###SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
 
main()

