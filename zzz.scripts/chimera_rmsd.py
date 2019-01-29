
import sys
#import chimera
from chimera import runCommand, openModels
from WriteMol2 import writeMol2
from DockPrep import prep

## Writen by Trent E Balius, Shoichet Group

def main():
  print sys.argv
  if len(sys.argv) != 3: # if no input
     print "ERROR: Wrong number of inputs"
     print "syntax: /nfs/software/chimera/current/bin/chimera --nogui --script 'chimera_rmsd.py temp.txt \"#0:107-115@N,CA,C,O #1:107-115@N,CA,C,O\" '"
     print len(sys.argv)
     return

  #models = openModels.list(modelTypes=[chimera.Molecule])

  input_list_file = sys.argv[1]
  #output_prefix   = sys.argv[2]
  seltion_rmsd    = sys.argv[2]
  print "pdb inputs    = " + input_list_file
  #print "output prefix = " + output_prefix
  print "seltion_rmsd = " + seltion_rmsd

  fileh = open(input_list_file)
  lines = fileh.readlines()
  N     = len(lines)
  print "there are N systems:" + str(N)

  fileh.close()


  #seltion_align = "#0:1-115@N,CA,C,O #1:107-115@N,CA,C,O"
  #seltion_rmsd  = "#0:107-115@N,CA,C,O #1:107-115@N,CA,C,O"

  #calulate alignment. 
  # this will already be aligned. 
  #templete = lines[0]
  #runCommand("open "+ templete)
  #for pdb_file in lines:
  #    runCommand("open "+ pdb_file) 
  #    runCommand(ma

  #seltion = "#0:111@N,CA,C,O #1:111@N,CA,C,O"
  #seltion = "#0:108@N,CA,C,O #1:108@N,CA,C,O"

  for i in range(0,N):
      pdb_file1 = lines[i].strip('\n')
      runCommand("open "+ pdb_file1)
      #for pdb_file2 in lines:
      for j in range(i+1,N):
          pdb_file2 = lines[j].strip('\n')
          print '\n########\n files:  ' + pdb_file1 +"   "+ pdb_file2 + '\n########\n' 
          #sys.stdout = open(output_prefix+"_"+str(i)+"_"+str(i)+".txt", 'w')
          runCommand("open "+ pdb_file2)
          runCommand("rmsd " + seltion_rmsd)
          #print "rmsd_Text", rmsd_Text
          runCommand("del #1")
          #runCommand("write 0 "+output_prefix+"_polarH.pdb")
          #sys.stdout.close()

      runCommand("del #0")
  

main()

