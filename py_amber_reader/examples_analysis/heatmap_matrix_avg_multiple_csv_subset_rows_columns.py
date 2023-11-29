

import sys
import copy
import  matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running
#import math, scipy, pylab, numpy
import math, scipy, numpy
import matplotlib.pyplot as pylab


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
        if ("Frame" in line) or ("AVG" in line) or ("avg" in line): 
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
    print ("min, max = ",minval, maxval)

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
     print (n,m,ln,lm)

     print ("thrsmax = %f"%thrsmax)
     print ("thrsmin = %f"%thrsmin)

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

                #print ("%s %s %6.2f %s"%(lab1[i],lab2[j], mat[i][j], lpair))
                print ("%s %s %6.2f %s"%(lab2[i],lab1[j], mat[i][j], lpair))


def keep_three_max(maxv,maxi,maxj,i,j,val):

   # skip if val is equal to start
   if val == -10000.0 : 
   #    print("In keep_three_max: skip if val is equal to start. this is likely true for the frist recurtions ")
       return
   #print("val = %f"%val)
   #print("max three: %f,%f,%f"%(maxv[0],maxv[1],maxv[2]))

   if (maxv[0] < val):
       oldval = maxv[0]
       oldi = maxi[0]
       oldj = maxj[0]
       maxv[0] = val
       maxi[0] = i
       maxj[0] = j
       keep_three_max(maxv,maxi,maxj,oldi,oldj,oldval) # see if the oldval is should be in maxv[1] or maxv[2]
   elif (maxv[1] < val):
       oldval = maxv[1]
       oldi = maxi[1]
       oldj = maxj[1]
       maxv[1] = val
       maxi[1] = i
       maxj[1] = j
       keep_three_max(maxv,maxi,maxj,oldi,oldj,oldval) # see if the oldval should be in maxv[2]
   elif (maxv[2] < val):
       maxv[2] = val
       maxi[2] = i
       maxj[2] = j
   return 
 
def keep_three_min(minv,mini,minj,i,j,val):

   # skip if val is equal to start
   if val == 10000.0: 
   #    print("In keep_three_min: skip if val is equal to start. this is likely true for the frist recurtions ")
       return
   #print("val = %f"%val)
   #print("min three: %f,%f,%f"%(minv[0],minv[1],minv[2]))

   if (minv[0] > val):
       oldval = minv[0]
       oldi = mini[0]
       oldj = minj[0]
       minv[0] = val
       mini[0] = i
       minj[0] = j
       keep_three_min(minv,mini,minj,oldi,oldj,oldval) # see if the oldval is should be in minv[1] or minv[2]
   elif (minv[1] > val):
       oldval = minv[1]
       oldi = mini[1]
       oldj = minj[1]
       minv[1] = val
       mini[1] = i
       minj[1] = j
       keep_three_min(minv,mini,minj,oldi,oldj,oldval) # see if the oldval should be in minv[2]
   elif (minv[2] > val):
       minv[2] = val
       mini[2] = i
       minj[2] = j
   return 


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
     #maxv[0] = maxv[1] = maxv[2] = Mat[0][0]
     #minv[0] = minv[1] = minv[2] = Mat[0][0]

     #for i in range(m):
     #    for j in range(n):
     for i in range(0,m):
         for j in range(0,n):

             val = Mat[i][j]
             # look to see if it val is biger then the max (0) if not check the next (1) and then the next (2)
             keep_three_max(maxv,maxi,maxj,i,j,val)
             keep_three_min(minv,mini,minj,i,j,val)
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
     #print("i=%d,j=%d"%(xres,yres))
     #print("i=%d,j=%d,red(i)=%s,res(j)=%s"%(xres,yres,xlabel[int(xres)],ylabel[int(yres)]))
     print("j=%d,i=%d,res(j)=%s,res(i)=%s,val[i,j]=%f"%(xres,yres,xlabel[int(xres)],ylabel[int(yres)],Mat[int(yres),int(xres)]))
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
         #item.set_fontsize(3)
         item.set_fontsize(8)
     for i in range(n):
         #labels = ax.xaxis.get_major_ticks()[i].label
         labels = ax.get_xticklabels()[i]
         #labels.set_fontsize(3)
         labels.set_fontsize(8)
         labels.set_rotation('vertical')

     [xstart,xstop] = get_range_for_zoomin(xres,n,11)
     [ystart,ystop] = get_range_for_zoomin(yres,m,11)
     #[ystart,ystop] = get_range_for_zoomin(yres,n,10)

     ax.set_xlim([xstart,xstop])
     ax.set_ylim([ystart,ystop])
     #ax.plot(xres,yres,'k*')
     ax.plot(xres,yres,syb)

