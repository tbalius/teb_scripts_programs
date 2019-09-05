
#################################################################################################################
## Writen by Trent Balius in the Shoichet Lab, UCSF in 2015
## modifed in 2016
## modifed in 2019 at the FNLCR
#################################################################################################################
import sys
import sph_lib as sph
#import mol2 
import pdb_lib as pdb

def distance_sph_pdb(sphs,pdbatoms,dt): 
    sphlist = []

    for sph in sphs:
        for atom in pdbatoms:
            #d2 = (atom.X - sph.X)**2 + (atom.Y - sph.Y)**2 + (atom.Z - sph.Z)**2
            d2 = (atom.X - sph.X)**2 + (atom.Y - sph.Y)**2 + (atom.Z - sph.Z)**2 - sph.radius**2 # here we calculate the distance to the surface of the sphere.
            if d2 < float(dt)**2.0: 
                sphlist.append(sph)
                #break
           
    return sphlist



# this function reads a pdblist and returns a dictionary of pdblists with resnum as index.  
def make_dict_pdb_res(pdblist): 

    dict_pdb_res = {}
    # intialize list. 
    for atom in pdblist: 
        print atom.resnum 
        dict_pdb_res[int(atom.resnum)] = []
    # we could have one forloop where we check if it is in the list 
    # but I think that this is just as fast ?? 
    for atom in pdblist:
        dict_pdb_res[int(atom.resnum)].append(atom)

    return dict_pdb_res

# This function reeds in the list of residues

def read_list( filename ):
    list_res = []
    fh = open(filename,'r')
    fristline = True
    for line in fh:
        # skip the frist line. 
        if fristline: 
           fristline = False
           continue
        
        splitline = line.split()
        
        # continue if it is an empty line
        if len(splitline) == 0:
           continue  
        #print line
        if len(splitline) != 1: 
            print "Error list file is not right"
            exit(0)
        #print "-->", proc_line
        list_res.append(int(splitline[0][1:-1]))
    return list_res 

def int_list_to_string(ilist):
    s = ''
    l = len(ilist)
    frist = True
    for ele in ilist:
        if frist : 
           s = str(ele)
           frist = False
        else: 
           s = s+ ' , ' +str(ele)  
    return s

def main():
    if len(sys.argv) != 6: # if no input
       print "ERORR: there need to be 4 inputs: sph inputfilename, pdb inputfilename, res list outputfilename, distance."
       return

    fileinputsph  = sys.argv[1]
    fileinputpdb  = sys.argv[2]
    fileinputlist = sys.argv[3]
    fileoutput    = sys.argv[4]
    distance      = float(sys.argv[5])

    print 'input_sph =' + fileinputsph
    print 'input_pdb =' + fileinputpdb
    print 'input_list =' + fileinputlist
    print 'output =' + fileoutput
    print 'distance = %6.3f'%distance

    reslist = read_list(fileinputlist)
    #exit(0) 
    sphlist = sph.read_sph(fileinputsph,"A","A")

    pdblist = pdb.read_pdb(fileinputpdb)[0]    

    # make dictionary
    dict_pdblist = make_dict_pdb_res(pdblist) 

    fhout = open(fileoutput,'w')
    # for each residue find the spheres within a certian distance
    for res in reslist:  
       print res
       if not res in dict_pdblist: 
          print str(res) + " not in dict"
          continue
       list2 = distance_sph_pdb(sphlist, dict_pdblist[res], distance)
       sphere_cluster = {}
       for sphere in list2: 
           sphere_cluster[sphere.cluster] = ''
       # sorted clusters contain all the sphere clusters that are close to the residue.  note that the sphere cluster define a pocket. 
       sorted_clusters = sorted(sphere_cluster.keys())
       print "sphere clusters close to residue %d:"%(res), sorted_clusters
       if len(sorted_clusters) != 0:
           fhout.write("sphere clusters close to residue %d: %s\n"%(res,int_list_to_string(sorted_clusters)))
    print "I AM HERE" 
    #sph.write_sph(fileoutput,list2)

main()
