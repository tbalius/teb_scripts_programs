
#################################################################################################################
## Writen by Trent Balius at FNLCR in 2020 (took from other scripts)
#################################################################################################################
import sys,os
import pdb_lib as pdb

#DOCKBASE = "/nfs/home/tbalius/zzz.github/DOCK"
# this script will process the crystalographic unitcell written out by chimera. 
 
def min_dist_between_two_sets_of_atoms(atom_list1,filename1,atom_list2,filename2,threshold):
        dict_res = {}
        flag_write = False
        print(filename1,filename2)
        if (filename1 == filename2): # all distances will be zeros. 
           print("%s is the center model. all distances are zeros"%filename1)
           return True
        for i in range(0,len(atom_list1)):
           if (atom_list1[i].resname == "HOH"): #skipe if water
               continue
           for j in range(0,len(atom_list2)):
               if (atom_list2[j].resname == "HOH"): # skipe if water
                  continue
               dist2 = 0.0
               dist2 = dist2 + (atom_list1[i].X-atom_list2[j].X)**2
               dist2 = dist2 + (atom_list1[i].Y-atom_list2[j].Y)**2
               dist2 = dist2 + (atom_list1[i].Z-atom_list2[j].Z)**2
               if (dist2<threshold**2.0): 
                   flag_write = True
                   dist = (dist2)**(1.0/2.0)
                   #print ('file = %s, %s,%s,%s,%s::%f'%(filename2,atom_list2[j].atomname,atom_list2[j].atomnum,atom_list2[j].resname,atom_list2[j].resnum,dist))
                   res = filename2+"::"+atom_list1[i].resname+atom_list1[i].resnum+"->"+atom_list2[j].resname+atom_list2[j].resnum
                   # populate dictionary with residue key and store the distance as the definition
                   if res in dict_res: # check if it is in the dictionary
                      if (dist < dict_res[res] ):
                         dict_res[res] = dist
                   else: 
                      dict_res[res] = dist
        for key in dict_res: 
           print('%s::%f'%(key,dict_res[key])) 
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
        print "number of atoms in reslist: " + str(count)
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
    if len(sys.argv) != 4: # if no input
       print ("ERORR: there need to be 3 inputs: pdb file_pdb_list dcutoff (center of ligand to center of model)")
       return

    fileinputpdb1 = sys.argv[1]
    file_pdb_list = sys.argv[2]
    #ligand_name   = sys.argv[3]
    #ligand_dist   = float(sys.argv[4])
    dist_to_center_protein   = float(sys.argv[3])

    prefix = check_filename(fileinputpdb1) 

    print ('input_pdb1 =' + fileinputpdb1)
    print ('sph prefix =' + prefix)
    print ('pdb list file =' + file_pdb_list)
    print ('dist = %d'%dist_to_center_protein)



    #center = centre_of_mass(pdblist)
    # calculate the center of mass of the full file that contains all molecles
    center1 = readin_all_atoms_center_of_mass(fileinputpdb1)
    fh = open(file_pdb_list,'r')
    dist_list = []
    pdb_f_list = []
    center_list = []
    # loop over the list of pdb files.  one file contains one model
    for line in fh:
       fileinputpdb2 = line.split()[0]
       print ('input_pdb2 =' + fileinputpdb2)
       check_filename(fileinputpdb2) 
       center2 = readin_all_atoms_center_of_mass(fileinputpdb2)
       d = distance(center1,center2)
       dist_list.append(d)
       pdb_f_list.append(fileinputpdb2)
       center_list.append(center2)
    distmin_id = 0
    distmin = dist_list[distmin_id]
    for i in range(0,len(dist_list)):
        if (dist_list[i] < distmin):
        #if dist_list[i] < dist_list[distmin_id]:
            distmin_id = i
            distmin = dist_list[distmin_id]
            
    print("The model closest (dist = %f) to center is %s" %(dist_list[distmin_id],pdb_f_list[distmin_id]))
    # lets get the ligand
    pdblist = pdb.read_pdb(pdb_f_list[distmin_id]) # read in the model that is closest to the center (this one should be completely suronded by neibors). 
    # get the atoms of the centeral protein
    atom_pro_list = []
    for pdbatoms in pdblist: 
        for atom in pdbatoms: 
            #print(atom.resname)
            #if (atom.resname == ligand_name):
                atom_pro_list.append(atom)
    pro_center = centre_of_mass(atom_pro_list)

    filelist = [] # remember wich models are close by center of position.  
    for i,center in enumerate(center_list):
        d = distance(center,pro_center)
        if d < dist_to_center_protein: 
           print("The model within cutoff (dist = %f) to center of %s" %(d,pdb_f_list[i]))
           filelist.append(pdb_f_list[i])
    cat_string = " files to cat "
    cat_cmd = " cat "
    for filename in filelist: 
       print(filename)
       pdblist = pdb.read_pdb(filename) # read in the model that is closest to the center (this one should be completely suronded by neibors). 
       atom_list = []
       for pdbatoms in pdblist: 
          for atom in pdbatoms: 
              #print(atom.resname)
              atom_list.append(atom)

       flag_write = min_dist_between_two_sets_of_atoms(atom_pro_list,pdb_f_list[distmin_id],atom_list,filename,5)
       if flag_write: 
           cat_string = cat_string + " " + filename 
           cat_cmd = cat_cmd + " " + filename 
    print(cat_string)
    os.system(cat_cmd+" > interfaces.pdb")
main()