# y is row
# y is lab1

# x is col
# x is lab2

def subset_row_column(mat,keep_row,keep_col,lab1,lab2):

     print("starting subset_row_column")
     m = len(mat) # row 
     n = len(mat[0]) # col
     lm = len(lab2)
     ln = len(lab1)
     print ("n (col) = %d \n m (row) = %d \n lab2 (ln) = %d \n lab1 (lm) = %d \n "%(n,m,ln,lm))

     new_m = len(keep_row)
     new_n = len(keep_col)
     print (new_m, new_n)

     #new_mat = numpy.zeros([new_m,new_n])
     new_mat = numpy.zeros([new_n,new_m])

     new_lab1 = []
     new_lab2 = []

     for i in keep_row:
        i = i-1
        print(i)
        new_lab1.append(lab1[i])

     for j in keep_col:
        j = j-1
        print(j)
        new_lab2.append(lab2[j])

     for i,i_ori in enumerate(keep_row):
        i_ori = i_ori-1
        for j,j_ori in enumerate(keep_col):
            j_ori = j_ori-1
            print(i,j,i_ori,j_ori)
            new_mat[j][i] = mat[int(j_ori)][int(i_ori)]
     print("leaving remove_row_column")

     return new_mat, new_lab1, new_lab2
         
def read_label(lab1file):
     flabel1 = open(lab1file,'r')
     label = []
     for line in flabel1:
          temp = len(line.split())
          if temp == 0:
              continue
          label.append(line.strip())
     flabel1.close()
     return label


#def heatmap(Mat,label,filename,threshold,heatmap_threshold):
#def heatmap(Mat0,filename,heatmap_threshold,cmin,cmax,lab1file,lab2file):
def heatmap(Mat0,filename,heatmap_threshold,cmin,cmax,ylabel,xlabel):
#def heatmap(Mat0,filename,heatmap_threshold,cmin,cmax,xlabel,ylabel):
     m = len(Mat0)
     n = len(Mat0[0])
     print ("num_row = %d\nnum_col=%d"%(m,n))
     print ("num_ylab=%d"%len(ylabel))
     print ("num_xlab=%d"%len(xlabel))
     #exit()

     Mat, vec1, vec2 = mat_to_mat(Mat0) 
     #flabel1 = open('../resnames.1.txt','r')
     #flabel2 = open('../resnames.2.txt','r')
     #flabel1 = open(lab1file,'r')
     #flabel2 = open(lab2file,'r')
     #xlabel = []
     #for line in flabel2:
     #     temp = len(line.split())
     #     if temp == 0:
     #         continue
     #     xlabel.append(line.strip())
     #ylabel = []
     #for line in flabel1:
     #     temp = len(line.split())
     #     if temp == 0:
     #         continue
     #     ylabel.append(line.strip())
     #flabel1.close()
     #flabel2.close()

     mat_larger_mag(Mat0,xlabel,ylabel,cmax,cmin)

     fig = pylab.figure(figsize=(8,8))

     ax1 = fig.add_axes([0.04,0.1,0.1,0.6])
     matplotlib.pyplot.plot(vec1,range(0,m),'k-') # draws a datshed line where dendogram is cut.
     #ax1.set_xticks([])
     ax1.set_yticks([])
     ax1.set_ylim(-0.5, m-0.5)
     for tick in ax1.get_xticklabels():
       tick.set_rotation(90)
     #ax1.set_xlim(cmin,cmax)
        
     ax2 = fig.add_axes([0.3,0.75,0.6,0.2])
     print (vec2)
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
         print (mp)
         print ("threshold = " + str(heatmap_threshold) + "is too high or low") 
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
         #item.set_fontsize(3)
         item.set_fontsize(8)

     for i in range(n):
         #labels = axmatrix.xaxis.get_major_ticks()[i].label
         labels = axmatrix.get_xticklabels()[i]
         #labels.set_fontsize(3)
         labels.set_fontsize(8)
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
     fig.clear()

     return

