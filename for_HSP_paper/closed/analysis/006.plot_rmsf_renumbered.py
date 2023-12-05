

import sys
import copy

import math

import matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running

import scipy, pylab, numpy


## Writen by Trent Balius, 2019 

dict_path = "/mnt/projects/RAS-CompChem/static/Mayukh/HSP83_for_Lorenzo/lookup_table_Closed.txt"
resi_dict = {}

with open(dict_path, 'r') as dictfile:
  for line in dictfile:
    linesplit = line.strip().split()
    key = "%s" %(linesplit[4])
    value = "%s" %(linesplit[2])
    resi_dict[key] = value

def read_rmsf_dat_file(filehandel):
    # si is the user specified i value
    # sj is the user specified j value
    rmsf = []
    resid = []
    renumbered_resid = []
    for line in filehandel:
        if "Frame" in line: 
            continue
        if "Res" in line:
	    continue
        splitline = line.strip().split()
        #resid.append(float(splitline[0]))
        resid.append(int(float(splitline[0])))
        rmsf.append(float(splitline[1]))
	renumbered_resid = [resi_dict[str(res)] for res in resid]
    return rmsf, renumbered_resid



#def heatmap(Mat,label,filename,threshold,heatmap_threshold):
def make_plot(val_array,rid_array,title,filename):

     print "Here in make_plot"
     fig = pylab.figure(figsize=(8,8))

     ax1 = fig.add_axes([0.1,0.1,0.6,0.2])
     matplotlib.pyplot.plot(range(0,len(val_array)),val_array,'k-') # draws a datshed line where dendogram is cut.
     ax1.set_title(title)
     ax1.set_xticks(range(0,len(val_array),1))
     ax1.set_xticklabels(rid_array[::1])
     ax1.set_yticks(range(0,int(max(val_array)+2)))
     ax1.set_xlabel('Residue number')
     ax1.set_ylabel('RMSF ($\mathrm{\AA}$)')
     m = len(range(0,len(val_array),1))  
     for i in range(m):
         labels = ax1.xaxis.get_major_ticks()[i].label
         labels.set_fontsize(10)
         labels.set_rotation(90)

     #ax2 = fig.add_axes([0.75,0.1,0.2,0.2])
     #n1_1, bins, patches = ax2.hist(val_array, normed=1, histtype='bar',orientation="horizontal")
     #ax2.set_yticks([])
     #fig.show()
     fig.savefig(filename+'.png',dpi=600)   
     return


def main():
  if len(sys.argv) != 4: # if no input
     print "syntax:  rmsd dat file, title of plot, output prefix"
     print "Error:  you have entered the wrong number of inputs:"
     print len(sys.argv)
     exit()

  print "You have entered in %d inputs:"%(len(sys.argv))
  file1name  = sys.argv[1] 
  title     = sys.argv[2] 
  output    = sys.argv[3] 

  #print "input matrix file prefix = " + file1name+'.'+str(i)
  file1handel = open(file1name,'r')
  rv,rid = read_rmsf_dat_file(file1handel)
  file1handel.close()
  make_plot(rv,rid,title,output)
  return
 
main()

