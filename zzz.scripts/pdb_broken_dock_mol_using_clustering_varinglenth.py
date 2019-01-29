#! /usr/bin/python
import sys

### 
# This programs was writen by Trent E. Balius, the Shoichet Group, UCSF, 2012
###


class PDB_atom_info:
    def __init__(self, molname, chainid, resname, resnum, atomname, atomnum, X, Y, Z, boolhet):
        self.molname  = molname
        self.chainid  = chainid
        self.resname  = resname
        self.resnum   = resnum
        self.atomname = atomname
        self.atomnum  = atomnum
        self.X        = X
        self.Y        = Y
        self.Z        = Z
        self.boolhet  = boolhet

    def __cmp__(self, other):
        return cmp(self.chainid, other.chainid)
# this defines a compares two LIG_DATA by comparing the two scores
# it is sorted in decinding order.
def byResId(x, y):
    str1 = x.resname + x.chainid + x.resnum
    str2 = y.resname + y.chainid + y.resnum
    return cmp(str1,str2)


def cov_radius(ele):
# These covalent radii are defined according to the CRC Handbook
# of Chemistry and Physics, 91st Ed., 2010-2011, pp 9-49 to 9-50

    COV_RADII_H = 0.32
    COV_RADII_C = 0.75
    COV_RADII_N = 0.71
    COV_RADII_O = 0.64
    COV_RADII_P = 1.09
    COV_RADII_S = 1.04
 # The following are from 
 # http://pubs.rsc.org/en/content/articlehtml/2008/dt/b801115j
    COV_RADII_Si = 1.11
    COV_RADII_Cl = 1.02
    COV_RADII_F  = 0.57 
    COV_RADII_I  = 1.39  
    COV_RADII_Br = 1.20

    if   ( ele == 'Si' ):
         radius = COV_RADII_Si
    elif ( ele == 'S'  ):
         radius = COV_RADII_S
    elif ( ele == 'Cl' ):
         radius = COV_RADII_Cl
    elif ( ele == 'C'  ):
         radius = COV_RADII_C
    elif ( ele == 'Br' ):
         radius = COV_RADII_Br
    elif ( ele == 'H'  ):
         radius = COV_RADII_H
    elif ( ele == 'N'  ):
         radius = COV_RADII_N
    elif ( ele == 'O'  ):
         radius = COV_RADII_O
    elif ( ele == 'F'  ):
         radius = COV_RADII_F
    elif ( ele == 'P'  ):
         radius = COV_RADII_P
    elif ( ele == 'I'  ):
         radius = COV_RADII_I
    elif ( ele == 'Du' ):
         radius = COV_RADII_C

    return radius


def look_up_bond(ele_name1,ele_name2):

  radius1 = cov_radius(ele_name1)
  radius2 = cov_radius(ele_name2) 

  return (radius1+radius2+0.2)

def atomname2elename(atomname):

    if (len(atomname) == 1):
       atomname = atomname + ' '

    if atomname[0] == 'S' or atomname[0] == 's':
       if atomname[1] == 'i' or atomname[1]=='I':
          elename = 'Si'
       else:
          elename = 'S'
    elif(atomname[0] == 'C' or atomname[0] == 'c'):
         if atomname[1] == 'l' or atomname[1]=='L':
            elename = 'Cl'
         else:
            elename = 'C'
    elif(atomname[0] == 'B' or atomname[0] == 'b'):
        if atomname[1] == 'r' or atomname[1]=='R':
           elename ='Br'
        else:
           elename= 'Du'
    elif(atomname[0] == 'H' or atomname[0] == 'h'):
        elename = 'H'
    elif(atomname[0] == 'N' or atomname[0] == 'n'):
        elename = 'N'
    elif(atomname[0] == 'O' or atomname[0] == 'o'):
        elename = 'O'
    elif(atomname[0] == 'F' or atomname[0] == 'f'):
        elename = 'F'
    elif(atomname[0] == 'P' or atomname[0] == 'p'):
        elename = 'P'
    elif(atomname[0] == 'I' or atomname[0] == 'i'):
        elename = 'I'
    else:
       elename = 'Du'
    return elename

def get_ideal_dist(atomname1,atomname2):
    ele1 = atomname2elename(atomname1)
    ele2 = atomname2elename(atomname2)
    #dist = look_up_bond(atomname2elename(atomname1),atomname2elename(atomname2));
    dist = look_up_bond(ele1,ele2);
    return dist*dist 

