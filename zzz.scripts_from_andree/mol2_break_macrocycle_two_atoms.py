
# Modified by Andree K Kolliegbo summer 2024. 

import mol2_python3 as mol2
import sys
import copy
import math

print ("this file requiers the mol2 libary writen by trent balius and sudipto mukherjee\n")
print ("syntax:   mol2_break_macrocycle.py      \'atom1Name,atom1Num\'     \'atom2Name,atom2Num\'     input_file     output_file")
print("(example usage: python3 mol2_break_macrocycle.py 'C25,25' 'C26,26' idea1/break_cycle/idea1_0_output.mol2 idea1_break_v1.mol2)\n\n")

#some initializations
atom1    = sys.argv[1]
new_type = "Du"
atom2    = sys.argv[2]
infile   = sys.argv[3]
outfile  = sys.argv[4]

atom1name = atom1.split(',')[0]
atom1num  = int(atom1.split(',')[1])

atom2name = atom2.split(',')[0]
atom2num  = int(atom2.split(',')[1])

print("you inputed the following information:\n")
print("atom1name = %s\natom1num = %d\natom2name = %s\natom2num = %d\nnew type = %s\ninfile = %s\noutfile = %s\n"%(atom1name,atom1num,atom2name,atom2num,new_type,infile,outfile))
print("\nlet's go ahead and break this cycle!")
print("------------------------------------")


mol_list = mol2.read_Mol2_file(infile)
print ("number of molecules in input file: %d\n"%len(mol_list))

count = 0
for mol in mol_list:
    print("number of atoms at start: %d"%len(mol.atom_list))
    print("number of bonds at start: %d"%len(mol.bond_list))
    print("------------------------------\n")

    if atom1name!=mol.atom_list[atom1num-1].name or mol.atom_list[atom1num-1].num != atom1num or atom2name!=mol.atom_list[atom2num-1].name or mol.atom_list[atom2num-1].num!=atom2num:
        print("Error...cannot find selected atom in atom list")
        exit()

    # calculate current formal charge on molecule
    dis_Q = 0.0
    for a in mol.atom_list: 
        dis_Q = dis_Q + a.Q
        
    atoms_to_be_removed = []
    atoms_to_be_removed.append([atom1num,atom2num])


    # So we don't need to  delete hydrogens anymore! since we're making the two heavy atoms the two dummies, there's no splitting of the atom or anythibg
    newbondlist =[] 
    count_H = 0  # hydrogen
    count_HA = 0 # heavy atom
    for b in mol.bond_list:
        bc = copy.copy(b) 
        if b.a1_num == atom1num: 
           #if its a hydrogen, increment the count of hydrogens but keep that new bond
           if mol.atom_list[b.a2_num-1].type == "H": 
              #print("removed %s %d %d"%("bond",b.a1_num,b.a2_num))
              #atoms_to_be_removed.append(b.a2_num)
              count_H = count_H + 1
              newbondlist.append(bc)
           elif b.a2_num == atom2num:
              print("removing bond between a1 = %d and a2 = %d"%(b.a1_num,b.a2_num))
           else: 
            #  bc.a1_num = bc.a1_num + count_HA # if fist add 0, if second add 1.  so the first is connected to original, and the next is connected to the copy. 
              newbondlist.append(bc)
              count_HA = count_HA + 1 
        elif b.a2_num == atom1num: 
           if mol.atom_list[b.a1_num-1].type == "H": 
              #print("removed %s %d %d"%("bond",b.a1_num,b.a2_num))
              #atoms_to_be_removed.append(b.a1_num)
              count_H = count_H + 1
              newbondlist.append(bc)
           elif b.a2_num == atom2num:
              print("removing bond between a1 = %s, %d and a2 = %s, %d"%(b.a1_name,b.a1_num,b.a2_name,b.a2_num))
           else: 
             # bc.a2_num = bc.a2_num + count_HA # if fist add 0, if second add 1.  so the first is connected to original, and the next is connected to the copy. 
              newbondlist.append(bc)
              count_HA = count_HA + 1
        else: 
           newbondlist.append(bc)
    mol.bond_list = newbondlist
    print("\nthere are %d hydrgens and %d heavy atoms connected to atom 1\n"%(count_H,count_HA))
    print("atom 1 in atom_list: %s, index: %d\natom 2 in atom_list: %s, index: %d"%((mol.atom_list[atom1num-1].name),(mol.atom_list[atom1num-1].num),(mol.atom_list[atom2num-1].name),(mol.atom_list[atom2num-1].num)))
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0
    z1 = 0.0
    z2 = 0.0
    # change atom type and save the atom coordinates
    for a in mol.atom_list:
        if a.num == atom1num:
           a.type = new_type
           x1 = a.X
           y1 = a.Y
           z1 = a.Z
           print("\natom1 %s coords:\nx = %f\ny = %f\nz = %f\n"%(a.name,x1,y1,z1))
        elif a.num == atom2num:
           a.type = new_type
           x2 = a.X
           y2 = a.Y
           z2 = a.Z
           print("atom2 %s coords:\nx = %f\ny = %f\nz = %f\n"%(a.name,x2,y2,z2))
        else:
          continue
           #print("atom num: %d"%a.num)    
    
    #calculate bond length between dummies
    bond_distance = 0.0
    bond_distance = math.sqrt(((x1-x2)**2) + ((y1 - y2)**2) + ((z1 - z2)**2))
    print ("\ncalculating deleted bond distance = %f\n"%bond_distance)
    
    # if dummy set charge to  charge to zero
    # count number of non-dummy atoms for charge redistribution 
    count_atoms = 0
    for a in mol.atom_list:
        if a.type == 'Du':
           a.Q = 0.0 # set dummy charge to zero 
        else: 
           count_atoms = count_atoms + 1
    print ("number of atoms at end = %d\nnon-dummy atom count = %d"%(len(mol.atom_list),count_atoms))

    # sum up partial charges
    tot_q = 0.0
    for a in mol.atom_list:
        tot_q = tot_q + a.Q

    print("tot_q = %f"%tot_q)
    diff_Q = (dis_Q-tot_q)/count_atoms

    #redistribute charges to non-dummy atoms
    print("distribute diff of %f to each of the non-dummy atoms.\n"%(diff_Q))
    for a in mol.atom_list:
        if a.type != 'Du':
           a.Q = a.Q - diff_Q

    print("------------------------------")
    print ("non-dummy atom count = %d\n\nnumber of atoms at end = %d"%(count_atoms,len(mol.atom_list)))
    print("number of bonds at end = %d"%len(mol.bond_list)) 
    print("------------------------------\n")
    print("all done! if these counts look ok then you're good to go!\nhappy docking ^_^\n\n")
    
    if count == 0:
       mol2.write_mol2(mol,outfile)
    else:
       mol2.append_mol2(mol,outfile)
    count=count+1

