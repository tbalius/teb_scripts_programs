#!/usr/bin/python

# This script will generate a DMS (discret molecular Surface) using Chimera.
# Writen by Trent E Balius, Shoichet Lab, 2013
# modified from
# http://plato.cgl.ucsf.edu/pipermail/chimera-users/2011-March/006130.html

import sys
from chimera import runCommand, openModels, MSMSModel
from WriteDMS import writeDMS

def main():
  if len(sys.argv) != 3: # if no input
     print "ERORR"
     return
  input_mol2 = sys.argv[1]
  output_dms = sys.argv[2]

  runCommand("open " + input_mol2)

  # generate surface using 'surf' command
  runCommand("surf")
  # get the surf object
  surf = openModels.list(modelTypes=[MSMSModel])[0]
  # write DMS
  writeDMS(surf, output_dms)
  return

main()
  
