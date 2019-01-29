#!/usr/bin/env python
# Written by Trent Balius modified from
# ~xyz/code/tools/apps/reactor/reactsmi.py
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
#try:
#    from flask import (
#        abort,
#        Flask, 
#        redirect,
#        render_template,
#        request,
#        Response,
#        url_for,
#    )
#except ImportError:
#    Flask = None
#
#
#DEBUG = True



#def reaction():
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
    print "Products: "
    for product in products:
       for mol in product:
          smiles_p =  MolToSmiles(mol, isomericSmiles=True)
          print(smiles_p)
    #for product in products:
    #     print(product)
    #     
    #     smiles_p =  MolToSmiles(product, isomericSmiles=True)
    #     print(smiles_p)

def main():
   if len(sys.argv) != 4:
     print "besure to source /nfs/soft/www/apps/zinc15/envs/production/env.csh"
     print "example: "
     print 'python simple_reaction.py "[SiH3:5].[C:1]=[C:2]-[C:3]=[O:4]>>[SiH3:5]-[C:1]-[C:2]-[C:3]=[O:4]" "[SiH3]" "CNCCCCNCCC=C-C(=O)CCCNCCCCNCCCCC"'
     exit()
   smarts = sys.argv[1]
   smi1 = sys.argv[2]
   smi2 = sys.argv[3]

   print "smarts = " + smarts
   print "smiles = " + smi1
   print "smiles = " + smi2

   reaction(smarts,smi1,smi2)
main()
