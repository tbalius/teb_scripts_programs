

import sys
import copy
import  matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running
import math, scipy, pylab, numpy


## Writen by Trent Balius in the Shoichet Group
## mod by Mayukh Chakrabarti at FNLRC, 2022
## mod by Trent Balius at FNLRC, Jan 2022


def readmatrix(filehandel):
    matrix = []
    #label1   = []
    #label2   = []
    maxval = -10000.
    minval = 10000.0
    for line in filehandel:
        if ("Frame" in line) or ("AVG" in line): 
            continue
        #line = replace_char(line,'>',' ')
        #line = replace_char(line,';',' ')
        splitline = line.split(',')
        row = []
        for val in splitline:
            #print val, " ",
            fval = float(val)
            if fval > maxval: 
               maxval = fval
            if fval < minval:
               minval = fval
            row.append(fval)
        matrix.append(row)
        #print "\n"
        #label1.append(splitline[0])
        #label2.append(splitline[1])
    print "min, max = ",minval, maxval

    return matrix #,label1,label2

def write_mat(mat,filename):

     fh = open(filename,'w')
     m = len(mat)
     n = len(mat[0])

     fh.write('avg mat\n')
     for i in range(m):
         for j in range(n):
             #fh.write('%f'%mat[i][j])
             fh.write('%f'%mat[i,j])
             if (j < n-1):
                 fh.write(',')
         fh.write('\n')
     fh.close()


def mat_to_mat(mat):

     m = len(mat)
     n = len(mat[0])

     mat2 = numpy.zeros([m,n]) 
     vec1 = numpy.zeros(m) 
     vec2 = numpy.zeros(n) 

     for i in range(m):
         for j in range(n):
             mat2[i,j] = mat[i][j]
             vec1[i] = vec1[i] + mat[i][j] 
             vec2[j] = vec2[j] + mat[i][j] 

     return mat2, vec1, vec2

def mat_larger_mag(mat,lab1,lab2,thrsmax,thrsmin):

     m = len(mat)
     n = len(mat[0])
     lm = len(lab1)
     ln = len(lab2)
     print n,m,ln,lm

     print "thrsmax = %f"%thrsmax
     print "thrsmin = %f"%thrsmin

     for i in range(m):
         for j in range(n):
             #print lab1[i],lab2[j], mat[i][j], thrsmax,thrsmin
             if mat[i][j]>thrsmax or mat[i][j]<thrsmin : 
                #print "%s %s %6.2f\n"%(lab1[i],lab2[j], mat[i][j])
                #print lab1[i],lab2[j], mat[i][j]
                if (i == j ):
                    lpair = "self"
                elif (i == j+1 ):
                    lpair = "near"
                elif (i+1 == j ):
                    lpair = "near"
                else: 
                    lpair = "non_near"                

                print "%s %s %6.2f %s"%(lab1[i],lab2[j], mat[i][j], lpair)

# this function will find the 3 weekest and strongest interactions
def three_max_three_min_residues(Mat):
     m = len(Mat)
     n = len(Mat[0])

     maxv = numpy.zeros(3)
     minv = numpy.zeros(3)
     maxi = numpy.zeros(3)
     mini = numpy.zeros(3)
     maxj = numpy.zeros(3)
     minj = numpy.zeros(3)

     maxv[0] = maxv[1] = maxv[2] = -10000.0
     minv[0] = minv[1] = minv[2] =  10000.0

     for i in range(m):
         for j in range(n):

             val = Mat[i][j]
             # look to see if it val is biger then the max (0) if not check the next (1) and then the next (2)
             if (maxv[0] < val):
                 maxv[0] = val
                 maxi[0] = i
                 maxj[0] = j
             elif (maxv[1] < val):
                 maxv[1] = val
                 maxi[1] = i
                 maxj[1] = j
             elif (maxv[2] < val):
                 maxv[2] = val
                 maxi[2] = i
                 maxj[2] = j

             if (minv[0] > val):
                 minv[0] = val
                 mini[0] = i
                 minj[0] = j
             elif (minv[1] > val):
                 minv[1] = val
                 mini[1] = i
                 minj[1] = j
             elif (minv[2] > val):
                 minv[2] = val
                 mini[2] = i
                 minj[2] = j
     # print out max and min
     for i in range(3):
          print ('%d ... %d -- %d :: val = %8.6f '%(i,maxi[i],maxj[i],maxv[i]))
          print ('check val = %8.6f '%(Mat[int(maxi[i])][int(maxj[i])]))
     for i in range(3):
          print ('%d ... %d -- %d :: val = %8.6f '%(i,mini[i],minj[i],minv[i]))
          print ('check val = %8.6f '%(Mat[int(mini[i])][int(minj[i])]))

     return maxi, maxj, mini, minj

