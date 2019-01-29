
# Written by Trent Balius. 

import os
import sys


def cal_enrichment(systdir,frac):
 lines = open(systdir+"ligands.name",'r').readlines()

 lig_name_dic = {}
 for line in lines:
     name = line.split()[0]
     #print name
     lig_name_dic[name] = 0
 
 numlig = len(lines)
 numdec = len(open(systdir+"decoys.name",'r').readlines())
 numtot = numlig+numdec
 
 numsel =  numtot * frac

 #print numlig,numdec,numtot,numsel

 fh_extract = open(systdir+"extract_all.sort.uniq.txt",'r')
 count = 0
 ligsel = 0
 for line in fh_extract:
     if (count > numsel): # when we have read all the top one percent then break out of loop
        #print "breaking the loop"
         break
     name = line.split()[2]
     #print name
     if name in lig_name_dic:
        #print name
        ligsel = ligsel+1
     count = count + 1

 fh_extract.close()

#print systdir
#print ligsel,numlig,numdec,numtot,numsel

 EF = (float(ligsel)/float(numsel))/(float(numlig)/float(numtot))
#print "EF1% = ", EF

 return EF

#systdir = "2RGP_GIST_0p5/ROC_ligdecoy/"
#systdir = "2RGP_GIST/ROC_ligdecoy/"
#systdir = "2RGP/ROC_ligdecoy/"
syslist = ["3EML","1E66","2E1W","1L2S","3ODU","2RGP","3KL6","2NNQ","2V3F","1XL2","3CCW","1UYG","2ICA","3G0E","2B8T","2OF2","1B9V","3L3M","2OWB","2P54","2AZR","1NJS","3EL8","1YPE","2AYW"]

#frac = 0.001
#frac = 0.01
frac = 0.1
EF_s = []
EF_g = []
EF_g0p5 = []
dif1 = []
dif2 = []
for pdb in syslist:
   dir1 = pdb+"/ROC_ligdecoy/"
   tEF_s = cal_enrichment(dir1,frac)
   EF_s.append(tEF_s)
   dir2 = pdb+"_GIST/ROC_ligdecoy/"
   tEF_g = cal_enrichment(dir2,frac)
   EF_g.append(tEF_g)
   dir3 = pdb+"_GIST_0p5/ROC_ligdecoy/"
   tEF_g0p5 = cal_enrichment(dir3,frac)
   EF_g0p5.append(tEF_g0p5)

   dif1.append(tEF_g-tEF_s)
   dif2.append(tEF_g0p5-tEF_s)

   print pdb, tEF_s,tEF_g0p5, tEF_g, (tEF_g-tEF_s),(tEF_g0p5-tEF_s)

#plot()
