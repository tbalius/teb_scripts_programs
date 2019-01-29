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
                   atomname = line[12:16]
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
       cluster_mol(mol,0.5,1.9)  
       count = count + 1

    print "done"
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

            if ( dist2 < dj2):
                #print "Atoms are close" + " dist2 = " + str(dist2)
                #print "likely bond::" + atom1.resname + atom1.resnum + atom1.chainid + "---" + atom2.resname + atom2.resnum + atom2.chainid
                count =  count + 1
                count_atom =  count_atom + 1

            if (dist2 < di2):
                print "Warning: Atoms are too close," + " dist2 = " + str(dist2)
                count_clash = count_clash + 1
        if (count_atom == 0):
           print "there is an atom that has no connections "
           print atom1.molname + " :: " + " atom " + str(i) + " " + atom1.atomname + " " + atom1.atomnum #+ " " +  atom1.resname + " " + atom1.resnum + " " + atom1.chainid

    if (count_clash > 0):
       print "internal clash"

    ## start clustring 
    cnum = make_cluster(dist2mat,dj2)
    if (cnum > 1):
        print atom1.molname, 
        print " has " + str(cnum) + " fragmented :: there's a problem...\n\n\n"
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
def min_dist_between_clusters(Matrix,list1,list2):

    min_val = 10000

    #print list1,list2

    for i in list1:
        for j in list2:
            if ( Matrix[i][j] < min_val):
                min_val = Matrix[i][j]

    #print min_val
    return min_val

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
def min_linkage(clusters,dist2mat,d2):

    N = len(dist2mat)
    num_cluster = len(clusters)

    count = 0
    final_clusters = []
    new_clusters   = []

    while ( len(clusters) + len(new_clusters) > 1 and count < N*N) :
        #print count 
        i = 0
        new_clusters = []
        while ( len(clusters) > 0):
            #print len(clusters)
            #print num_cluster
            #for i in range(len(clusters)):
            flag = True
            clust_min_val = 10000
            j = 1
            while ( j < len(clusters)):
                #print j
                val = min_dist_between_clusters(dist2mat,clusters[i],clusters[j])
                if (val < clust_min_val): ## find one pair within the thresold
                    clust_min_val = val
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
## Note that python passes pointer to lists,
## so modifing the list in the fuction is still modified outside.
#################################################################################################################
def make_cluster(dist2mat,d2):
    #print 'd2 = ', d2
    ## i is liked to j 
    ## if i is in the cluster then add to the same clusterj. 
    N = len(dist2mat)

    clusters = []
    count = 0

    for i in range(N):
        temp_clust = [i]
        clusters.append(temp_clust)

    clusters = min_linkage(clusters,dist2mat,d2)

    if len(clusters) > 1:
       print len(clusters), clusters
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