# get a start and stop for a window, do not go out of bounds.
# if point is at the edge then ajust not to go out of bounds.
# dim is the max posible (size of the vector or matrix)
def get_range_for_zoomin(crd,dim,windowsize):

    if crd>dim: 
       print ("error: crd > dim")
       exit()

    mod = windowsize % 2
    print (mod)
    if mod == 0:
       #print ("window is even, add 1")
       #pad = windowsize/2
       windowsize = windowsize + 1
    #else: 
    #   pad = (windowsize-1)/2
    pad = (windowsize-1)/2

    start = crd - pad
    stop = crd + pad

    if start < 0: 
        #print ("start < 0. ajust window")
        stop = stop - start + 1
        start = 0
        #print (stop - start, windowsize)
    if stop > dim: 
        pad = stop - dim
        stop = dim
        start = start - pad
        #print (stop - start, windowsize)

    return start, stop

# zoom in on xres and yres
#def heatmap_subplot(ax,Mat,my_cmap,cmin,cmax,xlabel,ylabel,xres,yres):
def heatmap_subplot(ax,Mat,my_cmap,cmin,cmax,xlabel,ylabel,xres,yres,syb):
     m = len(Mat)
     n = len(Mat[0])
     im = ax.imshow(Mat, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)
     im.set_clim(cmin,cmax)
     ax.set_xlim(-0.5, n-0.5)
     ax.set_ylim(-0.5, m-0.5)
     ax.set_xticks(range(0,n))
     ax.set_xticklabels(xlabel)
     ax.set_yticks(range(0,m))
     val_yticks = ax.get_yticks()
     val_ylim = ax.get_ylim()
     sel_ylabel = []
     for i in val_yticks:
           sel_ylabel.append(ylabel[i])
     ax.set_yticklabels(sel_ylabel)
     for item in (ax.get_yticklabels()):
         item.set_fontsize(3)
     for i in range(n):
         labels = ax.xaxis.get_major_ticks()[i].label
         labels.set_fontsize(3)
         labels.set_rotation('vertical')

     [xstart,xstop] = get_range_for_zoomin(xres,n,11)
     [ystart,ystop] = get_range_for_zoomin(yres,m,11)
     #[ystart,ystop] = get_range_for_zoomin(yres,n,10)

     ax.set_xlim([xstart,xstop])
     ax.set_ylim([ystart,ystop])
     #ax.plot(xres,yres,'k*')
     ax.plot(xres,yres,syb)


