
# Written by Trent Balius. 
# comments/edits by MF - March 2017

# needs 4 files as input upon calling:
# 1) ligand names file (full path) -> normally: docking/2runEnrich/4NVA_gist/ROC_ligdecoy/ligands.name
# 2) decoy names file (full path) -> normally: docking/2runEnrich/4NVA_gist/ROC_ligdecoy/decoys.name
# 3) extract_all sort uniq file -> docking/2runEnrich/4NVA_gist/ROC_ligdecoy/extract_all.sort.uniq.txt
# 4) define % fraction: e.g. give 1  1% for EF1

# potential source for error: just gets length of decoy file for calculation not number via names as for ligands

import os
import sys


def cal_enrichment(ligandfile,decoyfile,extractallfile,frac):
 lines = open(ligandfile,'r').readlines()

 lig_name_dic = {}
 for line in lines:
     name = line.split()[0]
     #print name
     lig_name_dic[name] = 0
 
 numlig = len(lines)
 numdec = len(open(decoyfile,'r').readlines())
 numtot = numlig+numdec
 
 numsel =  numtot * float(frac/100)

 print numlig,numdec,numtot,numsel,lig_name_dic

 fh_extract = open(extractallfile,'r')
 read_extract = fh_extract.readlines()
 fh_extract.close()
 count = 0
 ligsel = 0
 for line in read_extract:
     print(count)
     splitline = line.strip().split()
     if (count > numsel): # when we have read all the top one percent then break out of loop
        #print "breaking the loop"
         break
     print(numsel)
     #name = line.split()[2]
     name = splitline[2].split(".")[0]
     #print name
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


#frac = 0.001
#frac = 0.01
def main():
   ligands    = sys.argv[1]
   decoys     = sys.argv[2]
   extractall = sys.argv[3]
   #frac = 0.1
   frac = float(sys.argv[4])
   print "ligand names file (full path) = %s"%ligands
   print "decoy names file (full path) = %s"%decoys
   print "extract all (full path) = %s"%extractall
   print "frac = %f percent"%frac

   EF = cal_enrichment(ligands,decoys,extractall,frac)

   print "EF%3.1f = %f"%(frac,EF)

#plot()
main()
