
import mol2_python3 as mol2
import sys
import numpy, math
from scipy.optimize import linear_sum_assignment

#  This is written by Trent E. Balius 

# started on 2023.11.08 at FNLCR


# we can calculate the distance from a ref.  This should help us. 
# the ref should be the same atom in both files
def bond_dist(atom1,atom2,mol):
    # look for banching points (forks)
    # remember points we already vistited. 
    # if we reach the end of the molecule or a visited point go back to the most recent fork (forget the visited nodes after the branch) remember what we already explored.
    # (this is kind of like exploring a cave).   
    # we needed to find all paths between atom1 and atom2 not just one.  we then uses the minimum distance.  


def calc_atom_enviorment(atom,mol):
    num = atom.num 
    
    con = [] # store the atom numbers
    env = {} # store the types of atoms conected to atom
    # consider adding in bondtypes
    for bond in mol.bond_list:
        if bond.a1_num == num:
           print ("atom1")
           print ( "%d->%d" % (bond.a1_num,bond.a2_num))
           print ( "%d->%d" % (mol.atom_list[bond.a1_num-1].num, mol.atom_list[bond.a2_num-1].num))
           print ( "%s->%s" % (mol.atom_list[bond.a1_num-1].name, mol.atom_list[bond.a2_num-1].name))

           con.append(bond.a2_num)
           atype = mol.atom_list[bond.a2_num-1].type
           if atype in env:
              env[atype] = env[atype] + 1
           else:
              env[atype] = 1
        if bond.a2_num == num:
           print ("atom2")
           print ( "%d->%d" % (bond.a1_num,bond.a2_num))
           print ( "%d->%d" % (mol.atom_list[bond.a1_num-1].num, mol.atom_list[bond.a2_num-1].num))
           print ( "%s->%s" % (mol.atom_list[bond.a1_num-1].name, mol.atom_list[bond.a2_num-1].name))

           con.append(bond.a1_num)
           atype = mol.atom_list[bond.a1_num-1].type
           if atype in env:
              env[atype] = env[atype] + 1
           else:
              env[atype] = 1
    #return con, env 
    return env 

def atype_to_ele(atype):
    ele = atype.split('.')[0]
    print(atype,ele)
    #exit()
    return ele

def compare_types(atype1,atype2):
    if (atype1 == atype2): 
        return 0.0
    else: 
        ele1 = atype_to_ele(atype1)
        ele2 = atype_to_ele(atype2)
        if (ele1 == ele2): 
           return 0.5
        else: 
           return 1.0
    #return 1.0
    

def compare_atom_env(atype1,env1,atype2,env2):
    val = 0.0
    val = val + compare_types(atype1,atype2)
    # look at the things directly connected
    atypes = {}
    # get keys from both env
    for key in env1: 
        atypes[key] = 0
    for key in env2: 
        atypes[key] = 0
    # now loop over keys (atom types) from both envs. 
    for key in atypes: 
        if not key in env1: 
            env1[key] = 0
        if not key in env2:
            env2[key] = 0
        print (env1[key], env2[key])
        val = val + math.fabs(env1[key] - env2[key])  #  I want to penalize if the atoms are not connect to the same atom_types
    return val
    

def calc_atom_enviorment_matrix_assignment(molA,molB):

   if len(molA.atom_list) != len(molB.atom_list): 
       print ("molecules must have the same number of atoms")
       exit()

   cost = numpy.zeros([len(molA.atom_list),len(molB.atom_list)])
   for atomI in molA.atom_list:
       envI =calc_atom_enviorment(atomI,molA)
       numI = len(envI)
       for atomJ in molB.atom_list:
           envJ = calc_atom_enviorment(atomJ,molB)
           numJ = len(envJ)
           #costval = numI - numJ
           costval = compare_atom_env(atomI.type,envI,atomJ.type,envJ)
           cost[atomI.num-1,atomJ.num-1] = costval
           
   row_ind, col_ind = linear_sum_assignment(cost)
   print(row_ind)
   print(col_ind)
   print(len(molA.atom_list))
   print(len(molB.atom_list))
   print(len(row_ind))
   print(len(col_ind))
   return col_ind

print ("this file requiers the mol2 libary writen by trent balius and sudipto mukherjee")

print ("syntex: mol2_get_frist_mol.py input_file ref_file output_file")

infile = sys.argv[1]
reffile = sys.argv[2]
outfile = sys.argv[3]
mol_list1 = mol2.read_Mol2_file(infile)
mol_list2 = mol2.read_Mol2_file(reffile)
print (len(mol_list1))
print (len(mol_list2))
#mol = mol2.remove_hydrogens( mol_list[0] )

mol = mol_list1[0]
ref = mol_list2[0]

calc_atom_enviorment_matrix_assignment(mol,ref)

mol2.write_mol2(mol,outfile)