#def heatmap(Mat,label,filename,threshold,heatmap_threshold):
def heatmap(Mat0,filename,heatmap_threshold,cmin,cmax,lab1file,lab2file):
     m = len(Mat0)
     n = len(Mat0[0])
     print m,n

     Mat, vec1, vec2 = mat_to_mat(Mat0) 
     #flabel1 = open('../resnames.1.txt','r')
     #flabel2 = open('../resnames.2.txt','r')
     flabel1 = open(lab1file,'r')
     flabel2 = open(lab2file,'r')
     xlabel = []
     for line in flabel2:
          temp = len(line.split())
          if temp == 0:
              continue
          xlabel.append(line.strip())
     ylabel = []
     for line in flabel1:
          temp = len(line.split())
          if temp == 0:
              continue
          ylabel.append(line.strip())
     flabel1.close()
     flabel2.close()

     mat_larger_mag(Mat0,ylabel,xlabel,cmax,cmin)

     fig = pylab.figure(figsize=(8,8))

     ax1 = fig.add_axes([0.04,0.1,0.2,0.6])
     matplotlib.pyplot.plot(vec1,range(0,m),'k-') # draws a datshed line where dendogram is cut.
     #ax1.set_xticks([])
     ax1.set_yticks([])
     ax1.set_ylim(-0.5, m-0.5)
     for tick in ax1.get_xticklabels():
       tick.set_rotation(90)
     #ax1.set_xlim(cmin,cmax)
        
     ax2 = fig.add_axes([0.3,0.75,0.6,0.2])
     print vec2
     matplotlib.pyplot.plot(range(0,n),vec2,'k-') # draws a datshed line where dendogram is cut.
     ax2.set_xticks([])
     #ax2.set_yticks([])
     ax2.set_xlim(-0.5, n-0.5)
     #ax2.set_ylim(cmin,cmax)
        
         # Plot distance matrix.
     axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])

     #cmin = -1.0
     #cmax = 1.0 
     #mp  = (threshold - cmin) / (cmax - cmin)  # midpoint is where the white will appear
     mp  = (heatmap_threshold - cmin) / (cmax - cmin)  # midpoint is where the white will appear
     tol = 0.02
     if mp > 0.9 or mp < 0.1:
         print mp
         print "threshold = " + str(heatmap_threshold) + "is too high or low" 
         exit()

     cdict = {'blue': [(0.0,      1.0, 1.0),
                      ( mp-tol,  1.0, 1.0),
                      ( mp,      1.0, 1.0),
                      ( mp+tol,  0.7, 0.7),
                      (1.0,      0.0, 0.0)],
     
            'green': [(0.0,      0.0, 0.0),
                      ( mp-tol,  0.7, 0.7),
                      ( mp,      1.0, 1.0),
                      ( mp+tol,  0.7, 0.7),
                      (1.0,      0.0, 0.0)],
           
            'red':  [(0.0,      0.0, 0.0),
                      ( mp-tol,  0.7, 0.7),
                      ( mp,      1.0, 1.0),
                      ( mp+tol,  1.0, 1.0),
                      (1.0,      1.0, 1.0)]}

 
     my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,100)
    
     im = axmatrix.imshow(Mat, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)

     #v = range(0,n)
     #axmatrix.plot(v,v,'yo',markersize=2)
         

     im.set_clim(cmin,cmax)
     axmatrix.set_xlim(-0.5, n-0.5)
     axmatrix.set_ylim(-0.5, m-0.5)
     axmatrix.set_xticks(range(0,n))
     axmatrix.set_xticklabels(xlabel)
     axmatrix.set_yticks(range(0,m))
     val_yticks = axmatrix.get_yticks()
     val_ylim = axmatrix.get_ylim()
     #print val_yticks
     #print val_ylim
     sel_ylabel = []
     for i in val_yticks:
           sel_ylabel.append(ylabel[i])
     axmatrix.set_yticklabels(sel_ylabel)

     for item in (axmatrix.get_yticklabels()):
         item.set_fontsize(3)

     for i in range(n):
         labels = axmatrix.xaxis.get_major_ticks()[i].label
         labels.set_fontsize(3)
         labels.set_rotation('vertical')
     # write out vector to file
     #print len(vec1), len(ylabel)
     #print len(vec2), len(xlabel)
     fh = open(filename+'.vec2.txt','w')
     for i in range(len(vec2)):
         fh.write('%s,%f\n'%(xlabel[i],vec2[i]))
     fh.close()

     fh = open(filename+'.vec1.txt','w')
     for i in range(len(vec1)):
         fh.write('%s,%f\n'%(ylabel[i],vec1[i]))
     fh.close()
 
     # Plot colorbar.
     axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
     pylab.colorbar(im, cax=axcolor)
     #fig.show()
     fig.savefig(filename+'_1.png',dpi=600)
     fig.clear()

     # max zoomin plot around three max and three min pairs: 

     [t_max_i, t_max_j, t_min_i, t_min_j] = three_max_three_min_residues(Mat)

     fig = matplotlib.pyplot.figure(1,[15,15])

     ax11 = matplotlib.pyplot.axes([ 0.1, 0.1, 0.2, 0.2])
     yres = t_max_i[0]
     xres = t_max_j[0]
     heatmap_subplot(ax11,Mat,my_cmap,cmin,cmax,xlabel,ylabel,xres,yres,'k*')

     ax12 = matplotlib.pyplot.axes([ 0.4, 0.1, 0.2, 0.2])
     yres = t_max_i[1]
     xres = t_max_j[1]
     heatmap_subplot(ax12,Mat,my_cmap,cmin,cmax,xlabel,ylabel,xres,yres,'k*')

     ax13 = matplotlib.pyplot.axes([ 0.7, 0.1,  0.2, 0.2])
     yres = t_max_i[2]
     xres = t_max_j[2]
     heatmap_subplot(ax13,Mat,my_cmap,cmin,cmax,xlabel,ylabel,xres,yres,'k*')

     ax21 = matplotlib.pyplot.axes([ 0.1, 0.4, 0.2, 0.2])
     yres = t_min_i[0]
     xres = t_min_j[0]
     heatmap_subplot(ax21,Mat,my_cmap,cmin,cmax,xlabel,ylabel,xres,yres,'w*')

     ax22 = matplotlib.pyplot.axes([ 0.4, 0.4, 0.2, 0.2])
     yres = t_min_i[1]
     xres = t_min_j[1]
     heatmap_subplot(ax22,Mat,my_cmap,cmin,cmax,xlabel,ylabel,xres,yres,'w*')

     ax23 = matplotlib.pyplot.axes([ 0.7, 0.4,  0.2, 0.2])
     yres = t_min_i[2]
     xres = t_min_j[2]
     heatmap_subplot(ax23,Mat,my_cmap,cmin,cmax,xlabel,ylabel,xres,yres,'w*')
     

     fig.savefig(filename+'_2.png',dpi=600)

     return


