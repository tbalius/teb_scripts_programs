#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# this ways copyed and then modified from:
# http://sebsauvage.net/python/gui/#import
# Written by Trent Balius (shoichet lab, 2016) 


import sys,math,os, shutil,os.path , string
import pdb_lib


def dist_wat(wat1,wat2):
    dist = (wat1.X-wat2.X)**2.0 + (wat1.Y-wat2.Y)**2.0 + (wat1.Z-wat2.Z)**2.0
    return math.sqrt(dist)

def cluster_water_pdb(inputfilename,cutoff,outputfilename,denominator):
    bonds = []
    bond_dic = {}
    duplicate = {}
    pdb_ori = pdb_lib.read_pdb(inputfilename)[0]
    pdb_water = []
    pdb_other = []
    #print inputfilename
    for atom in pdb_ori:
         #print atom.resname
         if atom.resname == "HOH":
            pdb_water.append(atom)
         else:
            pdb_other.append(atom)
    numwat = len(pdb_water)
    print "%s contains %d waters" %(inputfilename,numwat)
    if numwat == 0: 
       print "There are zero waters in the file.  If this is not right make sure that there are no TER in the file and re-run. "
    for i in range(numwat):
        for j in range(i+1,numwat):
            dist = dist_wat(pdb_water[i],pdb_water[j])
            #print i, j, pdb_water[i].resnum, pdb_water[j].resnum, dist
            if (dist == 0.0): # discard duplicates
               duplicate[j] = i
            elif (dist < cutoff):
               #bonds.append([i,j, dist])
               bonds.append([i,j])
               print "bond: %d %d %f"%(i, j, dist)
               bond_dic[i] = 1
               bond_dic[j] = 1
            

    clusters = {} # what cluster belongs to each atom
    count = 0
    # 
    for bond in bonds:
        if bond[0] in clusters: # if the starting point is in a cluster then put the ending point in that same cluster
           clusters[bond[1]] = clusters[bond[0]]
        elif bond[1] in clusters: # if the ending point is in a cluster then put the starting point in that same cluster
           clusters[bond[0]] = clusters[bond[1]]
        else: # nether point is in a cluster
           clusters[bond[0]] = count
           clusters[bond[1]] = count
           count = count +1
    for i in range(numwat):
        if not i in bond_dic and not i in duplicate:
           # then singlton.
           clusters[i] = count
           count = count+1

    cluster_lists = {} # list of atoms in each cluster
    print clusters
    for key in clusters.keys(): # key is atom
        print key, clusters[key]
        cluster_lists[clusters[key]] = [] # intialize

    for key in clusters.keys():
        cluster_lists[clusters[key]].append(key)

    cluster_centers = []
    cluster_median = []
    for cluster in cluster_lists: 
        X = 0.0
        Y = 0.0
        Z = 0.0
        count = 0
        for atom in cluster_lists[cluster]:
               X = X + pdb_water[atom].X
               Y = Y + pdb_water[atom].Y
               Z = Z + pdb_water[atom].Z
               count = count + 1
        X = X/count
        Y = Y/count
        Z = Z/count
            
        #alpha = float(count)/float(numwat)
        alpha = float(count)/denominator
        temp_atom_info = pdb_lib.PDB_atom_info('',"A","HOH",cluster," O  ",cluster,X,Y,Z,0.0,alpha,False)

        # find median water
        min_val = [-1, 1000]
        for i in range(len(cluster_lists[cluster])):
		dist = dist_wat(temp_atom_info, pdb_water[cluster_lists[cluster][i]])
		if dist < min_val[1]:
			#min_val[0] = i  # this index of the cluster member
			min_val[0] = cluster_lists[cluster][i] # index of the water, simplifies call
			min_val[1] = dist
			pdb_water[cluster_lists[cluster][i]].bfact = temp_atom_info.bfact # make both report the number of waters/ dem in b column

        cluster_centers.append(temp_atom_info)
        #cluster_median.append(pdb_water[cluster_lists[cluster][min_val[0]]]) # when we saved the index of the cluster instead of index of water
        cluster_median.append(pdb_water[min_val[0]]) # 

    pdb_lib.output_pdb(cluster_centers,outputfilename+"_center.pdb")
    pdb_lib.output_pdb(cluster_median,outputfilename+"_median.pdb")
    #return clusters, count
 

def main():

        if (len(sys.argv) != 5):
              print "Give this script 4 inputs:"
              print "(1) input pdb "
              print "(2) distance threshold "
              print "(3) output pdb prefix"
              print "(4) denominator (this could be the number of pdb files from which water are obtained,\n     beta column need to be a decemial) "
              exit()

        infilename = sys.argv[1]
        distance = float(sys.argv[2])
        outfilename = sys.argv[3]
        den = int(sys.argv[4])

        print "input filename: "+infilename
        print "distance: "+str(distance)
        print "output fileprifix: "+outfilename
        print "denominator: " + str(den)

        cluster_water_pdb(infilename,distance,outfilename,den)

if -1 != string.find(sys.argv[0], "water_clustering.py"):
   main()

