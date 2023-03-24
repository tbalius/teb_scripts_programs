
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
         #print (line.strip())
         name = line.split()[0]
         names.append(name)

def make_energy_array(dic,maxscore,name_array,score_array):
     # dic is a dictionary of names with scores as entries.
     # maxscore is the value assigned if there is not entry for a name in the dictionary
     # name_array is a list of names to look up the score value associated in the dictionary and store it in the score_array
     # score_array is empty but will be popuated here with scores. 
     #print (name_array)
     #exit()
     for name in name_array:
         #print(name)
         score = float(maxscore)
         if name in dic:
             score = float(dic[name])
         score_array.append(score)
         #print(score)    
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
            #print("random = %f"%k)
            value = float(values[int(k)])
            temp_array.append(value)
        arrays.append(temp_array)  

def bootstrap_sample_pair(values,values2,arrays,arrays2,num):
    import random
    # values is the list of value we start with, 
    # arrays is a empty list of lists that will be populated, 
    # num is the number of lists to generate
    # note that the arrays values and values2 will be in the same order because the ligands or decoys lists (read from ligand.name or decoy.name) are in the same order.  
    arrays.clear()
    if len(values) != len(values2): 
        print(len(values), len(values2)) 
        print("Error.  bootstrap_sample_pair values and values2 sizes must be the same...")
        exit()

    size = len(values)
    for i in range(num):
        temp_array = []
        temp_array2 = []
        for j in range(size):
            #random.uniform(a, b)
            k = round(random.uniform(0, size-1),0)
            #print("random = %f"%k)
            value = float(values[int(k)])
            value2 = float(values2[int(k)])
            temp_array.append(value)
            temp_array2.append(value2)
        arrays.append(temp_array)  
        arrays2.append(temp_array2)  


def sortSecond(val):
    return val[1]

def cal_auc_logauc_fromsamples(arraylig,arraydec,dirname):
#def cal_auc_logauc_fromsamples(arraylig,arraydec,lignames,decnames,ligfile,decfile,dirname):
#def cal_auc_logauc_fromsamples(arraylig,arraydec,lignames,decnames,dirname):
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
        #name = lignames[i]
        #print (name)
        text_score = [format_extract%(name,arraylig[i]),arraylig[i]] 
        text_score_array.append(text_score)
        lignames.append(name)
    # for decoys
    for i in range(len(arraydec)):
        name = "decoy%06d"%i
        #name = decnames[i]
        #print (name)
        text_score = [format_extract%(name,arraydec[i]),arraydec[i]] 
        text_score_array.append(text_score)
        decnames.append(name)

    #print(text_score_array[0][1])    
    text_score_array.sort(key=sortSecond)
    #print(text_score_array[0][1])    
    #exit()
    

    cwd = os.getcwd()
    os.mkdir(dirname)
    os.chdir(dirname) 

    # make a dulicate of the ligand.name file.  
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
        #print(score)
        fh.write('%s\n'%string)
    fh.close()

    os.system('python ~/zzz.github/DOCK_dev_2020_12_01/ucsfdock/analysis/enrich.py -i ./ -l ligand.name -d decoy.name')
    #print('python ~/zzz.github/DOCK_dev_2020_12_01/ucsfdock/analysis/enrich.py -i ./ -l %s/%s -d %s/%s'%(cwd,ligfile,cwd,decfile)
    #os.system('python ~/zzz.github/DOCK_dev_2020_12_01/ucsfdock/analysis/enrich.py -i ./ -l %s/%s -d %s/%s'%(cwd,ligfile,cwd,decfile)

    os.chdir(cwd)     

    return
    
def read_extract(dic,filename,colnum):
     fh = open(filename,'r')
     for line in fh:
         #print (line.strip())
         splitline = line.split()
         #print(len(splitline))
         if len(splitline) != colnum: 
            exit()
         name = splitline[2]
         energy = splitline[colnum-1]
         if name in dic: 
             print("Warning...")
         dic[name] = energy
     fh.close()

