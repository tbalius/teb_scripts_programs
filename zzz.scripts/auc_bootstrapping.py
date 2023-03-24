
## Written by Trent Balius at FNLCR, 2023/03/24 
## we use DUDEZ paper as insperation.  
## https://pubs.acs.org/doi/full/10.1021/acs.jcim.0c00598

import sys
import copy
import math
import matplotlib
matplotlib.use('Agg')  # allows you to not have an x-server running
import matplotlib.pyplot
import numpy
import os

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
    
def bootstrap_sample(values,arrays,num):
    import random
    # values is the list of value we start with, 
    # arrays is a empty list of lists that will be populated, 
    # num is the number of lists to generate
    arrays.clear()
    size = len(values)
    for i in range(num):
        temp_array = []
        for j in range(size):
            #random.uniform(a, b)
            k = round(random.uniform(0, size-1),0)
            print("random = %f"%k)
            value = float(values[int(k)])
            temp_array.append(value)
        arrays.append(temp_array)  

def sortSecond(val):
    return val[1]

def cal_auc_logauc_fromsamples(arraylig,arraydec,dirname):
    text_score_array=[]
    lignames = []
    decnames = []
    count=0

    # check if the dir exists.  
    if (os.path.exists(dirname)): 
        return

    #format_extract = "./AB/                     27991 %16s 1                    2702       2702    0.10  11         1      1612      1     1     0.00    0.00    0.00   0.00    0.00    0.00    0.00    0.00    0.00    %6.2f\n"
    format_extract = "./AB/                     27991 %16s 1                    2702       2702    0.10  11         1      1612      1     1     0.00    0.00    0.00   0.00    0.00    0.00    0.00    0.00    0.00    %6.2f"
    # for ligands
    for i in range(len(arraylig)):
        name = "ligand%06d"%i
        print (name)
        text_score = [format_extract%(name,arraylig[i]),arraylig[i]] 
        text_score_array.append(text_score)
        lignames.append(name)
    # for decoys
    for i in range(len(arraydec)):
        name = "decoy%06d"%i
        print (name)
        text_score = [format_extract%(name,arraydec[i]),arraydec[i]] 
        text_score_array.append(text_score)
        decnames.append(name)

    print(text_score_array[0][1])    
    text_score_array.sort(key=sortSecond)
    print(text_score_array[0][1])    
    #exit()
    

    cwd = os.getcwd()
    os.mkdir(dirname)
    os.chdir(dirname) 

    fh = open("ligand.name",'w')
    for name in lignames:
        fh.write('%s\n'%name)
    fh.close()

    fh = open("decoy.name",'w')
    for name in decnames:
        fh.write('%s\n'%name)
    fh.close()

     
    fh = open("extract_all.sort.uniq.txt",'w')
    for string,score in text_score_array:
        print(score)
        fh.write('%s\n'%string)
    fh.close()

    os.system('python ~/zzz.github/DOCK_dev_2020_12_01/ucsfdock/analysis/enrich.py -i ./ -l ligand.name -d decoy.name')

    os.chdir(cwd)     

    return
    



def main(): 
     import statistics as stat
     CNUM = 22
     #MAXSCORE = 100.0
     MAXSCORE_pad = 10.0
     
     extract_filename = sys.argv[1]
     lig_filename = sys.argv[2]
     decoy_filename = sys.argv[3]
     num_boot = int(sys.argv[4])
     
     print("extract:"+extract_filename)
     print("ligand: "+lig_filename)
     print("decoy: "+decoy_filename)
     print("number_of_bootstraps: %d"%num_boot)
     
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

     lig_arrays = []
     dec_arrays = []
     bootstrap_sample(elig,lig_arrays,num_boot)
     bootstrap_sample(edec,dec_arrays,num_boot)

     #i = 0
     #cal_auc_logauc_fromsamples(lig_arrays[i],dec_arrays[i],"boot%d"%i)
     cmd = ''
     auclist = []
     logauclist = []
     for i in range(num_boot):
        cal_auc_logauc_fromsamples(lig_arrays[i],dec_arrays[i],"boot%d"%i)
        cmd = cmd+" -i ./boot%d"%i 
        fh = open("./boot%d/roc_own.txt"%i)
        sline = fh.readline().split()
        if (sline[0] != "#AUC"):
           print(sline)
           print("Error: #AUC need to be frist in line") 
           exit()
        auc = float(sline[1])
        logauc = float(sline[3])
        print(auc,logauc)
        auclist.append(auc)
        logauclist.append(logauc)

     print ("AUC mean = %f\n"%stat.mean(auclist) )
     print ("AUC stdev = %f\n"%stat.stdev(auclist) )
     print ("logAUC mean = %f\n"%stat.mean(logauclist) )
     print ("logAUC stdev = %f\n"%stat.stdev(logauclist) )
     
     os.system('python ~/zzz.github/DOCK_dev_2020_12_01/ucsfdock/analysis/plots.py'+cmd)
     
     

     #max_e = max(max(elig),max(edec))      
     #min_e = min(min(elig),min(edec))      
     #
     ## calculate the bins to use for the histogram and the mid bin value to use in ploting the overlay of the histograms
     #delta = 1.0
     #print(min_e, max_e)
     #size = 50
     #bin_e = numpy.linspace(min_e-delta, max_e+delta, num=size)
     #mid_bin_e = numpy.zeros(size-1)
     #for i in range(1,size):
     #    mid_bin_e[i-1] = (bin_e[i]+bin_e[i-1])/2
     #     
     #
     #fig = matplotlib.pyplot.figure(figsize=(8, 8), dpi=600)
     ##ax = matplotlib.pyplot.axes([0.2, 0.3, 0.7, 0.6])
     #ax = matplotlib.pyplot.axes([0.1, 0.1, 0.8, 0.2])
     #print(elig[0:10])
     #pl,temp1,temp2 = ax.hist(elig,bin_e)
     
     #ax = matplotlib.pyplot.axes([0.1, 0.4, 0.8, 0.2])
     #print(edec[0:10])
     #pd,temp1,temp2 = ax.hist(edec,bin_e)
     ##print(pl) 
     ##print(pd) 

     #ax = matplotlib.pyplot.axes([0.1, 0.7, 0.8, 0.2])
     #for i in range(size-1):
     #    pl[i] = pl[i]/len(elig)
     #    pd[i] = pd[i]/len(edec)
     #ax.plot(mid_bin_e,pl,'r-',mid_bin_e,pd,'b-')
     #fig.savefig('fig_hist.png',dpi=600)
    
main() 
