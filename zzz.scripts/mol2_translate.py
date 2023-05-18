import sys, mol2_python3
import copy

## Writen by Trent Balius in the Shoichet Group
## shifts a mol2 file cordenates in the x,y,z directions. 


def shift_mol2(fileprefix,ori_mol,xtran,ytran,ztran):
    mol = copy.copy(ori_mol)
    namemol2 = fileprefix+"_"+str(xtran)+"_"+str(ytran)+"_"+str(ztran)+".mol2"
    for i in range(len(mol.atom_list)): 
        mol.atom_list[i].X = mol.atom_list[i].X + xtran
        mol.atom_list[i].Y = mol.atom_list[i].Y + ytran
        mol.atom_list[i].Z = mol.atom_list[i].Z + ztran
    mol2.write_mol2(mol,namemol2)
    return

def main():
  if len(sys.argv) != 6: # if no input
     print ("ERORR.") 
     print ("syntax: namemol2in namemol2outprefix xtran ytran ztran")
     return
  namemol2in        = sys.argv[1]
  namemol2outprefix = sys.argv[2]
  xtran = float(sys.argv[3])
  ytran = float(sys.argv[4])
  ztran = float(sys.argv[5])
  mol  = mol2.read_Mol2_file(namemol2in)[0]
  shift_mol2(namemol2outprefix, mol,xtran,ytran,ztran)
main()