def compare_lists(list1,list2):
     # this fuction compares to lists of strings
     # if they are the same it returns true. 
     # if they are different it returns false.
     if len(list1)!=len(list2): 
        return False
     for i in range(len(list1)): 
         if (list1[i]!=list2[i]):
             return False
     return True

def max_value(dic):
     # get the max value from the dictionary.  This is so that any ligand or decoy can be assigned a max value.  
     max_val = -1000.0
     for key in dic.keys():
          if float(dic[key]) > max_val: 
             max_val = float(dic[key])
     #max_val_ten = round(max_val/10,0)*10
     max_val_ten = math.ceil(max_val/10)*10
     print ("max value = %6.3f; rounded to nearest ten (ceiling): %6.3f"%(max_val,max_val_ten))
     #exit()
     return max_val_ten

def main(): 
     import statistics as stat
     CNUM = 22
     #MAXSCORE = 100.0
     MAXSCORE_pad = 10.0

     if (len(sys.argv) == 5):      
         extract_filename = sys.argv[1]
         lig_filename = sys.argv[2]
         decoy_filename = sys.argv[3]
         num_boot = int(sys.argv[4])
         flag_pair = False
     elif (len(sys.argv) == 8):
         extract_filename = sys.argv[1]
         lig_filename = sys.argv[2]
         decoy_filename = sys.argv[3]
         extract_filename2 = sys.argv[4]
         lig_filename2 = sys.argv[5]
         decoy_filename2 = sys.argv[6]
         num_boot = int(sys.argv[7])
         flag_pair = True
     else: 
         print ("Error: incorrect number of inputs" )
         print ("syntax (4 inputs): extract_filename lig_filename decoy_filename num_boot" )
         print ("syntax (7 inputs for pair calculation): extract_filename lig_filename decoy_filename extract_filename2 lig_filename2 decoy_filename2 num_boot" )
         exit()

     print("extract:"+extract_filename)
     print("ligand: "+lig_filename)
     print("decoy: "+decoy_filename)
     if flag_pair: 
        print("extract2:"+extract_filename2)
        print("ligand2: "+lig_filename2)
        print("decoy2: "+decoy_filename2)
     print("number_of_bootstraps: %d"%num_boot)
     
     # read in the arrays of values and names and store it in a dictionary
     #fh = open('ligand_scored.mol2','r')
     Energy_dic = {};
     read_extract(Energy_dic,extract_filename,CNUM)
     if flag_pair: 
        Energy_dic2 = {};
        read_extract(Energy_dic2,extract_filename2,CNUM)

     # read in list of names of ligand and decoys
     ligands = []
     decoys = []
     read_names(lig_filename,ligands)
     read_names(decoy_filename,decoys)

     max_val_ten = max_value(Energy_dic)

     if flag_pair: 
         ligands2 = []
         decoys2 = []
         read_names(lig_filename2,ligands2)
         read_names(decoy_filename2,decoys2)
         if not compare_lists(ligands,ligands2):
            print("Error. ligands are not the same...")
            print("run two times instead of pair run.")
            exit() 
         if not compare_lists(decoys,decoys2):
            print("Error. ligands are not the same...")
            print("run two times instead of pair run.")
            exit() 

         max_val_ten2 = max_value(Energy_dic2)
             

     # get scores for the set of ligands and decoys
     elig = []
     edec = []
     make_energy_array(Energy_dic,max_val_ten+MAXSCORE_pad,ligands,elig)
     make_energy_array(Energy_dic,max_val_ten+MAXSCORE_pad,decoys,edec)
     if flag_pair: 
        elig2 = []
        edec2 = []
        make_energy_array(Energy_dic2,max_val_ten2+MAXSCORE_pad,ligands2,elig2)
        make_energy_array(Energy_dic2,max_val_ten2+MAXSCORE_pad,decoys2,edec2)

     lig_arrays = []
     dec_arrays = []
     if not flag_pair:
        bootstrap_sample(elig,lig_arrays,num_boot)
        bootstrap_sample(edec,dec_arrays,num_boot)
     elif flag_pair:
        lig_arrays2 = []
        dec_arrays2 = []
        bootstrap_sample_pair(elig,elig2,lig_arrays,lig_arrays2,num_boot)
        bootstrap_sample_pair(edec,edec2,dec_arrays,dec_arrays2,num_boot)
        

     cmd = ''
     auclist = []
     logauclist = []

     if flag_pair:
        cmd2 = ''
        auclist2 = []
        logauclist2 = []
        diffauclist = []
        difflogauclist = []

     for i in range(num_boot):
        #cal_auc_logauc_fromsamples(lig_arrays[i],dec_arrays[i],ligands,decoys,"boot_%d"%i)
        cal_auc_logauc_fromsamples(lig_arrays[i],dec_arrays[i],"boot_%d"%i)
        cmd = cmd+" -i ./boot_%d"%i 
        if flag_pair:
            #cal_auc_logauc_fromsamples(lig_arrays2[i],dec_arrays2[i],ligands2,decoys2,"boot2_%d"%i)
            cal_auc_logauc_fromsamples(lig_arrays2[i],dec_arrays2[i],"boot2_%d"%i)
            cmd2 = cmd2+" -i ./boot2_%d"%i 

        fh = open("./boot_%d/roc_own.txt"%i)
        sline = fh.readline().split()
        fh.close()
        if (sline[0] != "#AUC"):
           print(sline)
           print("Error: #AUC need to be frist in line") 
           exit()

        auc = float(sline[1])
        logauc = float(sline[3])
        auclist.append(auc)
        logauclist.append(logauc)

        if flag_pair:
           fh = open("./boot2_%d/roc_own.txt"%i)
           sline = fh.readline().split()
           fh.close()
           if (sline[0] != "#AUC"):
              print(sline)
              print("Error: #AUC need to be frist in line")
              exit()
           auc2 = float(sline[1])
           logauc2 = float(sline[3])
           auclist2.append(auc2)
           logauclist2.append(logauc2)

        if not flag_pair: 
            print(auc,logauc)
        if flag_pair: 
            print(auc,auc2,logauc,logauc2)
            diffauc = auc - auc2
            difflogauc = logauc - logauc2
            diffauclist.append(diffauc)
            difflogauclist.append(difflogauc)

     print ("AUC mean = %f\n"%stat.mean(auclist) )
     print ("AUC stdev = %f\n"%stat.stdev(auclist) )
     print ("logAUC mean = %f\n"%stat.mean(logauclist) )
     print ("logAUC stdev = %f\n"%stat.stdev(logauclist) )
     if flag_pair: 
        print ("AUC2 mean = %f\n"%stat.mean(auclist2) )
        print ("AUC2 stdev = %f\n"%stat.stdev(auclist2) )
        print ("logAUC2 mean = %f\n"%stat.mean(logauclist2) )
        print ("logAUC2 stdev = %f\n"%stat.stdev(logauclist2) )
        print ("diffAUC mean = %f\n"%stat.mean(diffauclist) )
        print ("diffAUC stdev = %f\n"%stat.stdev(diffauclist) )
        print ("difflogAUC mean = %f\n"%stat.mean(difflogauclist) )
        print ("difflogAUC stdev = %f\n"%stat.stdev(difflogauclist) )
     
     os.system('python ~/zzz.github/DOCK_dev_2020_12_01/ucsfdock/analysis/plots.py'+cmd)
     
     if flag_pair: 
         #os.system('python ~/zzz.github/DOCK_dev_2020_12_01/ucsfdock/analysis/plots.py'+cmd2)
         print('python ~/zzz.github/DOCK_dev_2020_12_01/ucsfdock/analysis/plots.py'+cmd2)
     
     

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