def subset_file_reader(filename):
    print(filename)
    fh = open(filename)
    setnums = []
    labels = []
    for line in fh: 
        #print(line)
        splitline = line.split(':')
        num = int(splitline[0])
        newlabel = splitline[1][10:20].strip()
        #print(newlabel)
        setnums.append(num)
        labels.append(newlabel)
    return setnums, labels

def main():
  if len(sys.argv) != 9: # if no input
     print ("syntax: matrix file, heatmap_threshold heatmap_min heatmap_max label1_filename label2_filename, subsetfile1, subsetfile2")
     print ("Error:  you have entered the wrong number of inputs:")
     print (len(sys.argv))
     exit

  print ("You have entered in the right number of inputs:")
  file1name  = sys.argv[1] 
  heatmap_threshold  = float(sys.argv[2])
  vmin               = float(sys.argv[3])
  vmax               = float(sys.argv[4])
  flab1               = sys.argv[5] 
  flab2               = sys.argv[6] 
  subsetfile1        = sys.argv[7]
  subsetfile2        = sys.argv[8]

  set1,lab_n1 = subset_file_reader(subsetfile1)
  set2,lab_n2 = subset_file_reader(subsetfile2)

  lab1 = read_label(flab1)
  lab2 = read_label(flab2)
  #exit

  if (vmin > vmax): 
     print ("error:heatmap_min > heatmap_max")
     exit()
  print ("input matrix file = " + file1name)

  fname = file1name
  file1handel = open(fname,'r')
  m_t = readmatrix(file1handel)
  file1handel.close()
  xl = len(m_t)
  yl = len(m_t[0])

  m = numpy.zeros([xl,yl]) 
  for i in range(xl):
      for j in range(yl):
           m[i,j] = m_t[i][j]

  print(len(lab1))
  print(len(lab2))
  print (m.shape)
  #subset_row_column(mat,keep_row,keep_col,lab1,lab2) 
  new_mat, new_lab1, new_lab2 = subset_row_column(m,set1,set2,lab1,lab2) 

  print("compare lab1")
  print(len(new_lab1))
  print(len(lab_n1))
  print(new_lab1)
  print(lab_n1)
  print("compare lab2")
  print(len(new_lab2))
  print(len(lab_n2))
  print(new_lab2)
  print(lab_n2)

  print (new_mat.shape)
  #exit()
  #write_mat(m,file1name+'_out.csv')
  #heatmap(m,file1name+'_out',heatmap_threshold,vmin,vmax,lab_n1,lab_n2)
  #heatmap(new_mat,file1name+'_out',heatmap_threshold,vmin,vmax,lab_n1,lab_n2)
  heatmap(new_mat,file1name+'_out',heatmap_threshold,vmin,vmax,lab_n2,lab_n1)
  return
  #SimlesToFingerPrint("CCC") 
  #SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
  ###SimlesToFingerPrint("C[C@@H](C(=O)Nc1ccccc1)Sc2nnc(n2C)c3cccnc3") 
 
main()

