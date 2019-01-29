
import mol2
import sys


def combine_q_and_remove_hydrogens(m):
    atom_list = []
    bond_list = []
    residue_list = {}

    # Retain only bonds containing heavy atoms
    for bond_id in range(len(m.bond_list)):
        retain_bond = True
        bond = m.bond_list[bond_id]
        a1 = m.atom_list[bond.a1_num-1]
        a2 = m.atom_list[bond.a2_num-1]
        if (a1.heavy_atom and a2.heavy_atom):
            continue
        # Atoms down here are always hydrogen 
        elif (a1.heavy_atom):
           print bond.a1_num, bond.a1_num,  m.atom_list[bond.a1_num-1].Q, m.atom_list[bond.a2_num-1].Q
           m.atom_list[bond.a1_num-1].Q = m.atom_list[bond.a1_num-1].Q + m.atom_list[bond.a2_num-1].Q
           m.atom_list[bond.a2_num-1].Q = 0 
        elif (a2.heavy_atom):
           print bond.a1_num, bond.a1_num,  m.atom_list[bond.a1_num-1].Q, m.atom_list[bond.a2_num-1].Q
           m.atom_list[bond.a2_num-1].Q = m.atom_list[bond.a2_num-1].Q + m.atom_list[bond.a1_num-1].Q
           m.atom_list[bond.a1_num-1].Q = 0 

    # Assuming that residue list does not change

    #data = mol2.Mol(m.header,m.name,atom_list,bond_list,m.residue_list)
    #return data
    return m


print "this file requiers the mol2 libary writen by trent balius and sudipto mukherjee"

print "syntex: mol2_removeH.py input_file output_file"

infile = sys.argv[1]
outfile = sys.argv[2]
mol_list = mol2.read_Mol2_file(infile)
print len(mol_list)
mol1 = combine_q_and_remove_hydrogens(mol_list[0])
mol = mol2.remove_hydrogens( mol1 )
mol2.write_mol2(mol,outfile)

