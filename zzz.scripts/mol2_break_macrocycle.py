
#import mol2
import mol2_python3 as mol2
import sys
import copy
#def in_atomnum_list(atomnum_list,atom_num):
#    for atom_num_ele in atomnum_list: 
#        if atom


print ("this file requiers the mol2 libary writen by trent balius and sudipto mukherjee")

print ("syntex: mol2_break_macrocycle.py atom1name input_file output_file")

atom1    = sys.argv[1]
new_type = "Du"
infile   = sys.argv[2]
outfile  = sys.argv[3]

atom1name = atom1.split(',')[0]
atom1num  = int(atom1.split(',')[1])

print("atom1name=%s\natom1num=%d\nnew type = %s\ninfile=%s\noutfile=%s\n"%(atom1name,atom1num,new_type,infile,outfile))

mol_list = mol2.read_Mol2_file(infile)
print (len(mol_list))

count = 0
for mol in mol_list:
    print("number of atoms at start: %d"%len(mol.atom_list))
    print("number of bonds at start: %d"%len(mol.bond_list))
    print(mol.atom_list[atom1num-1].name)
    print(mol.atom_list[atom1num-1].num)
    if atom1name!=mol.atom_list[atom1num-1].name or mol.atom_list[atom1num-1].num != atom1num: 
        print("Error...")
        exit()

    # calculate current formal charge on molecule
    dis_Q = 0.0
    for a in mol.atom_list: 
        dis_Q = dis_Q + a.Q
        
    atoms_to_be_removed = []

    # we need to renumber the atoms
    for a in mol.atom_list:
        if a.num > atom1num:
           a.num = a.num + 1

    # we need to renumber the atoms in bonds 
    for b in mol.bond_list: 
        #print (b.a1_num, b.a2_num)
        #if b.a1_num > atom1num: 
        if b.a1_num > atom1num :   
           b.a1_num = b.a1_num + 1
        if b.a2_num > atom1num :
           b.a2_num = b.a2_num + 1

    # add dummy.  
    newatomlist =[] 
    for a in mol.atom_list:
       if a.num == atom1num:
           # add atom twice
           atemp = a
           atemp.type = new_type
           newatomlist.append(atemp)
           atemp = copy.copy(a)
           atemp.type = new_type
           atemp.name = atemp.name+"'"
           atemp.num  = atemp.num+1
           newatomlist.append(atemp)
       else:
           newatomlist.append(a)
    mol.atom_list = newatomlist



    # Delete any hydrogens connected to the slected atom.
    # check that the atom is only connected to only two other heavy atoms
    # if not return an error
    newbondlist =[] 
    count_H = 0  # hydrogen
    count_HA = 0 # heavy atom
    for b in mol.bond_list:
        bc = copy.copy(b) 
        if b.a1_num == atom1num: 
           #print ("atom num compare", atom1num,mol.atom_list[atom1num-1].num)
           if mol.atom_list[b.a2_num-1].type == "H": 
              #print(b.a2_num-1, mol.atom_list[b.a2_num-1].num, mol.atom_list[b.a2_num-1].type)
              print("removed %s %d %d"%("bond",b.a1_num,b.a2_num))
              atoms_to_be_removed.append(b.a2_num)
              count_H = count_H + 1
           else: 
              bc.a1_num = bc.a1_num + count_HA # if frist add 0, if second add 1.  so the first is connected to original, and the next is connected to the copy. 
              newbondlist.append(bc)
              count_HA = count_HA + 1 
        elif b.a2_num == atom1num: 
           if mol.atom_list[b.a1_num-1].type == "H": 
              #print(b.a1_num-1, mol.atom_list[b.a1_num-1].num, mol.atom_list[b.a1_num-1].type)
              print("removed %s %d %d"%("bond",b.a1_num,b.a2_num))
              atoms_to_be_removed.append(b.a1_num)
              count_H = count_H + 1
           else: 
              bc.a2_num = bc.a2_num + count_HA # if frist add 0, if second add 1.  so the first is connected to original, and the next is connected to the copy. 
              newbondlist.append(bc)
              count_HA = count_HA + 1
        else: 
           newbondlist.append(bc)
    mol.bond_list = newbondlist
    print("there are %d hydrgens and %d heavy atoms connected to the chosen atom"%(count_H,count_HA))
    if count_HA != 2: 
       print("Error, heavy atoms connected to the chosen atom must be 2")
       exit(0)

    #print ("atoms to be removed: ",atoms_to_be_removed)
          
    # remove atoms
    newatomlist =[] 
    for a in mol.atom_list:
       # if a.num != atom1num: 
       #    newatomlist.append(a)
       # else: 
       if not a.num in atoms_to_be_removed: 
           newatomlist.append(a)
       else: 
           print("removed %s %s %d"%(a.type,a.name,a.num))
           
    mol.atom_list = newatomlist
    print("number of atoms (removed H added dulicate): %d"%len(mol.atom_list))
    print("number of bonds (removed H added dulicate): %d"%len(mol.bond_list))

   #count = 0

   #for b in mol.bond_list: 
   #    if b.a1_num == atom1num: 
   #       b.a1_num = b.a1_num + count # count will be 0 (start) or one (after incrament)
   #       count = count +1
   #    if b.a2_num == atom1num: 
   #       b.a2_num = b.a2_num + count
   #       count = count +1
   #    if count == 2: 
   #       break

    

    # change atom type
    for a in mol.atom_list:
        if a.num == atom1num:
           a.type = new_type
    # if dummy set charge to  charge to zero
    # count number of non-dummy atoms for charge distribution. 
    count_atoms = 0
    for a in mol.atom_list:
        if a.type == 'Du':
           a.Q = 0.0 # set dummy charge to zero 
        else: 
           count_atoms = count_atoms + 1
    #print (count_atoms)

    # sum up partail charges
    tot_q = 0.0
    for a in mol.atom_list:
        tot_q = tot_q + a.Q

    print("tot_q = %f"%tot_q)
    diff_Q = (dis_Q-tot_q)/count_atoms
    #print("distribute diff of %f to all non-dummy atoms."%(dis_Q-tot_q))
    print("distribute diff of %f to each non-dummy atoms."%(diff_Q))

    for a in mol.atom_list:
        if a.type != 'Du':
           a.Q = a.Q - diff_Q

    new_bond_list = []
    for b in mol.bond_list: 
         #new = mol.atom_list[b.a1_num-1].num 
         #print(b.a1_num,new)
         #b.a1_num = new
         #new = mol.atom_list[b.a2_num-1].num
         #print(b.a2_num,new)
         #b.a2_num = new
         bc = copy.copy(b)
         count = 0
         for i,a in enumerate(mol.atom_list): 
             if (a.num == b.a1_num):
                #print(b.a1_num,i+1)
                bc.a1_num = i+1
                count = count + 1
             if (a.num == b.a2_num):
                #print(b.a2_num,i+1)
                bc.a2_num = i+1
                count = count + 1
         if count != 2: 
             print("bond has only %d atom, bond removed"%count)
             #print(bc.a1_num, bc.a2_num)
             #exit(0)
         else: 
             #print("bond ", bc.a1_num, bc.a2_num)
             new_bond_list.append(bc)

    mol.bond_list = new_bond_list

    #print(len(mol.atom_list))
    #for b in mol.bond_list:
    #    print (b.a1_num,b.a2_num)
    for i,a in enumerate(mol.atom_list):
        #print(a.num, "change to", i)
        a.num = i+1
        

    #    if b.a1_num > atom2num: 
    #       b.a1_num = b.a1_num -1
    #    if b.a2_num > atom2num: 
    #       b.a2_num = b.a2_num -1
    if count == 0:
       mol2.write_mol2(mol,outfile)
    else:
       mol2.append_mol2(mol,outfile)
    count=count+1

