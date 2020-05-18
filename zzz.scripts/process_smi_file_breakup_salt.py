
# Written by Trent Balius (c) March 9, 2020
# Frederick National Lab for Cancer Research. 
# script to process smiles file

import sys


def process_smiles(input_smi,output):

   infh = open(input_smi,'r')
   outfh = open(output,'w')

   for line in infh: 
      splitline = line.split()
      smi = splitline[0]
      name = splitline[1]
      split_smi = smi.split('.')
      for smi_p in split_smi:
          outfh.write('%s %s\n'%(smi_p,name))
def main():

   if (len(sys.argv) != 3): # if no input
        print (" (1) input smiles file")
        print (" (2) output smiles file")
        return

   insmiles  = sys.argv[1]
   outsmiles = sys.argv[2]
 
   print('input file: %s\noutput file:%s\n'%(insmiles,outsmiles))

   process_smiles(insmiles,outsmiles)
   
main()
