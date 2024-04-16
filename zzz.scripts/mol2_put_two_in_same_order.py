
import mol2_python3 as mol2
import sys
import numpy, math
from scipy.optimize import linear_sum_assignment
import copy

#  This is written by Trent E. Balius 

# started on 2023.11.08 at FNLCR


#def bond_dist(atom1,atom2,mol):

# currently only look at the atom enviorment one atom away.  
# we could look two atoms away as well
def calc_atom_enviorment(atom,mol):
    num = atom.num 
    
    con = [] # store the atom numbers
    env = {} # store the types of atoms conected to atom
    # consider adding in bondtypes
    for bond in mol.bond_list:
        if bond.a1_num == num:
           #print ("atom1")
           #print ( "%d->%d" % (bond.a1_num,bond.a2_num))
           #print ( "%d->%d" % (mol.atom_list[bond.a1_num-1].num, mol.atom_list[bond.a2_num-1].num))
           #print ( "%s->%s" % (mol.atom_list[bond.a1_num-1].name, mol.atom_list[bond.a2_num-1].name))

           con.append(bond.a2_num)
           print (bond.a2_num)
           atype = mol.atom_list[bond.a2_num-1].type
           if atype in env:
              env[atype] = env[atype] + 1
           else:
              env[atype] = 1
        if bond.a2_num == num:
           #print ("atom2")
           #print ( "%d->%d" % (bond.a1_num,bond.a2_num))
           #print ( "%d->%d" % (mol.atom_list[bond.a1_num-1].num, mol.atom_list[bond.a2_num-1].num))
           #print ( "%s->%s" % (mol.atom_list[bond.a1_num-1].name, mol.atom_list[bond.a2_num-1].name))

           con.append(bond.a1_num)
           atype = mol.atom_list[bond.a1_num-1].type
           if atype in env:
              env[atype] = env[atype] + 1
           else:
              env[atype] = 1
    #return con, env 
    #print ("debug env")
    #for key in env.keys():
    #    print (key, env[key])
    return env, con 

#def nextlayr(atom,mol,connected):
#    for atom_num in connected:
    

def atype_to_ele(atype):
    ele = atype.split('.')[0]
    #print(atype,ele)
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
           #return 1.0
           return 10.0
    #return 1.0
    

def compare_atom_env(atype1,env1,atype2,env2):
    val = 0.0
    val = val + compare_types(atype1,atype2)
    print ( "compare %s %s "% (atype1,atype2))
    print ("enviorment: ") 
    # look at the things directly connected
    weight = 2.0
    atypes = {}

    # if the number of atoms bonded are not the same
    # add large penalty.
    if len(env1) != len(env2): 
       val = val + 10.0

    # get keys from both env
    for key in env1: 
        atypes[key] = 0
    for key in env2: 
        atypes[key] = 0
    # now loop over keys (atom types) from both envs. 

    # local env to make sure we are not modifing the original
    temp_env1 = {}
    temp_env2 = {}
    
    for key in atypes: 
        if not key in env1: 
            temp_env1[key] = 0
        else:
            temp_env1[key] = env1[key]
        if not key in env2:
            temp_env2[key] = 0
        else:
            temp_env2[key] = env2[key]
        print (key, temp_env1[key], temp_env2[key])
        val = val + weight * math.fabs(temp_env1[key] - temp_env2[key])  #  I want to penalize if the atoms are not connect to the same atom_types
    return val
    

def calc_atom_enviorment_matrix_assignment(molA,molB,submap):

   if len(molA.atom_list) != len(molB.atom_list): 
       print ("molecules must have the same number of atoms")
       exit()

   cost = numpy.zeros([len(molA.atom_list),len(molB.atom_list)])
   for atomI in molA.atom_list:
       envI,con =calc_atom_enviorment(atomI,molA)
       print(envI)
       numI = len(envI)
       for atomJ in molB.atom_list:
           envJ,con = calc_atom_enviorment(atomJ,molB)
           print(envJ)
           numJ = len(envJ)
           #costval = numI - numJ
           costval = compare_atom_env(atomI.type,envI,atomJ.type,envJ)
           cost[atomI.num-1,atomJ.num-1] = costval

   # for user spesified map force match by modifing cost matrix.
   if (len(submap)>0):
       for ele in submap:
           cost[ele[0]-1,ele[1]-1] = 0.0
           for i in range(len(molA.atom_list)):
                if i != (ele[0]-1): 
                   cost[i,ele[1]-1] = 100.0
           for j in range(len(molB.atom_list)):
                if j != (ele[1]-1): 
                   cost[ele[0]-1,j] = 100.0

   costtxt = ''
   #print (cost)
   for i in range(len(molA.atom_list)): 
       for j in range(len(molA.atom_list)): 
           costtxt = costtxt+"\t"+str(cost[i,j])
       costtxt = costtxt+'\n'
   print(costtxt)
       
           
   row_ind, col_ind = linear_sum_assignment(cost)
   #print(row_ind)
   #print(col_ind)
   #print(len(molA.atom_list))
   #print(len(molB.atom_list))
   #print(len(row_ind))
   #print(len(col_ind))
   sumcost = 0.0
   for i in range(len(row_ind)):
       ii = row_ind[i]
       ij = col_ind[i]
       print ("%d -> %d, cost = %f"%(ii,ij,cost[ii,ij]))
       sumcost = sumcost + cost[ii,ij]
   print ("sum cost = %f"%sumcost)
   return col_ind
   #return row_ind

