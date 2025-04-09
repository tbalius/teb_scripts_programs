
# Modified by Andree K Kolliegbo summer 2024. 

import mol2_python3 as mol2
import sys
import copy
import math

print ("this file requiers the mol2 libary writen by trent balius and sudipto mukherjee\n")
print ("syntax:   mol2_break_macrocycle.py      \'atom1Name,atom1Num\'     \'atom2Name,atom2Num\'     input_file solv_file output_file")
print("(example usage: python3 mol2_break_macrocycle.py 'C25,25' 'C26,26' idea1/break_cycle/idea1_0_output.mol2 idea1/break_cycle/idea1_0_output.solv idea1_break_v1.mol2)\n\n")

#some initializations
atom1    = sys.argv[1]
new_type = "Du"
atom2    = sys.argv[2]
infile   = sys.argv[3]
solvfile = sys.argv[4]
outfile  = sys.argv[5]

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

    ### Write out solvation information ### added by Trent Balius 2025/03/05 

    fileh = open(solvfile,'r')
    print(atoms_to_be_removed)
    count = 0
    text = ''
    lines = []
    for line in fileh:
         #print (count, atoms_to_be_removed[0])
         if count in atoms_to_be_removed[0]: # atoms_to_be_removed[0] is the list of atom number, numbering starting at 1 not 0
            print ("Du line (%d):                %s"%(count,line.strip()))
            temp = "%8.4f %7.2f %6.2f %7.2f %7.2f\n"%(0.0,0.0,0.0,0.0,0.0)
            lines.append(temp)
         else:
            #text = text+line
            lines.append(line)
         count = count+1

    fileh.close()

    print (len(lines))

    count = 0
    c1 = 0.0
    c2 = 0.0
    c3 = 0.0
    c4 = 0.0
    c5 = 0.0

    for line in lines:
        #print(line)
        #exit()
        if (count != 0):
           text = text+line
           #text = text+str(count)+" "+line
           splitline = line.split()
           #print(count, splitline)
           c1 = c1+float(splitline[0])
           c2 = c2+float(splitline[1])
           c3 = c3+float(splitline[2])
           c4 = c4+float(splitline[3])
           c5 = c5+float(splitline[4])
        count = count+1
    #exit()
    #print(lines[0])
    text1 = "%-10s %3d %3.1f %8.2f %8.2f %8.2f %8.2f\n"%("name",count-1, c1,c2,c3,c4,c5)
    #print (text1)
    text = text1 + text


    if count == 0:
       mol2.write_mol2(mol,outfile)
    else:
       mol2.append_mol2(mol,outfile)
    count=count+1

    fileho = open(outfile,'a') # append
    fileho.write("@<TRIPOS>SOLVATION\n")
    fileho.write(text)
    fileho.close()
    
 
    print("------------------------------")
    print ("non-dummy atom count = %d\n\nnumber of atoms at end = %d"%(count_atoms,len(mol.atom_list)))
    print("number of bonds at end = %d"%len(mol.bond_list)) 
    print("------------------------------\n")
    print("all done! if these counts look ok then you're good to go!\nhappy docking ^_^\n\n")
    
