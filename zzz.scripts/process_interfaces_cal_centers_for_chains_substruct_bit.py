
#################################################################################################################
## Writen by Trent Balius at FNLCR in 2020 (took from other scripts)
#################################################################################################################
import sys,os
import pdb_lib as pdb

#DOCKBASE = "/nfs/home/tbalius/zzz.github/DOCK"
# this script will process the crystalographic unitcell written out by chimera. 
 
def min_dist_between_two_sets_of_atoms(atom_list1,filename1,atom_list2,filename2,threshold,dict_ss):
        dict_res = {}
        flag_write = False
        print(filename1,filename2)
        filename_prefix = filename1.replace(' ','_')+'.'+filename2.replace(' ','_')
        fhi1 = open(filename_prefix+'_interface1.txt','w')
        fhi2 = open(filename_prefix+'_interface2.txt','w')
        fhi1b = open(filename_prefix+'_interface1.bits','w')
        fhi2b = open(filename_prefix+'_interface2.bits','w')
        interface1 = {}
        interface2 = {}
        interface1_resnum = {}
        interface2_resnum = {}
        if (filename1 == filename2): # all distances will be zeros. 
           print("%s is the center model. all distances are zeros"%filename1)
           return True
        for i in range(0,len(atom_list1)):
           if (atom_list1[i].resname == "HOH"): #skipe if water
               continue
           if not (atom_list1[i].resnum in interface1_resnum):
              interface1_resnum[atom_list1[i].resnum] = 0
           for j in range(0,len(atom_list2)):
               if (atom_list2[j].resname == "HOH"): # skipe if water
                  continue
               if not (atom_list2[j].resnum in interface2_resnum):
                   interface2_resnum[atom_list2[j].resnum] = 0
               dist2 = 0.0
               dist2 = dist2 + (atom_list1[i].X-atom_list2[j].X)**2
               dist2 = dist2 + (atom_list1[i].Y-atom_list2[j].Y)**2
               dist2 = dist2 + (atom_list1[i].Z-atom_list2[j].Z)**2
               if (dist2<threshold**2.0): 
                   flag_write = True
                   dist = (dist2)**(1.0/2.0)
                   #print ('file = %s, %s,%s,%s,%s::%f'%(filename2,atom_list2[j].atomname,atom_list2[j].atomnum,atom_list2[j].resname,atom_list2[j].resnum,dist))
                   res = filename2+"::"+atom_list1[i].resname+atom_list1[i].resnum+"->"+atom_list2[j].resname+atom_list2[j].resnum
                   interface1[atom_list1[i].resname+atom_list1[i].resnum] = int(atom_list1[i].resnum)
                   interface2[atom_list2[j].resname+atom_list2[j].resnum] = int(atom_list2[j].resnum)
                   #interface1_resnum[atom_list1[j].resnum] = 1
                   interface1_resnum[atom_list1[i].resnum] = 1
                   interface2_resnum[atom_list2[j].resnum] = 1
                   # populate dictionary with residue key and store the distance as the definition
                   if res in dict_res: # check if it is in the dictionary
                      if (dist < dict_res[res] ):
                         dict_res[res] = dist
                   else: 
                      dict_res[res] = dist
        print("######### %s --> %s"%(filename2,filename1))
        for key in dict_res: 
           print('%s::%f'%(key,dict_res[key])) 
        print("######## Interface1 (%s)"%filename1)

        sorted_dict_interface1 = sorted(interface1.items(), key = lambda kv:(kv[1], kv[0]))
        #print(sorted_dict_interface1)
        #for key in interface1:
        #    print key
        for key in sorted_dict_interface1:
            #print("%s"%key[0])
            #print(key[0],key[1])
            #print("%s %s"%(key[0],dict_ss[key[1]]))
            if key[1] in dict_ss:
               print("%s %s"%(key[0],dict_ss[key[1]]))
               fhi1.write("%s %s\n"%(key[0],dict_ss[key[1]]))
            else: 
               print("%s %s"%(key[0],"not in substructure def"))
               fhi1.write("%s %s\n"%(key[0],"not in substructure def"))
        print("######## Interface2 (%s)"%filename2)
        #for key in interface2:
        #    print key
        sorted_dict_interface2 = sorted(interface2.items(), key = lambda kv:(kv[1], kv[0]))
        for key in sorted_dict_interface2:
            #print("%s"%key[0])
            if key[1] in dict_ss:
               print("%s %s"%(key[0],dict_ss[key[1]]))
               fhi2.write("%s %s\n"%(key[0],dict_ss[key[1]]))
            else: 
               print("%s %s"%(key[0],"not in substructure def"))
               fhi2.write("%s %s\n"%(key[0],"not in substructure def"))

        #sorted_dict_interface1_resnum = sorted(interface1_resnum.items(), key = lambda kv:(kv[1], kv[0]))
        sorted_dict_interface1_resnum = sorted(interface1_resnum.keys())
        for key in sorted_dict_interface1_resnum:
               #print(key[0])
               #print("%s %s"%(key[0],interface1_resnum[key[0]]))
               #fhi1b.write("%s %s\n"%(key[0],interface1_resnum[key[0]]))
               print("%s %s"%(key,interface1_resnum[key]))
               fhi1b.write("%s %s\n"%(key,interface1_resnum[key]))

        #sorted_dict_interface2_resnum = sorted(interface2_resnum.items(), key = lambda kv:(kv[1], kv[0]))
        sorted_dict_interface2_resnum = sorted(interface2_resnum.keys())
        for key in sorted_dict_interface2_resnum:
               #print("%s %s"%(key[0],interface2_resnum[key[0]]))
               #fhi2b.write("%s %s\n"%(key[0],interface2_resnum[key[0]]))
               print("%s %s"%(key,interface2_resnum[key]))
               fhi2b.write("%s %s\n"%(key,interface2_resnum[key]))
            
        fhi1.close() 
        fhi2.close() 
        fhi1b.close() 
        fhi2b.close() 
            

        return flag_write

