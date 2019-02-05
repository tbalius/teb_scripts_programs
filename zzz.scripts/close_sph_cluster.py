
#################################################################################################################
## Writen by Trent Balius in the Shoichet Lab, UCSF in 2015
## modifed in 2016
#################################################################################################################
import sys
import sph_lib as sph
#import mol2 
import pdb_lib as pdb
import copy


# this function curently find the closest sphere cluster (comparing the centroids of the pdbfile and the sphere file.  
def distance_sph_pdb(sph_clusts,pdbatoms): 
    sphlist = []

    pdb_centroid = [0.0, 0.0, 0.0]
    for atom in pdbatoms:
        pdb_centroid[0] = pdb_centroid[0] + atom.X
        pdb_centroid[1] = pdb_centroid[1] + atom.Y
        pdb_centroid[2] = pdb_centroid[2] + atom.Z
        
    pdb_centroid[0] = pdb_centroid[0] /float(len(pdbatoms))
    pdb_centroid[1] = pdb_centroid[1] /float(len(pdbatoms))
    pdb_centroid[2] = pdb_centroid[2] /float(len(pdbatoms)) 

    centroid_dist = []
    clust_count = 0
    min_dist  = 10000.0
    min_clust = -100
    for sphs in sph_clusts:

        sph_centroid = [0.0, 0.0, 0.0]
        for sph in sphs:
             sph_centroid[0] = sph_centroid[0] + sph.X
             sph_centroid[1] = sph_centroid[1] + sph.Y
             sph_centroid[2] = sph_centroid[2] + sph.Z

        sph_centroid[0] = sph_centroid[0] / float(len(sphs))
        sph_centroid[1] = sph_centroid[1] / float(len(sphs))
        sph_centroid[2] = sph_centroid[2] / float(len(sphs))

        d2 = 0.0
        for i in range(3):
            d2 = d2 + (pdb_centroid[i] - sph_centroid[i])**2
        centroid_dist.append([clust_count,d2])
        #print clust_count, d2
        if d2 < min_dist:
           min_dist = d2
           min_clust = clust_count
        
        #d2 = (atom.X - sph.X)**2 + (atom.Y - sph.Y)**2 + (atom.Z - sph.Z)**2
        #if d2 < float(dt)**2.0: 
        #     sphlist.append(sph)
        #     break
        clust_count = clust_count + 1
    print min_dist, min_clust
    sphlist = copy.copy(sph_clusts[min_clust])   
    return sphlist

def main():
    #if len(sys.argv) != 5: # if no input
    #   print "ERORR: there need to be 4 inputs: sph inputfilename, pdb inputfilename, outputfilename, distance."
    #   return
    if len(sys.argv) != 4: # if no input
       print "ERORR: there need to be 3 inputs: sph inputfilename, pdb inputfilename, outputfilename"
       return

    fileinputsph = sys.argv[1]
    fileinputpdb = sys.argv[2]
    fileoutput   = sys.argv[3]
    #distance     = float(sys.argv[4])

    print 'input_sph =' + fileinputsph
    print 'input_pdb =' + fileinputpdb
    print 'output =' + fileoutput
    #print 'distance = %6.3f'%distance

    sph_cluster_list = sph.read_sph_cluster_list(fileinputsph)
    pdblist = pdb.read_pdb(fileinputpdb)[0]    
    #list2 = distance_sph_pdb(sph_cluster_list, pdblist, distance)
    list2 = distance_sph_pdb(sph_cluster_list, pdblist)
    sph.write_sph(fileoutput,list2)

main()
