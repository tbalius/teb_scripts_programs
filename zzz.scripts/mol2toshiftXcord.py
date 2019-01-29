import sys, mol2
import copy

## Writen by Trent Balius in the Shoichet Group
## shifts a mol2 file cordenates along the x axis. 


def shift_mol2(fileprefix,ori_mol):
    mol = copy.copy(ori_mol)
    step = 0.03
    name = 0.03
    for i in range(10):
       #outmol2 = open(fileprefix+"."+str(var)+".mol2",'w')
       namemol2 = fileprefix+"."+str(name)+".mol2"
       print len(mol.atom_list)
       for i in range(len(mol.atom_list)): 
           mol.atom_list[i].X = mol.atom_list[i].X + step
       mol2.write_mol2(mol,namemol2)
       name = name + 0.03 
    return

def main():
  if len(sys.argv) != 3: # if no input
     print "ERORR"
     return
  namemol2in        = sys.argv[1]
  namemol2outprefix = sys.argv[2]
  mol  = mol2.read_Mol2_file(namemol2in)[0]
  shift_mol2(namemol2outprefix, mol)
main()