#################################################################################################################
def id_close_atoms_lig(pdb_file, pdb_out):
    
    ## this function will read in a muli-pdb file conatining ligands from docking hits.

    file1 = open(pdb_file,'r')
   
    temp_atom_list  = []
    mol_list        = []
 
    lines    = file1.readlines()
   
    file1.close()
 
    resstr_cur = ' '
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 1):
            if (linesplit[0] == "COMPND"):
                  molname = linesplit[2]
            if (linesplit[0] == "ATOM"):
                   chainid  = line[21]
                   resname  = line[17:20]
                   resnum   = line[23:26]
                   atomname = line[12:16].replace(' ', '')
                   atomnum  = line[9:12]
                   X        = float(line[30:38])
                   Y        = float(line[38:46])
                   Z        = float(line[46:54])
                   boolhet  = (linesplit[0] == "HETATM")
                   temp_atom_info = PDB_atom_info(molname,chainid,resname,resnum,atomname,atomnum,X,Y,Z,boolhet)
                   temp_atom_list.append(temp_atom_info)
            elif (linesplit[0] == "TER"):
                   mol_list.append(temp_atom_list)
                   temp_atom_list = []
    count = 0;        
    for mol in mol_list:
       #print count
       cluster_mol(mol,0.75,1.9)  
       count = count + 1

    #print "done"
    return 

#################################################################################################################
#################################################################################################################
def cluster_mol(mol,di,dj):

    ## This fuction will use hierarchical clustering cut at a minium distance to idenify clusters
    if (len(mol) == 0 ):
       print "len(mol) == 0 "
       return False


    count = 0 # count the number of contact points 
    count_atom = 0 # count the number of contact points 
    count_clash = 0 # count the number of contact points 
    dist2mat = []

    # installize matrix
    dist2mat = installize_matrix(len(mol),len(mol),0)
    boolmat  = installize_matrix(len(mol),len(mol),True)

    # fill matrix
    for i in range(len(mol)):
        count_atom = 0 # count the number of contact points 
        for j in range(len(mol)):
            if (i == j):
               continue
            atom1  = mol[i]
            atom2  = mol[j]

            di2       = di**2
            dj2       = dj**2

            X_diff_2       = (atom1.X - atom2.X)**2.0
            Y_diff_2       = (atom1.Y - atom2.Y)**2.0
            Z_diff_2       = (atom1.Z - atom2.Z)**2.0
            dist2          = (X_diff_2 + Y_diff_2 + Z_diff_2)
            dist2mat[i][j] = dist2

            d2 = get_ideal_dist(mol[i].atomname,mol[j].atomname)
            #if ( dist2 < dj2):
            if ( dist2 < d2):
                #print "Atoms are close" + " dist2 = " + str(dist2)
                #print "likely bond::" + atom1.resname + atom1.resnum + atom1.chainid + "---" + atom2.resname + atom2.resnum + atom2.chainid
                count =  count + 1
                count_atom =  count_atom + 1

            if (dist2 < di2):
                #print "Warning: Atoms are too close," + " dist2 = " + str(dist2)
                count_clash = count_clash + 1
        if (count_atom == 0):
           #print "there is an atom that has no connections "
           print atom1.molname + " : " + " atom " + str(i) + " " + atom1.atomname + " " + atom1.atomnum #+ " " +  atom1.resname + " " + atom1.resnum + " " + atom1.chainid

    if (count_clash > 0):
       print atom1.molname + " : " + "internal clash"

    ## start clustring 
    cnum = make_cluster(dist2mat,mol)
    if (cnum > 1):
        print atom1.molname + " : " + str(cnum) + " fragmented"
    #exit()
    ##     
    #for 
    #   count=count+1


#################################################################################################################
#################################################################################################################
def installize_matrix(N,M,val):
    matrix = []
    for i in range(N):
        row = []
        for j in range(M):
            row.append(val)
        matrix.append(row)
    return matrix
#################################################################################################################
#################################################################################################################
def print_matrix(matrix):
    for row in matrix:
        for ele in row:
            print round(ele,2),
        print " "
     
  
#################################################################################################################
#################################################################################################################
#def min_dist(Matrix,boolmat):
#
#    min_val = 10000
#    min_i   = -1
#    min_j   = -1
#
#    for i in range(len(Matrix)):
#        for j in range(len(Matrix[i])):
#            if ( i != j and boolmat[i][j] and Matrix[i][j] < min_val):
#                min_val = Matrix[i][j]
#                min_i   = i
#                min_j   = j
#
#    return min_val,min_i,min_j
#
#################################################################################################################
#################################################################################################################
def min_dist_between_clusters(Matrix,list1,list2,mol):

    min_val = 10000
    min_i = 0
    min_j = 0

    #print list1,list2

    for i in list1:
        ## H are never conected only conected to one atom in a mol.
        if atomname2elename(mol[i].atomname) == 'H' and len(list1) > 1:
           continue
        for j in list2:
            ## H are never conected to another H in a mol > 2 atoms
            if (atomname2elename(mol[i].atomname) == 'H' and atomname2elename(mol[j].atomname) == 'H'):
                continue
            ## H are never conected only conected to one atom in a mol.
            if (atomname2elename(mol[j].atomname) == 'H' and len(list2) > 1):
                continue
            if ( Matrix[i][j] < min_val):
                min_val = Matrix[i][j]
                min_i   = i
                min_j   = j

    #print min_val
    return min_val,min_i,min_j

