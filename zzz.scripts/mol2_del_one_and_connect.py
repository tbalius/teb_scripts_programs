
#import mol2
import mol2_python3 as mol2
import sys

print ("this file requiers the mol2 libary writen by trent balius and sudipto mukherjee")

print ("syntex: mol2_del_one_and_connect.py atom1name,atom1num  atom2name,atom2num new_type formal_charge input_file output_file")

atom1    = sys.argv[1]
atom2    = sys.argv[2]
new_type = sys.argv[3]
dis_Q    = float(sys.argv[4])
infile   = sys.argv[5]
outfile  = sys.argv[6]

atom1name = atom1.split(',')[0]
atom1num  = int(atom1.split(',')[1])

atom2name = atom2.split(',')[0]
atom2num  = int(atom2.split(',')[1])

print("atom1name=%s\natom1num=%d\natom2name=%s\natom2num=%d\nnew type = %s\ndisiered charge=%f\ninfile=%s\noutfile=%s\n"%(atom1name,atom1num,atom2name,atom2num,new_type,dis_Q,infile,outfile))

mol_list = mol2.read_Mol2_file(infile)
print (len(mol_list))

count = 0
for mol in mol_list:
    print(mol.atom_list[atom1num-1].name)
    print(mol.atom_list[atom1num-1].num)
    if atom1name!=mol.atom_list[atom1num-1].name or mol.atom_list[atom1num-1].num != atom1num: 
        print("Error...")
        exit()
    print(mol.atom_list[atom2num-1].name)
    print(mol.atom_list[atom2num-1].num)
    if atom2name!=mol.atom_list[atom2num-1].name or mol.atom_list[atom2num-1].num != atom2num: 
        print("Error...")
        exit()
    newatomlist =[] 

    for a in mol.atom_list:
        if a.num != atom2num: 
           newatomlist.append(a)
           
    mol.atom_list = newatomlist

    for b in mol.bond_list: 
        if b.a1_num == atom2num: 
           b.a1_num = atom1num
        if b.a2_num == atom2num: 
           b.a2_num = atom1num
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

    # renumber since we remove an atom. 
    for a in mol.atom_list:
        if a.num > atom2num: 
           a.num = a.num - 1

    for b in mol.bond_list: 
        if b.a1_num > atom2num: 
           b.a1_num = b.a1_num -1
        if b.a2_num > atom2num: 
           b.a2_num = b.a2_num -1
    if count == 0:
       mol2.write_mol2(mol,outfile)
    else:
       mol2.append_mol2(mol,outfile)
    count=count+1

