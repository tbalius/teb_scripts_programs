
import mol2
import sys,copy



def maping_by_cord(mol_1, mol_2): 
   dictionary_cord = {}
   for i,a in enumerate(mol_1.atom_list):
       entry = '%6.3f_%6.3f_%6.3f'%(a.X,a.Y,a.Z)
       print entry
       dictionary_cord[entry] = [i+1]
   
   for i,a in enumerate(mol_2.atom_list):
       entry = '%6.3f_%6.3f_%6.3f'%(a.X,a.Y,a.Z)
       if not entry in dictionary_cord:
           print "error."
       dictionary_cord[entry].append(i+1)
   
   maping = []
   for key in dictionary_cord.keys():
       maping.append(0)
   
   for key in dictionary_cord.keys(): 
        if len(dictionary_cord[key]) != 2:
           print "UhOh. something is wrong" 
        print str(dictionary_cord[key][0]) + "-->"+str(dictionary_cord[key][1])
        #maping[dictionary_cord[key][0]-1] = (dictionary_cord[key][1]-1)
        maping[dictionary_cord[key][1]-1] = (dictionary_cord[key][0]-1)

   return maping   

def maping_by_atom_name(mol_1, mol_2):
   dictionary_cord = {}
   for i,a in enumerate(mol_1.atom_list):
       entry = a.name
       print entry
       dictionary_cord[entry] = [i+1]

   for i,a in enumerate(mol_2.atom_list):
       entry = a.name
       if not entry in dictionary_cord:
           print "error."
       dictionary_cord[entry].append(i+1)

   maping = []
   for key in dictionary_cord.keys():
       maping.append(0)

   for key in dictionary_cord.keys():
        if len(dictionary_cord[key]) != 2:
           print "UhOh. something is wrong"
        print str(dictionary_cord[key][0]) + "-->"+str(dictionary_cord[key][1])
        #maping[dictionary_cord[key][0]-1] = (dictionary_cord[key][1]-1)
        maping[dictionary_cord[key][1]-1] = (dictionary_cord[key][0]-1)

   return maping


print "This file requiers the mol2 libary writen by trent balius and sudipto mukherjee"


print "syntex: mol2_shuffle.py input_file1 input_file2 input_file3 output_file"
print "this file takes in 3 mol2 input files 2 of the files are the same but a different order. "
print "The 3 input is a file that you want to suffle for the order of 1 to 2"
print "(1) origenal order."
print "(2) the new order."
print "(3) mol2 to file to change the order (can be multi mol2)"
print "(4) name to which to write newly reordered mol2."

infile1 = sys.argv[1]
infile2 = sys.argv[2]
infile3 = sys.argv[3]
outfile = sys.argv[4]
mol_1 = mol2.read_Mol2_file(infile1)[0] # ori order
mol_2 = mol2.read_Mol2_file(infile2)[0] # new order

mol_3list = mol2.read_Mol2_file_head(infile3)

#maping = maping_by_cord(mol_1, mol_2)

for j,mol_3 in enumerate(mol_3list):
   print "molecule %d"%(j)
   #mol_3_new = copy.deepcopy(mol_3) 
   maping = maping_by_atom_name(mol_3,mol_2)
   atomlist = []
   for i,move in enumerate(maping):
       #print i,move,maping[i] 
       atom = mol_3.atom_list[move]
       atom.num = i+1
       atomlist.append(atom)
       
   #mol_3_new.atom_list = atomlist
   #bondlist     = copy.deepcopy(mol_2.bond_list)
   bondlist     = mol_2.bond_list
   header       = mol_3.header
   name         = mol_3.name
   residuelist = mol_3.residue_list
   mol_3_new = mol2.Mol(header,name,atomlist,bondlist,residuelist)
   print mol_3.header, mol_3_new.header 
#  for bond in mol_3_new.bond_list: 
#      print bond.a1_num, bond.a2_num, bond.num, bond.type
#      print atomlist[bond.a1_num-1].num, atomlist[bond.a2_num-1].num, bond.num, bond.type
   if j == 0: 
      mol2.write_mol2(mol_3_new,outfile) 
   else: 
      mol2.append_mol2(mol_3_new,outfile)



#print len(mol_list)
#mol = mol2.remove_hydrogens( mol_list[0] )
#mol2.write_mol2(mol,outfile)