def main ():
    print ("this file requiers the mol2 libary writen by trent balius and sudipto mukherjee")
    
    print ("syntex: mol2_get_frist_mol.py input_file ref_file output_file [user-spesified submap (1:2,3:4,...,10:10 or None)]")
    
    if ( len(sys.argv) != 4 and len(sys.argv) != 5):
       print("syntex error ...")
       exit(0)
    
    #flag_submap = False
    infile = sys.argv[1]
    reffile = sys.argv[2]
    outfile = sys.argv[3]
    mol_list1 = mol2.read_Mol2_file(infile)
    mol_list2 = mol2.read_Mol2_file(reffile)

    u_submap = [];
    if (len(sys.argv) ==5):
      #flag_submap = True
      submap = sys.argv[4]
      for ele in submap.split(','):
          se = ele.split(':')
          e1 = int(se[0])
          e2 = int(se[1])
          u_submap.append([e1,e2])
          
    
    
    print("mol = %s"%infile)
    print("ref = %s"%reffile)
    #print (len(mol_list1))
    #print (len(mol_list2))
    #mol = mol2.remove_hydrogens( mol_list[0] )
    
    #mol = mol_list1[0]
    #ref = mol_list2[0]
    mol = mol2.remove_hydrogens(mol_list1[0],True)
    ref = mol2.remove_hydrogens(mol_list2[0],True)
    
    mol2.write_mol2(ref,outfile+'_ref.mol2')
    mol2.write_mol2(mol,outfile+'_mol.mol2')
    
    #mapping = calc_atom_enviorment_matrix_assignment(mol,ref)
    mapping = calc_atom_enviorment_matrix_assignment(ref,mol,u_submap)
    
    # reverse map 
    re_mapping = []
    for i in mapping:
        re_mapping.append(0)
    for i in range(len(mapping)):
        re_mapping[mapping[i]] = i
        
    
    new_atom_list = []
    
    for i in range(len(mapping)):
        #new_atom_list.append(mol.atom_list[mapping[i]])
        new_atom = mol.atom_list[mapping[i]]
        new_atom.num = i+1
        new_atom_list.append(new_atom)
    
    new_bond_list = []
    
    for i in range(len(mol.bond_list)):
       #print( mol.bond_list[i].a1_num, mapping[mol.bond_list[i].a1_num-1]+1);
       #print( mol.bond_list[i].a2_num, mapping[mol.bond_list[i].a2_num-1]+1);
       #new_bond_list.append(mol2.bond(mapping[mol.bond_list[i].a1_num-1]+1,mapping[mol.bond_list[i].a2_num-1]+1,mol.bond_list[i].num,mol.bond_list[i].type))
       #new_bond = mol2.bond(mapping[mol.bond_list[i].a1_num-1]+1,mapping[mol.bond_list[i].a2_num-1]+1,mol.bond_list[i].num,mol.bond_list[i].type)
       #new_bond_list.append(new_bond)
       #print("re_mapp")
       print( mol.bond_list[i].a1_num, re_mapping[mol.bond_list[i].a1_num-1]+1);
       print( mol.bond_list[i].a2_num, re_mapping[mol.bond_list[i].a2_num-1]+1);
       new_bond = mol2.bond(re_mapping[mol.bond_list[i].a1_num-1]+1,re_mapping[mol.bond_list[i].a2_num-1]+1,mol.bond_list[i].num,mol.bond_list[i].type)
       new_bond_list.append(new_bond)
    
    
    #mol2.write_mol2(mol,outfile)
    molnew = mol2.Mol(mol.header,mol.name,new_atom_list,new_bond_list,mol.residue_list) 
    
    mol2.write_mol2(molnew,outfile+'_newmol.mol2')
main() 