def main():
  if len(sys.argv) != 7: # if no input
     print "syntax:  text file with name and weights (lenth of simulation), heatmap_threshold heatmap_min heatmap_max label1_filename label2_filename"
     print "Error:  you have entered the wrong number of inputs:"
     print len(sys.argv)

  print "You have entered in 3 inputs:"
  file1name  = sys.argv[1] 
  heatmap_threshold  = float(sys.argv[2])
  vmin               = float(sys.argv[3])
  vmax               = float(sys.argv[4])
  lab1               = sys.argv[5] 
  lab2               = sys.argv[6] 

  if (vmin > vmax): 
     print "error:heatmap_min > heatmap_max" 
     exit()
  print "input matrix file = " + file1name
  txtfilehandel = open(file1name,'r')
  count = 0
  w_sum = 0.0
  for line in txtfilehandel: 
      sline = line.split()
      fname = sline[0]
      w     = float(sline[1])
      file1handel = open(fname,'r')
      m_t = readmatrix(file1handel)
      file1handel.close()
      print( "file = %s, weight = %f"%(fname,w))
      #xl,yl = m_t.shape()
      xl = len(m_t)
      yl = len(m_t[0])

      if count == 0: 
         m = numpy.zeros([xl,yl]) 
      for i in range(xl):
          for j in range(yl):
               m[i,j] = m[i,j] + w * m_t[i][j]
      #if count == 0: 
      #   #m = w * m_t
      #else: 
      #   #m = m + w * m_t
      count = count+1
      w_sum = w_sum + w
  #write_matrix(file2handel,m)
  print("sum_of_weights = %f"%w_sum)
  #m = (1/w_sum) * m # normalize weight.  
  for i in range(xl):
      for j in range(yl):
          m[i,j] = (1.0/w_sum) * m[i,j]
  txtfilehandel.close()
  write_mat(m,file1name+'_out.csv')
  heatmap(m,file1name+'_out',heatmap_threshold,vmin,vmax,lab1,lab2)
  return
  #SimlesToFingerPrint("CCC") 
  #SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
  ###SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
 
main()

