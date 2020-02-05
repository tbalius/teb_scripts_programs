#!/usr/bin/env python

# This script was written by Trent Balius at FNLCR in 2020/02/04 

#from __future__ import print_function
#import itertools
import sys

from rdkit.Chem import (
    MolFromSmiles,
    MolToSmiles,
    AddHs
)

from rdkit.Chem.Descriptors import MolLogP, MolWt
from rdkit.Chem.rdChemReactions import ReactionFromSmarts
from rdkit import Chem

def main():
   if len(sys.argv) != 4:
#     print "besure to source /nfs/soft/www/apps/zinc15/envs/production/env.csh"
     print ("example: ")
     print ('python search_smi_for_smarts_file.py "[C:1]=[C:2]-[C:3]=[O:4]" input.smi output.smi')
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
   patt = Chem.MolFromSmarts(smarts)
   for line in fh: # read in a line, which contains a smiles
       if 'smiles' in line: 
           continue
       #print(line)
       splitline = line.split()
       smi2 = splitline[0]
       name = splitline[1]
       m = Chem.MolFromSmiles(smi2)
       if m.HasSubstructMatch(patt):
          fho.write(line)
   fh.close()
   fho.close()
main()
