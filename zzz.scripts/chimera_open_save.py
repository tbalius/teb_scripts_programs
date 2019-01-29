
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
  if len(sys.argv) != 3: # if no input
     print "ERROR: Wrong number of inputs"
     print "syntax: chimera --nogui --script \"chimera_open_save.py pdbinput output_prefix\""
     print len(sys.argv)
     return

  #models = openModels.list(modelTypes=[chimera.Molecule])

  input_file     = sys.argv[1]
  output_prefix = sys.argv[2]

  print "input = " + input_file 
  model = openModels.open(input_file)
  writeMol2(model, output_prefix+"_chimera.mol2")

main()

