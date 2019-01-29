#! /bin/python

import tanimoto_cal_axon as tca
import sys
import math
 

def main():
   SmilesString1 = sys.argv[1]
   SmilesString2 = sys.argv[2]
   print SmilesString1, SmilesString2

   mw1 = float(tca.molecularMass(SmilesString1))
   mw2 = float(tca.molecularMass(SmilesString2))

   print mw1, mw2, math.fabs(mw1-mw2)

   

   formula1 = tca.MolecularFormula(SmilesString1)
   formula2 = tca.MolecularFormula(SmilesString2)
   val = tca.compareFormula(formula1,formula2)
   

main()
