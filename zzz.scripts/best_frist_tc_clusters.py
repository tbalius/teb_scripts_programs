import sys, os
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

  outfileC = outfileprefix +'.clusters'

  # initialize cluster array
  clusters = []
  tcs      = []
  i = 0
  while(i < len(fpvec1)):
       print i
       clusters.append(0)
       tcs.append(1.0)
       i = i+1


  # best frist clustering. 
  #tc_thres = 0.4
  tc_thres = tc_threshold
  cluster_num = 1
  for i,fp1 in enumerate(fpvec1):
     print i 
     if (clusters[i] !=0):
        continue # skip if the molecule is all ready asigned to a cluster.
     clusters[i] = cluster_num # asign a cluster number to the next best molecule
     for j,fp2 in enumerate(fpvec1):
        if (clusters[j] !=0):
           continue # skip if the molecule is all ready asigned to a cluster.
        TC = tccalc.tanimoto(fp1,fp2)
        #print TC
        if i == j: #skip it if they are the same
           continue
        if (TC > tc_thres):
           print cluster_num, i,j
           clusters[j] = cluster_num
           tcs[j]      = TC
     cluster_num = cluster_num + 1

  file1 = open(outfileC,'w')
  for i in range(len(clusters)):
      file1.write('%s,%d,%f\n' % (names[i],clusters[i],tcs[i]) )
  file1.close()
main()

