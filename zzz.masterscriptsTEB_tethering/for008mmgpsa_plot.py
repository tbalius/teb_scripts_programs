
import matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running
import sys
import copy
import math
import scipy
import numpy
import pylab

#def read_MD_outfile(filename,totE, kE, pE, time, temp, pres):
#
#    fileh = open(filename,'r')
#
#
#    result_flag = False    
#    count  = 0
#    for line in fileh:
#        line = line.strip('\n')
#        splitline = line.split()
#        if "4.  RESULTS" in line:
#            result_flag = True
#        elif "A V E R A G E S   O V E R" in line:
#            result_flag = False 
#
#        if (result_flag):
#           if "NSTEP" in line:
#              if (len(splitline)<11):
#                  continue
#              t_time = float(splitline[5])/1000.0 # convert from ps to ns
#              t_temp = float(splitline[8])
#              t_pres = float(splitline[11])
#              time.append(t_time)
#              temp.append(t_temp)
#              pres.append(t_pres)
#           if "Etot" in line: 
#              if (len(splitline)<8):
#                  continue
#              t_totE = float(splitline[2])
#              t_kE   = float(splitline[5])
#              t_pE   = float(splitline[8])
#              totE.append(t_totE)
#              kE.append(t_kE)
#              pE.append(t_pE)
#    fileh.close()
#    return totE, kE, pE, time, temp, pres

def read_csv(filename):
   print("start read_csv")
   fh = open(filename)
   count = 0
   vdw=[];es=[];gb=[];apol=[];tot=[];
   for line in fh: 
       splitline=line.strip().split(',')
       if count == 0: 
          header = splitline 
       else: 
          if len(splitline)!=5: 
              print "error"
              exit()
          vdw.append(float(splitline[0]))
          es.append(float(splitline[1]))
          gb.append(float(splitline[2]))
          apol.append(float(splitline[3]))
          tot.append(float(splitline[4]))
       count = count + 1

   print("stop read_csv")
   return header,[vdw,es,gb,apol,tot]

def mean_var(name,array):
    N = len(array)
    meanX = 0
    meanX2 = 0
    for ele in array:
        #if len(ele) != 1: 
        #   print("error")
        #   exit()
        meanX = meanX+ele
        meanX2 = meanX2+ele**2
    meanX=meanX/N
    meanX2=meanX2/N
    varX = meanX2-meanX**2
    print("%s mean=%f var=%f"%(name,meanX,varX))
    #return meanX, varX

def main():

    if len(sys.argv) != 3:
      print "error:  this program takes 2 inputs:"
      print "   (1) filename for csv file with vdw,es,gb,apol,tot "
      print "   (2) filename prefix for png plots"
      print "     "
      exit()

    filename        = sys.argv[1]
    filenamepng     = sys.argv[2]

    # read in file with a list of mdout files.
    print "filename " + filename
    print "Plot file prefix " + filenamepng

    header, data = read_csv(filename)

    # Plot with 5 panels; tabs [x_left,y_left,x_up,y_up].
    subpanel = [ [0.2,0.1,0.3,0.2], [0.6,0.1,0.3,0.2], [0.2,0.4,0.3,0.2], [0.6,0.4,0.3,0.2], [0.2,0.7,0.3,0.2], [0.6,0.7,0.3,0.2] ]
    fig = pylab.figure(figsize=(8,8))
    for i,desc in enumerate(data):
       print("ploting %s"%header[i])
       #print len(desc), len(totE), len(time)
       time = range(1,len(desc)+1)
       axis = fig.add_axes(subpanel[i])
       #lim_min = min(math.floor(Ymin),math.floor(Xmin))
       # lim_max = max(math.ceil(Ymax), math.ceil(Xmax))
       im = axis.plot(time,desc,'k-o') #,[0,100],[0,100],'--')
       axis.set_xlabel("time (ps)")
       axis.set_ylabel(header[i])
       #axis.set_title('file='+xyfilename)
       #axis.set_ylim(lim_min, lim_max)
       #axis.set_xlim(lim_min, lim_max)
    #fig.savefig('md_analysis_fig.png',dpi=600)
    print("saving plot")
    fig.savefig(filenamepng+".EvsT.png",dpi=600) 

    fig = pylab.figure(figsize=(8,8))
    nv = [];mbv=[]
    #cv = ['b','g','r','c','m','orange','yellow','k']
    cv = ['b','g','r','c','m','orange','yellow','k']
    #print len(cv)
    #print cv[0]

   #    b: blue
   #    g: green
   #    r: red
   #    c: cyan
   #    m: magenta
   #    y: yellow
   #    k: black
   #    w: white


    for i,desc in enumerate(data):
       print i
       #n, b, p = axis.hist(cluster2_2_sci, inbins, normed=1, histtype='bar')
       mean_var(header[i],desc)
       axis = fig.add_axes(subpanel[i])
       n, b, p = axis.hist(desc, normed=1, histtype='bar')
       axis.set_xlabel(header[i])
       axis.set_ylabel("pop")

       mb = []
       for j in range(len(b)-1):
           mb.append((b[j]+b[j+1])/2.0)

       #print(mb,b,n)
       #print cv[i]
       axis.plot(mb,n,color=cv[i]) #.

       #print n,b,p
       #print len(n),len(b),len(p)
       nv.append(n)
       mbv.append(mb)

    #print n, bins, patches
    axis = fig.add_axes(subpanel[5])
    for i in range(len(nv)):
       pylab.plot(mbv[i],nv[i],color=cv[i]) #.
    fig.savefig(filenamepng+".hist.png",dpi=600) 

    
    subpanel = [ [0.2,0.1,0.3,0.2], [0.6,0.1,0.3,0.2], [0.2,0.4,0.3,0.2], [0.6,0.4,0.3,0.2], [0.2,0.7,0.3,0.2], [0.6,0.7,0.3,0.2] ]
    fig = pylab.figure(figsize=(8,8))
    axis = fig.add_axes(subpanel[0])
    im = axis.plot(data[1],data[2],'ko') #,[0,100],[0,100],'--')
    max1 = max(data[1])
    min1 = min(data[1])
    max2 = max(data[2])
    min2 = min(data[2])
    maxboth = max([max1, max2])
    minboth = min([min1, min2])
    #print [min1,max1],[min2,max2]
    #im = axis.plot([min1,max1],[min2,max2],'b-') #,[0,100],[0,100],'--')
    #im = axis.plot([minboth,maxboth],[maxboth,minboth],'b-') #,[0,100],[0,100],'--')
    im = axis.plot([minboth,maxboth],[-minboth,-maxboth],'b-') #,[0,100],[0,100],'--')
    axis.set_xlabel(header[1])
    axis.set_ylabel(header[2])
    axis = fig.add_axes(subpanel[1])
    el = []
    for i in range(len(data[1])):
         el.append(data[1][i]+data[2][i])
    time = range(1,len(el)+1)
    im = axis.plot(time,el,'k-o') #,[0,100],[0,100],'--')
    axis.set_xlabel("time (ns)")
    axis.set_ylabel("electrostatics(coul+gb)")
    fig.savefig(filenamepng+".es.gb.png",dpi=600) 


main()

