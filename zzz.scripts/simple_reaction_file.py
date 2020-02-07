#!/usr/bin/env python
# Written by Trent Balius modified from
# ~xyz/code/tools/apps/reactor/reactsmi.py
# this will react. 
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
#
#    #smarts = '[13CH3:5].[C:1]=[C:2]-[C:3]=[O:4]>>[13CH3:5]-[C:1]-[C:2]-[C:3]=[O:4]'
#    #smiles1 = '[13CH3]'
#    smarts = '[SiH3:5].[C:1]=[C:2]-[C:3]=[O:4]>>[SiH3:5]-[C:1]-[C:2]-[C:3]=[O:4]'
#    smiles1 = '[SiH3]'
#    smiles2 = 'CNCCCCNCCC=C-C(=O)CCCNCCCCNCCCCC'

def reaction(smarts,smiles1,smiles2):

    rxn = ReactionFromSmarts(smarts) 
    mole1 = MolFromSmiles(smiles1)  
    mole2 = MolFromSmiles(smiles2)  

    #prod1 = rxn.RunReactants(mole1)
    #prod2 = rxn.RunReactants(mole2)
    #smiles_p =  MolToSmiles(prod1, isomericSmiles=True)
    #print(smiles_p)

    mols = [mole1, mole2]
    products = rxn.RunReactants(mols)
    #print "Products: "
    list_prod = []
    for product in products:
       for mol in product:
          smiles_p =  MolToSmiles(mol, isomericSmiles=True)
          list_prod.append(smiles_p)
          #print(smiles_p)
    #for product in products:
    #     print(product)
    #     
    #     smiles_p =  MolToSmiles(product, isomericSmiles=True)
    #     print(smiles_p)
    return list_prod

def main():
   if len(sys.argv) != 5:
#     print "besure to source /nfs/soft/www/apps/zinc15/envs/production/env.csh"
     print ("example: ")
     print ('python simple_reaction.py "[SiH3:5].[C:1]=[C:2]-[C:3]=[O:4]>>[SiH3:5]-[C:1]-[C:2]-[C:3]=[O:4]" "[SiH3]" input.smi output.smi')
     print ('input file will contain: \n CNCCCCNCCC=C-C(=O)CCCNCCCCNCCCCC lig')
     exit()
   smarts = sys.argv[1]
   smi1 = sys.argv[2]
   inputsmi = sys.argv[3]
   outputsmi = sys.argv[4]

   print ("smarts = " + smarts)
   print ("smiles = " + smi1)
   print ("input smi file = " + inputsmi)
   print ("output smi file = " + outputsmi)

   fh = open(inputsmi,'r')  # open up for reading,  file of reactants
   fho = open(outputsmi,'w') # open up for writting, file of products
   count = 1
   for line in fh: # read in a line, which contains a smiles
       splitline = line.split()
       smi2 = splitline[0]
       name = splitline[1]
       plist = reaction(smarts,smi1,smi2) # products list
       for p in plist:
           fho.write('%s %s\n'%(p, name+'_'+str(count)))
           count = count+1
main()
