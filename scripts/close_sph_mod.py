
#################################################################################################################
## Writen by Trent Balius in the Shoichet Lab, UCSF in 2015
## modifed in 2016
#################################################################################################################
import sys
import sph_lib as sph
#import mol2 
import pdb_lib as pdb

def distance_sph_pdb(sphs,pdbatoms,dt): 
    sphlist = []

    for sph in sphs:
        for atom in pdbatoms:
            d2 = (atom.X - sph.X)**2 + (atom.Y - sph.Y)**2 + (atom.Z - sph.Z)**2
            if d2 < float(dt)**2.0: 
                sphlist.append(sph)
                break
           
    return sphlist

def main():
    if len(sys.argv) != 5: # if no input
       print "ERORR: there need to be 4 inputs: sph inputfilename, pdb inputfilename, outputfilename, distance."
       return

    fileinputsph = sys.argv[1]
    fileinputpdb = sys.argv[2]
    fileoutput   = sys.argv[3]
    distance     = float(sys.argv[4])

    print 'input_sph =' + fileinputsph
    print 'input_pdb =' + fileinputpdb
    print 'output =' + fileoutput
    print 'distance = %6.3f'%distance

    list = sph.read_sph(fileinputsph,"A","A")
    pdblist = pdb.read_pdb(fileinputpdb)[0]    
    list2 = distance_sph_pdb(list, pdblist,distance)
    sph.write_sph(fileoutput,list2)

main()
