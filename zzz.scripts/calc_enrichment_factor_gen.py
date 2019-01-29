
# Written by Trent Balius. 

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
 
 numsel =  numtot * frac

 #print numlig,numdec,numtot,numsel

 fh_extract = open(extractallfile,'r')
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
