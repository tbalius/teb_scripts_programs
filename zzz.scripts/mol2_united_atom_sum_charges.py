
import mol2
import sys


polar_heavy = [ "N.3", "N.2", "N.1", "N.ar", "N.am", "N.pl3", "N.4", "O.3", "O.2", "O.co2", "O.spc", "O.t3p", "S.3", "S.2", "S.O", "S.O2" ]

def combine_q_and_remove_hydrogens(m):
    atom_list = []
    bond_list = []
    #residue_list = {}
    atom_keep_dict = {}

    # proceed with only bonds containing 1 heavy atom and 1 hydrogen atom
    # check if it is a polar hydrogen ( if so continue)
    # add hydrogen charge to that of the heavy atom
    for bond_id in range(len(m.bond_list)):
        #retain_bond = True
        bond = m.bond_list[bond_id]
        a1 = m.atom_list[bond.a1_num-1]
        a2 = m.atom_list[bond.a2_num-1]
        #print (a2.type, a1.type)
        if (a1.heavy_atom and a2.heavy_atom):
            bond_list.append(bond)
            atom_keep_dict[bond.a1_num-1] = True
            atom_keep_dict[bond.a2_num-1] = True
            continue
        # Atoms down here are always hydrogen 
        elif (a1.heavy_atom):
           if (a1.type in polar_heavy):
               print ("polar ",a2.type, a1.type)
               bond_list.append(bond)
               atom_keep_dict[bond.a1_num-1] = True
               atom_keep_dict[bond.a2_num-1] = True
               continue
           print bond.a1_num, bond.a1_num,  m.atom_list[bond.a1_num-1].Q, m.atom_list[bond.a2_num-1].Q
           m.atom_list[bond.a1_num-1].Q = m.atom_list[bond.a1_num-1].Q + m.atom_list[bond.a2_num-1].Q
           m.atom_list[bond.a2_num-1].Q = 0 
           atom_keep_dict[bond.a1_num-1] = True
           atom_keep_dict[bond.a2_num-1] = False
        elif (a2.heavy_atom):
           if (a2.type in polar_heavy):
               print (a2.type, a1.type)
               bond_list.append(bond)
               atom_keep_dict[bond.a1_num-1] = True
               atom_keep_dict[bond.a2_num-1] = True
               continue
           print bond.a1_num, bond.a1_num,  m.atom_list[bond.a1_num-1].Q, m.atom_list[bond.a2_num-1].Q
           m.atom_list[bond.a2_num-1].Q = m.atom_list[bond.a2_num-1].Q + m.atom_list[bond.a1_num-1].Q
           m.atom_list[bond.a1_num-1].Q = 0 
           atom_keep_dict[bond.a2_num-1] = True
           atom_keep_dict[bond.a1_num-1] = False // hydrogen

    for atom_id in range(len(m.atom_list)):
       if (atom_keep_dict[atom_id]):
          atom_list.append(m.atom_list[atom_id])

    # Assuming that residue list does not change

    m2 = mol2.Mol(m.header,m.name,atom_list,bond_list,m.residue_list)
    #return data
    return m2


print "this file requiers the mol2 libary writen by trent balius and sudipto mukherjee"

print "syntex: mol2_removeH.py input_file output_file"

infile = sys.argv[1]
outfile = sys.argv[2]
mol_list = mol2.read_Mol2_file(infile)
print len(mol_list)
mol1 = combine_q_and_remove_hydrogens(mol_list[0])
#mol = mol2.remove_hydrogens( mol1 )
#mol2.write_mol2(mol,outfile)
mol2.write_mol2(mol1,outfile)

