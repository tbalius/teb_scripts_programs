
import sys
#import chimera
from chimera import runCommand, openModels
from WriteMol2 import writeMol2
from DockPrep import prep

## Writen by Trent E Balius, Shoichet Group
## This script is made based on the following dockfans entry:
## http://mailman.docking.org/pipermail/dock-fans/2007-May/001043.html
def main():
  print sys.argv
  if len(sys.argv) != 3 and len(sys.argv) != 4: # if no input
     print "ERROR: Wrong number of inputs"
     print "syntax: chimera --nogui --script \"chimera_dockprep.py pdbinput output_prefix keepH\""
     print len(sys.argv)
     return

  #models = openModels.list(modelTypes=[chimera.Molecule])

  input_pdb     = sys.argv[1]
  output_prefix = sys.argv[2]
  if len(sys.argv) == 4:
      if (sys.argv[3] == 'yes'):
          keepH = True
      elif (sys.argv[3] == 'no'): 
          keepH = False
      else: 
          print("keepH must be yes or no, setting it to no.")
          keepH = False

  else:
      keepH = False

  print "pdb input = " + input_pdb 
  print "output prefix = " + output_prefix

  #runCommand("open " + input_pdb)
  #models = chimera.openModels.list(modelTypes=[chimera.Molecule])
  #model = models
  model = openModels.open(input_pdb)
  if not (keepH):
     runCommand("del @H,H?,H??,H???") # remove all hydrogens
  
  writeMol2(model, output_prefix+"before_dockprep.mol2")

  prep(model)

  runCommand("write 0 "+output_prefix+".pdb")
  writeMol2(model, output_prefix+".mol2")
  
  runCommand("del HC") # remove all non-polar hydrogens
  runCommand("write 0 "+output_prefix+"_polarH.pdb")
  runCommand("del @H,H?,H??,H???") # remove all hydrogens
  runCommand("write 0 "+output_prefix+"_noH.pdb")

main()

