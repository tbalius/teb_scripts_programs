import sys, os, math
import tanimoto_tversky_cal_axon_lib as tccalc 
# writen by Trent Balius in 2016

def main():
  if (len(sys.argv) != 4): # if no input
     print "ERORR"
     print "syntexs: python best_frist_tc_clusters.py smiles1 outputprefix threshold"
     return

  smilesfile1   = sys.argv[1]
  outfileprefix = sys.argv[2]
  tc_threshold  = float(sys.argv[3])

  outfileF = outfileprefix +'.fp'

  pid = str(os.getpid()) # get the process idenifier so that we do not right over the same file. 

  # read in names from smiles file.  
  names = []
  file1 = open(smilesfile1,'r')
  for line in file1:
      name = line.split()[1]  
      #print line, name
      names.append(name)
  file1.close()

  
  # if the fp file already exists, just read in the fingerprints.  
  # otherwise caluclate the fingerprints.
  if (os.path.isfile(outfileF) ):
     print outfileF + "exists."
     fpvec1 = []
     file1 = open(outfileF)
     for line in file1:
         fp = line.split()[2]
         #print fp
         fpvec1.append(fp)
  else:
     fpvec1 = tccalc.get_fp(smilesfile1,outfileF,pid)

  # make dictionary of footprints and 1-tc values.
  fp_dic = {}
  tc_dic = {}
  for i in range(len(fpvec1)):
      name = names[i]
      fp   = fpvec1[i]
      fp_dic[name] = fp
      tc_dic[name] = -1.0

  # best frist clustering. 
  # -- pick the top ranked molecule (frist in the list), 
  # -- write out everything close to that molecule, 
  # -- append everything else to a new list.  
  # -- replace the old list with the new list 
  name_list = names
  name_newlist  = []
  cluster = 1
  tc_thres = tc_threshold
  first_pass = True
  while( len(name_list) > 0): # loop until the list is empty
       outclusterfile = outfileprefix+".cluster."+str(cluster)
       file1 = open(outclusterfile,'w') # open up the file for current cluster.
       fp1 = fp_dic[name_list[0]] # pick the top molecule
       onentc_1_2 =  1.0-tc_dic[name_list[0]] # this is one minus the tc. 
       print "on cluster %d - 1-tc=%f"%(cluster,onentc_1_2)
       for i,name in enumerate(name_list):
             fp2 = fp_dic[name]
             onentc_1_3 = 1.0-tc_dic[name]
             if ((not first_pass) and (math.fabs(onentc_1_2 - onentc_1_3) > (1-tc_thres))): # by minipulating the triangle inequality.
                print i, "inequality, not in cluster", onentc_1_2, onentc_1_3 
                name_newlist.append(name) # not put in cluster
             elif ((not first_pass) and (onentc_1_2 + onentc_1_3 <= (1-tc_thres))):
                # this should never be true here, because 2, and 3 would be already in cluster 1, if it were true, which is a contradiction. 
                print i, "inequality, in cluster", onentc_1_2, onentc_1_3 
                TC = 1 - ( onentc_1_2 + onentc_1_3 )
                print name_list[0]+','+name+": <= "+str(TC) 
                file1.write('%s,<=%f\n'%(name,TC)) # write out everything close to that molecule, in the current cluster file.
             else: 
                TC = tccalc.tanimoto(fp1,fp2)
                if (TC > tc_thres):
                    print i
                    print name_list[0]+','+name+":"+str(TC) 
                    file1.write('%s,%f\n'%(name,TC)) # write out everything close to that molecule, in the current cluster file.
                else:
                    if (first_pass):
                       tc_dic[name] = TC
                    name_newlist.append(name) # append everything else to a new list
       first_pass = False
       file1.close() # close the file for the current cluster.
       name_list = name_newlist # replace the old list with the new list 
       name_newlist = []
       cluster = cluster+1 # increment the cluster name. 

main()