def centre_of_mass(atom_list):
        # Dictionary of atomic weights of elements
        #atom_mass = {'O':15.9994 ,'N':14.00674 ,'C':12.011 ,'F':18.9984032 ,'Cl':35.4527 ,'Br':79.904
        #,'I':126.90447 ,'H':1.00794 ,'B':10.811 ,'S':32.066 ,'P':30.973762 ,'Li':6.941 ,'Na':22.98968
        #,'Mg':24.3050 ,'Al':26.981539 ,'Si':28.0855 ,'K':39.0983 ,'Ca':40.078 ,'Cr':51.9961 ,'Mn':54.93805
        #,'Fe':55.847 ,'Co':58.93320 ,'Cu':63.546 ,'Zn':65.39 ,'Se':78.96 ,'Mo':95.94 ,'Sn':118.710 ,'LP':0.0 }

        #cmass = [0,0,0]
        centroid = [0,0,0]
        molecular_weight = 0
        count = 0
        for k in range(0,len(atom_list)):
                #cmass[0] += atom_list[k].X * atom_mass[element]
                #cmass[1] += atom_list[k].Y * atom_mass[element]
                #cmass[2] += atom_list[k].Z * atom_mass[element]
                centroid[0] += atom_list[k].X
                centroid[1] += atom_list[k].Y
                centroid[2] += atom_list[k].Z
                #molecular_weight += atom_mass[element]
                count = count+1
        #print "Molecular Weight =",molecular_weight
        #cmass[0] /= molecular_weight
        #cmass[1] /= molecular_weight
        #cmass[2] /= molecular_weight
        print ("number of atoms in reslist: " + str(count))
        centroid[0] /= count
        centroid[1] /= count
        centroid[2] /= count
        #print 'Centroid =',centroid
        #return cmass
        return centroid

def check_filename(fileinputpdb):
    splitname = fileinputpdb.split('\\')[-1].split('.') 
    if len(splitname) != 2:
        print ("error pdb file is weird. ")
        exit()
    return splitname[0] 

def readin_all_atoms_center_of_mass(fileinputpdb):
    pdblist = pdb.read_pdb(fileinputpdb)
    atoms =[]
    for pdbatoms in pdblist:
        for atom in pdbatoms:
           atoms.append(atom)
    return centre_of_mass(atoms)

def readin_all_atoms_return_chains(fileinputpdb):
    pdblist = pdb.read_pdb(fileinputpdb)
    if (len(pdblist) > 1):
        print("len(pdblist) = %d"%len(pdblist))
        print("pdblist is greater than 1. there is more than one model...")
    pdblist_combined = []
    for atoms in pdblist: 
        print(len(atoms))
        for atom in atoms:
            pdblist_combined.append(atom)
    #    exit()
    atoms_list =[]
    chains = []
    chains_dict = {}
    #current_chain = pdblist_combined[0].chainid
    for atom in pdblist_combined:
        #for atom in pdbatoms:
           if not (atom.chainid in chains_dict):
              chains_dict[atom.chainid] = []
           chains_dict[atom.chainid].append(atom)

    for key in chains_dict:        
       chains.append(chains_dict[key])
    return chains

def distance(centeri,centerj):
    #print ("In distance")
    dist2 = 0.0
    for k in range(0,3):
        dist2 = dist2 + (centeri[k]-centerj[k])**2
    #    print("%f-%f"%(centeri[k],centerj[k]))
    dist = dist2**(1.0/2.0)
    #print('dist = %f'%dist)
    return dist

def main():
    if len(sys.argv) != 3: # if no input
       print ("ERORR: there need to be 2 inputs: pdb substruct.txt")
       return

    fileinputpdb1 = sys.argv[1]
    fileinputsubstruct = sys.argv[2]

    prefix = check_filename(fileinputpdb1) 

    print ('input_pdb1 =' + fileinputpdb1)
    print ('input_txt  =' + fileinputsubstruct)
    print ('prefix =' + prefix)
    dict_substruct = {} 
    fh = open(fileinputsubstruct,'r')

    for line in fh: 
        splitline = line.strip().split('\t')
        key = int(splitline[0])
        def_string = ''
        for i in range(1,len(splitline)): 
           def_string = def_string + " " + splitline[i]
        if key in dict_substruct: 
           print("%s is allready in dictionary"%key) 
        dict_substruct[key] = def_string
        print(key,def_string)
    fh.close()
    #center = centre_of_mass(pdblist)
    # calculate the center of mass of the full file that contains all molecles
    #center1 = readin_all_atoms_center_of_mass(fileinputpdb1)
    chains = readin_all_atoms_return_chains(fileinputpdb1)
    print ("number of chains = %d"%len(chains))  
    #print chains[0][0].chainid
    #print chains[1][0].chainid
    for i in range(len(chains)):
      chain1 = chains[i]
      #for j in range(i+1,len(chains)):
      for j in range(1,len(chains)):
         if j == i: 
            continue
         chain2 = chains[j]
         print("i=%d,j=%d"%(i,j))
         flag_write = min_dist_between_two_sets_of_atoms(chain1,'chain %s'%chain1[0].chainid,chain2,'chain %s'%chain2[0].chainid,5,dict_substruct)
main()
