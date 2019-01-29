#! /bin/python

import tanimoto_cal_axon as tca
import sys
 

def main():
   SmilesString = sys.argv[1]
   print SmilesString
   mw = tca.molecularMass(SmilesString)
   print mw

main()
