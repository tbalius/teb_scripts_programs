
import sys
#import chimera
from chimera import runCommand, openModels
from WriteMol2 import writeMol2
from DockPrep import prep

## Writen by Trent E Balius, Shoichet Group
## This script is made based on the following dockfans entry:

def main():
  print sys.argv
  if len(sys.argv) != 3: # if no input
     print "ERROR: Wrong number of inputs"
     print "syntax: chimera --nogui --script \"chimera_move_pdb.py pdbinput output_prefix\""
     print len(sys.argv)
     return


  input_pdb     = sys.argv[1]
  output_prefix = sys.argv[2]

  print "pdb input = " + input_pdb 
  print "output prefix = "+ output_prefix
  model = openModels.open(input_pdb) 

  #prep(model)
  start = 0.0
  #list = [start]
  for i in range(10):
      start = start + 0.03
      #list.append(start)
      runCommand("move x 0.03 ")
      print output_prefix+"."+str(start)+".pdb"
      runCommand("write 0 "+output_prefix+"."+str(start)+".pdb")

  #runCommand("write 0 "+output_prefix+".pdb")
  #writeMol2(model, output_prefix+".mol2")
  
  #runCommand("del HC") # remove all non-polar hydrogens
  #runCommand("write 0 "+output_prefix+"_polarH.pdb")

main()

