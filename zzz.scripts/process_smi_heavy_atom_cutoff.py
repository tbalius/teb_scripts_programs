
# Written by Trent Balius (c) March 9, 2020
# Frederick National Lab for Cancer Research. 
# script to process smiles file

import sys
import rdkit
from rdkit import Chem

def process_smiles(input_smi,output,nmax,nmin):

   infh = open(input_smi,'r')
   outfh = open(output,'w')

   for line in infh: 
      splitline = line.split()
      smi = splitline[0]
      name = splitline[1]
      #if 'p' in smi: 
      #   print(smi,name)
      #   continue
      #print(smi,name)
      try: 
          m = Chem.MolFromSmiles(smi)
      except ValueError: 
          print(smi,name)
          continue 
      if (m is None): 
          print (smi,name)
          continue
      num = Chem.rdchem.Mol.GetNumHeavyAtoms(m) 
      if (num > nmin and num<nmax): 
         outfh.write('%s %s\n'%(smi,name))

def main():

   if (len(sys.argv) != 3): # if no input
        print (" (1) input smiles file")
        print (" (2) output smiles file")
        return

   insmiles  = sys.argv[1]
   outsmiles = sys.argv[2]
 
   print('input file: %s\noutput file:%s\n'%(insmiles,outsmiles))

   process_smiles(insmiles,outsmiles,100,4)
   
main()
