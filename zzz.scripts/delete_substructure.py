#!/usr/bin/env python
# Written by Trent Balius modified from
# ~xyz/code/tools/apps/reactor/reactsmi.py
# this will react. 
#from __future__ import print_function
#import itertools
import sys

from rdkit.Chem import (
    MolFromSmiles,
    MolFromSmarts,
    MolToSmiles,
    AddHs
)

from rdkit.Chem import AllChem

from rdkit.Chem.Descriptors import MolLogP, MolWt
from rdkit.Chem.rdChemReactions import ReactionFromSmarts

def delete_sub(smarts,smiles):

    #print(smarts,smiles)
    m = MolFromSmiles(smiles)
    patt = MolFromSmarts(smarts)
    #print (m,patt)
    #print("I AM HERE")
    rm = AllChem.DeleteSubstructs(m, patt)
    #rm = AllChem.DeleteSubstructs(smiles,smarts)
    #print("I AM HERE")
    #print(rm)
    smiles_p = MolToSmiles(rm)
    #print(smiles_p)

    return smiles_p

def main():
   if len(sys.argv) != 4:
#     print "besure to source /nfs/soft/www/apps/zinc15/envs/production/env.csh"
     print ("example: ")
     print ('python delect_substructure.py substructure(smarts) input.smi output.smi')
     print ('input file will contain: \n CNCCCCNCCC=C-C(=O)CCCNCCCCNCCCCC lig')
     exit()
   smarts = sys.argv[1]
   inputsmi = sys.argv[2]
   outputsmi = sys.argv[3]

   print ("smarts = " + smarts)
   print ("input smi file = " + inputsmi)
   print ("output smi file = " + outputsmi)

   fh = open(inputsmi,'r')  # open up for reading,  file of reactants
   fho = open(outputsmi,'w') # open up for writting, file of products
   count = 1
   for line in fh: # read in a line, which contains a smiles
       splitline = line.split()
       smi1 = splitline[0]
       #print (smi2)
       name = splitline[1]
       smi2 = delete_sub(smarts,smi1) # products list
       fho.write('%s %s\n'%(smi2, name+'_'+str(count)))
       count = count+1
main()