#################################################################################################################
#################################################################################################################
def join_clusters(list1,list2):

    temp_clust = []

    for ele in list1:
       temp_clust.append(ele)
    for ele in list2:
       if not in_set(ele,temp_clust):
          temp_clust.append(ele)

    return temp_clust
#################################################################################################################
#################################################################################################################
def in_set(ele1,temp_clust):
    for ele2 in temp_clust:
        if (ele1 == ele2):
           return True
    return False

#################################################################################################################
#################################################################################################################
def min_linkage(clusters,dist2mat,mol):

    N = len(dist2mat)
    num_cluster = len(clusters)

    count = 0
    final_clusters = []
    new_clusters   = []

    old_cluster_len = 100000
    #while ( len(clusters) + len(new_clusters) > 1 and count < N*N) :
    while ( len(clusters) != old_cluster_len and count < N*N*N) :
        #print count 
        old_cluster_len = len(clusters)
        #print "# of Cluster " + str(len(clusters))
        i = 0
        new_clusters = []
        while ( len(clusters) > 0):
            #print len(clusters)
            #print num_cluster
            #for i in range(len(clusters)):
            flag = True
            clust_min_val = 10000
            d2 = 2.0
            j = 1
            while ( j < len(clusters)):
                #print j
                val, c_min_i, c_min_j = min_dist_between_clusters(dist2mat,clusters[i],clusters[j],mol)
                if (val < clust_min_val): ## find one pair within the thresold
                    clust_min_val = val
                    d2 = get_ideal_dist(mol[c_min_i].atomname,mol[c_min_j].atomname)
                    min_j = j
                j = j+1
            if (clust_min_val < d2):
                #print clusters[i],clusters[min_j]
                temp_clust = join_clusters(clusters[i],clusters[min_j])
                #print temp_clust
                new_clusters.append(temp_clust)
                del clusters[i]
                del clusters[min_j-1]
                #print new_clusters
            else:
    #            final_clusters.append(clusters[i])
                new_clusters.append(clusters[i])
                del clusters[i]
           
        clusters = new_clusters
        count = count+1
            
#    for cluster in new_clusters:
#        final_clusters.append(cluster)
#    print final_clusters
    #print clusters
    #print_matrix(dist2mat)
    #del clusters
    #return final_clusters
    return clusters

#################################################################################################################
#################################################################################################################
def print_clusters(clusters,mol,dist2mat):
    count = 0
    for cluster in clusters:
        print "cluster",count, ":", 
        for ele in cluster:
            #print ele, "(", mol[ele].atomname, ")",
            print mol[ele].atomname + " ", 
        print " "
        count = count+1
    for i in range(len(clusters)):
        for j in range(i+1,len(clusters)):
            print i,j,min_dist_between_clusters(dist2mat,clusters[i],clusters[j],mol)


#################################################################################################################
## Note that python passes pointer to lists,
## so modifing the list in the fuction is still modified outside.
#################################################################################################################
def make_cluster(dist2mat,mol):
    #print 'd2 = ', d2
    ## i is liked to j 
    ## if i is in the cluster then add to the same clusterj. 
    N = len(dist2mat)

    clusters = []
    count = 0

    for i in range(N):
        temp_clust = [i]
        clusters.append(temp_clust)

    clusters = min_linkage(clusters,dist2mat,mol)

    #if len(clusters) > 1:
    #   print len(clusters), clusters
    #   print_clusters(clusters,mol,dist2mat)
    return len(clusters)

#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print "This function takes as input a pdb file"
        print "id connected residues"
        print "writes a modified pdbfile with hetatoms combinded into redidue if short bond."
        print "python pdb_het_res_bonds_combine.py IN.pdb OUT.pdb CM"
        print "  IN.pdb -- input pdb file.  OUT.pdb -- output pdbfile."
        print len(sys.argv)
        return
    
    pdb_file  = sys.argv[1]
    pdb_out   = sys.argv[2]

    id_close_atoms_lig(pdb_file,pdb_out)
    
    
#################################################################################################################
#################################################################################################################
main()
