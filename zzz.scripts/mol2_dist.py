import sys, mol2
import copy

## Writen by Trent Balius in the Shoichet Group
## shifts a mol2 file cordenates along the x axis. 

def is_bonded(mol,i,j):
    for bond in mol.bond_list:
        if ((bond.a1_num == (i+1) and bond.a2_num == (j+1)) or 
            (bond.a1_num == (j+1) and bond.a2_num == (i+1))):
            return True 
    return False

def dist_mol2(mol,tval):
    for i in range(len(mol.atom_list)): 
        for j in range(i+1,len(mol.atom_list)): 
            if (is_bonded(mol,i,j)):
               #print "bond"
               continue

            dist = ((mol.atom_list[i].X - mol.atom_list[j].X )**2.0
                 +  (mol.atom_list[i].Y - mol.atom_list[j].Y )**2.0
                 +  (mol.atom_list[i].Z - mol.atom_list[j].Z )**2.0)
            dist = (dist)**(1.0/2.0)
            if (dist < tval):
                print dist, mol.atom_list[i].name,mol.atom_list[i].num, mol.atom_list[j].name, mol.atom_list[j].num
    return

def main():
   if len(sys.argv) != 2: # if no input
      print "ERORR"
      return
   namemol2in        = sys.argv[1]
   mols  = mol2.read_Mol2_file(namemol2in)
   count = 0
   for mol in mols:
       print "mol%d"%(count)
       dist_mol2(mol,1.70)
       count = count + 1

main()


