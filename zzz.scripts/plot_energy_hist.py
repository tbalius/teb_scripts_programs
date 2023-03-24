
## Written by Trent Balius at FNLCR, 2023/03/23 
# this script reads in a extract_all file and plots histograms for ligand and decoys.  

import sys
import copy
import math
import matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running
import matplotlib.pyplot
import numpy

def pos_neg(array,p_array,n_array): # pointer to arrays. 

    for i in range(len(array)):
        val_pos = 0.0
        val_neg = 0.0
        if (array[i] <= 0 ):
            val_neg = array[i]
        if (array[i] >0):
            val_pos = array[i]
        p_array.append(val_pos)
        n_array.append(val_neg)

def read_names(filename,names):
     fh = open(filename,'r')
     #names;
     for line in fh:
         print (line.strip())
         name = line.split()[0]
         names.append(name)

def make_energy_array(dic,maxscore,name_array,score_array):
     # dic is a dictionary of names with scores as entries.
     # maxscore is the value assigned if there is not entry for a name in the dictionary
     # name_array is a list of names to look up the score value associated in the dictionary and store it in the score_array
     # score_array is empty but will be popuated here with scores. 
     print (name_array)
     #exit()
     for name in name_array:
         print(name)
         score = float(maxscore)
         if name in dic:
             score = float(dic[name])
         score_array.append(score)
         print(score)    
         #exit()
    
def main(): 
     CNUM = 22
     #MAXSCORE = 100.0
     MAXSCORE_pad = 10.0
     
     extract_filename = sys.argv[1]
     lig_filename = sys.argv[2]
     decoy_filename = sys.argv[3]
     
     print("extract:"+extract_filename)
     print("ligand: "+lig_filename)
     print("decoy: "+decoy_filename)
     
     # read in the arrays of values and names and store it in a dictionary
     #fh = open('ligand_scored.mol2','r')
     fh = open(extract_filename,'r')
     Energy_dic = {};
     for line in fh:
         print (line.strip())
         splitline = line.split()
         print(len(splitline))
         if len(splitline) != CNUM: 
            exit()
         name = splitline[2]
         energy = splitline[CNUM-1]
         if name in Energy_dic: 
             print("Warning...")
         Energy_dic[name] = energy
     fh.close()

     # read in list of names of ligand and decoys
     ligands = []
     decoys = []

     read_names(lig_filename,ligands)
     read_names(decoy_filename,decoys)

     # get the max value from the dictionary.  This is so that any ligand or decoy can be assigned a max value.  
     max_val = -1000.0
     for key in Energy_dic.keys():
          if float(Energy_dic[key]) > max_val: 
             max_val = float(Energy_dic[key])
     #max_val_ten = round(max_val/10,0)*10
     max_val_ten = math.ceil(max_val/10)*10
     print ("max value = %6.3f; rounded to nearest ten (ceiling): %6.3f"%(max_val,max_val_ten))
     #exit()

     # get scores for the set of ligands and decoys
     elig = []
     edec = []
     make_energy_array(Energy_dic,max_val_ten+MAXSCORE_pad,ligands,elig)
     make_energy_array(Energy_dic,max_val_ten+MAXSCORE_pad,decoys,edec)

     max_e = max(max(elig),max(edec))      
     min_e = min(min(elig),min(edec))      

     # calculate the bins to use for the histogram and the mid bin value to use in ploting the overlay of the histograms
     delta = 1.0
     print(min_e, max_e)
     size = 50
     bin_e = numpy.linspace(min_e-delta, max_e+delta, num=size)
     mid_bin_e = numpy.zeros(size-1)
     for i in range(1,size):
         mid_bin_e[i-1] = (bin_e[i]+bin_e[i-1])/2
          
     
     fig = matplotlib.pyplot.figure(figsize=(8, 8), dpi=600)
     #ax = matplotlib.pyplot.axes([0.2, 0.3, 0.7, 0.6])
     ax = matplotlib.pyplot.axes([0.1, 0.1, 0.8, 0.2])
     print(elig[0:10])
     pl,temp1,temp2 = ax.hist(elig,bin_e)
     
     ax = matplotlib.pyplot.axes([0.1, 0.4, 0.8, 0.2])
     print(edec[0:10])
     pd,temp1,temp2 = ax.hist(edec,bin_e)
     #print(pl) 
     #print(pd) 

     ax = matplotlib.pyplot.axes([0.1, 0.7, 0.8, 0.2])
     for i in range(size-1):
         pl[i] = pl[i]/len(elig)
         pd[i] = pd[i]/len(edec)
     ax.plot(mid_bin_e,pl,'r-',mid_bin_e,pd,'b-')
     fig.savefig('fig_hist.png',dpi=600)
    
main() 
