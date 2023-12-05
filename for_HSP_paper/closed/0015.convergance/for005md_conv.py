
import matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running
import sys
import copy
import math
import scipy
import numpy
import pylab
import time_conv_lib as conv 


# in amber if the entree has a stars then it is too big to show. 
def check_stars( val ): 

    if '**' in val: 
        return 10000 
#    if val > 100: cap
#        return 100
    return val

def read_MD_outfile(filename,totE, kE, pE, time, temp, pres, vol):

    fileh = open(filename,'r')


    result_flag = False    
    count  = 0
    for line in fileh:
        t_vol = 0.0 # for NPT volume is not reported
        line = line.strip('\n')
        splitline = line.split()
        if "4.  RESULTS" in line:
            result_flag = True
        elif "A V E R A G E S   O V E R" in line:
            result_flag = False 

        if (result_flag):
           if "NSTEP" in line:
              if (len(splitline)<11):
                  continue
              t_time = float(splitline[5])/1000.0 # convert from ps to ns
              t_temp = float(splitline[8])
              t_pres = float(splitline[11])
              time.append(t_time)
              temp.append(t_temp)
              pres.append(t_pres)
              vol.append(t_vol) # intialize
           if "Etot" in line: 
              if (len(splitline)<8):
                  continue
              t_totE = float(check_stars(splitline[2]))
              t_kE   = float(check_stars(splitline[5]))
              t_pE   = float(check_stars(splitline[8]))
              totE.append(t_totE)
              kE.append(t_kE)
              pE.append(t_pE)
           if  "VOLUME" in line:
              #t_vol = float(splitline[9])
              # print line, splitline, splitline[8]
              t_vol = float(splitline[8])
              #vol.append(t_vol)
              vol[-1] = t_vol
    fileh.close()
    return totE, kE, pE, time, temp, pres, vol

def main():

    if len(sys.argv) != 3:
      print ("error:  this program takes 2 inputs:")
      print ("   (1) filename that contains a list of md output files. If it doesn't exist do sth like this: ")
      print ("        ls 5609039/*.out > tmpout.txt")
      print ("   (2) filename for png plot")
      print ("        This should be done automatically as part of 005md.checkMDrun.csh")
      exit()

    filelist        = sys.argv[1]
    filenamepng     = sys.argv[2]

    # read in file with a list of mdout files.
    print ("filelist containing MD.out files: " + filelist)
    print ("Plot will be saved as: " + filenamepng)
    filenamelist = []
    fileh = open(filelist,'r')

    for line in fileh:
        tfile = line.strip("\n")
        splitline = tfile.split(".")
        if (splitline[-1] != "out"):
            print ("Error. %s is not a .out file" % tfile)
            exit()
        filenamelist.append(tfile)
    fileh.close()
    totE = []
    kE   = []
    pE   = []
    time = []
    temp = []
    pres = []
    vol  = []

    for filename in filenamelist:
        print ("reading info from file: " + filename)
        totE, kE, pE, time, temp, pres, vol = read_MD_outfile(filename,totE, kE, pE, time, temp, pres, vol)

    # Plot with 5 panels; tabs [x_left,y_left,x_up,y_up].
    subpanel = [ [0.2,0.1,0.3,0.2], [0.6,0.1,0.3,0.2], [0.2,0.4,0.3,0.2], [0.6,0.4,0.3,0.2], [0.2,0.7,0.3,0.2], [0.6,0.7,0.3,0.2] ]
    descname = ["totE", "kE", "pE", "temp", "pres", "vol"]
    fig = pylab.figure(figsize=(8,8))
    for i,desc in enumerate([totE, kE, pE, temp, pres, vol]):
       #print len(desc), len(totE), len(time)

       axis = fig.add_axes(subpanel[i])
       #lim_min = min(math.floor(Ymin),math.floor(Xmin))
       # lim_max = max(math.ceil(Ymax), math.ceil(Xmax))
       im = axis.plot(time,desc,'k-') #,[0,100],[0,100],'--')
       #axis.set_xlabel("time (ps)")
       axis.set_xlabel("time (ns)")
       axis.set_ylabel(descname[i])
       #axis.set_title('file='+xyfilename)
       #axis.set_ylim(lim_min, lim_max)
       #axis.set_xlim(lim_min, lim_max)
    #fig.savefig('md_analysis_fig.png',dpi=600) 
    fig.savefig(filenamepng,dpi=600) 

    
    subpanel = [ [0.2,0.1,0.3,0.2], [0.6,0.1,0.3,0.2], [0.2,0.4,0.3,0.2], [0.6,0.4,0.3,0.2], [0.2,0.7,0.3,0.2], [0.6,0.7,0.3,0.2] ]
    fig = pylab.figure(figsize=(8,8))
    axis = fig.add_axes(subpanel[0])
    axis.plot(time,totE,'k-') #,[0,100],[0,100],'--')
    sw_time,sw_totE = conv.sliding_wendow(time,totE,100) 
    axis.plot(sw_time,sw_totE,'g-') #,[0,100],[0,100],'--')
    axis.set_xlabel("time (ns)")
    axis.set_ylabel("TotE (kcal/mol)")
    axis.set_title("Sliding window")
    acf_totE = conv.ACF(totE,1)
    axis = fig.add_axes(subpanel[1])
    axis.plot(acf_totE,'k-')
    axis.set_title("Auto-correlation function")
    blocks_totE = conv.BASEM(totE,100)
    axis = fig.add_axes(subpanel[2])
    axis.plot(blocks_totE,'k-')
    axis.set_title("Block averages")
    axis = fig.add_axes(subpanel[3])
    m,b,totEfit = conv.fit_line(time,totE)
    axis.plot(time,totE,'k.',time,totEfit,'g-')
    axis.text(0.95, 0.01, 'y = %f x + %f'%(m,b),
        verticalalignment='bottom', horizontalalignment='right',
        transform=axis.transAxes,
        #color='green', fontsize=15)
        color='green', fontsize=8)
    fig.savefig(filenamepng.replace('.png','')+"_converge.png",dpi=600) 

main()

