
import mol2_python3 as mol2
import sys

# This function read in mol2 file, atom type 1, atom type 2, atom type 3, output name
# it searches for a bond that formed with an atom that has the search type (atom_t_search)
# check if its partner atom has the atomtype (atom_t_ori) that needs to be replace then replace with the new type (atom_t_replac)

def loop_bonds(atom_t_ori,atom_t_replace,atom_t_search,mol):

    for bond in mol.bond_list:
        if (mol.atom_list[bond.a1_num-1].type == atom_t_search):
           print (bond.a1_num, bond.a2_num)
           print (mol.atom_list[bond.a1_num-1].type, mol.atom_list[bond.a2_num-1].type)
           if (mol.atom_list[bond.a2_num-1].type == atom_t_ori):
                mol.atom_list[bond.a2_num-1].type = atom_t_replace
                print ("replace")
                #print (bond.a1_num, bond.a2_num)
                #print (mol.atom_list[bond.a1_num-1].type, mol.atom_list[bond.a2_num-1].type)
        if (mol.atom_list[bond.a2_num-1].type == atom_t_search):
           print (bond.a1_num, bond.a2_num)
           print (mol.atom_list[bond.a1_num-1].type, mol.atom_list[bond.a2_num-1].type)
           if (mol.atom_list[bond.a1_num-1].type == atom_t_ori):
                mol.atom_list[bond.a1_num-1].type = atom_t_replace
                print ("replace")
                #print (bond.a1_num, bond.a2_num)
                #print (mol.atom_list[bond.a1_num-1].type, mol.atom_list[bond.a2_num-1].type)
            
        #exit()
    return mol 
print ("this file requiers the mol2 libary writen by trent balius and sudipto mukherjee")

print ("syntex: mol2_replace_atomtype_bonds.py input_file output_file, a1_ori,a2_rep,a3_search")

infile = sys.argv[1]
outfile = sys.argv[2]
a1_ori = sys.argv[3] # ori
a2_rep = sys.argv[4]
a3_search = sys.argv[5]

print('infile=%s,\noutfile=%s,\na1_ori=%s,\na2_rep=%s,\na3_search=%s\n'%(infile,outfile,a1_ori,a2_rep,a3_search))

mol_list = mol2.read_Mol2_file(infile)
print (len(mol_list))
count = 0
for mol in mol_list:
    moln = loop_bonds( a1_ori,a2_rep,a3_search,mol )
    if (count == 0): 
        mol2.write_mol2(moln,outfile)
    else: 
        mol2.append_mol2(moln,outfile)
    count = count + 1
print("processed %d mol2 entries"%count)
