#!/bin/python3

## This script is writen by
## Trent E Balius
## 2021/10/13 at FNLCR 
################################################################
## This script  
## scrapes the pdb for the ligand names assoiated with a pdb file. 
## And get the smiles for these ligands. 
################################################################

## wget https://files.rcsb.org/ligands/view/AQ4_ideal.sdf .

## search header for HET https://files.rcsb.org/header/1M17.pdb


import sys,urllib
import urllib.request

def get_lig_from_pdbcode(pdb):
    url = 'https://files.rcsb.org/header/%s.pdb'%pdb
    webfile = urllib.request.urlopen(url)
    flag = False
    lignames = []
    for line in webfile:
    #     print(line)
         #if flag: # this line contains smi.
         #   smiles=str(line).strip().replace("'"," ").split()[1].replace('\\n','')
         #   break
         if "HET " in str(line):
             print(line)
             print(str(line).split()[1])
             lignames.append(str(line).split()[1])
             flag = True

    webfile.close()
    print(lignames)
    return lignames


def get_smiles(ligresid):
    #url = 'http://zinc.docking.org/results/structure?structure.smiles='+smiles+'&structure.similarity=' + similarity
    #url = 'http://www.rcsb.org/pdb/ligand/ligandsummary.do?hetId=' + ligresid
    url = 'https://files.rcsb.org/ligands/view/%s_ideal.sdf'%ligresid
    
    #print "url = " + url
    
    #page=requests.get(url)
    
    #webfile = urllib.urlopen(url)
    webfile = urllib.request.urlopen(url)
    flag = False
    smiles = "" 
    for line in webfile:
         #print(line)
         if flag: # this line contains smi.
            smiles=str(line).strip().replace("'"," ").split()[1].replace('\\n','') 
            break
         if "OPENEYE_ISO_SMILES" in str(line): 
             flag = True
             
    webfile.close()
    print(smiles) 
    return smiles


if len(sys.argv) != 2:
    print ("Error: one arguments is needed")
    print ("list of ligand name")
    sys.exit()

filepdb     = sys.argv[1]

fh = open(filepdb,'r')



for line in fh:
  pdb = line.split()[0]
  listlig = get_lig_from_pdbcode(pdb)
  fileoutput = pdb+".smi"
  fileh = open(fileoutput,'w')
  for ligresid in listlig: 
      smiles = get_smiles(ligresid)
      fileh.write(smiles+' '+ligresid+'\n')
  fileh.close()


