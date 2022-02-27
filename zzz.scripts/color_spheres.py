#! /bin/python2

# this script is written to color the spheres.  It is a replacement of the perl script. 


##########################################################################################
# Current coloring system:
#    positive                       (1)   e.g., sphere near 2 Asp/Glu
#    negative                       (2)   e.g., sphere near 2 Arg/Lys
#    acceptor                       (3)   e.g., sphere near backbone HN, Asn/Gln HN, Ser/Thr/Tyr HO
#    donor                          (4)   e.g., sphere near backbone O, Asn/Gln O
#    ester_o                        (5)
#    amide_o                        (6)
#    neutral                        (7)   e.g., sphere near nonpolar C only (no polar atoms)
#    not_neutral                    (8)   e.g., sphere near both positive and negative, pos_don and neg_acc
#    positive_or_donor              (9)   e.g., sphere near Asp/Glu O
#    negative_or_acceptor           (10)  e.g., sphere near Arg/Lys HN
#    neutral_or_acceptor_or_donor   (11)  e.g., sphere near S-related atoms (Cys, Cyx, Met S and HG)
#    donacc                         (12)  e.g., sphere near both donor & acceptor receptor atoms
##########################################################################################

import sph_lib 
import pdb_lib
import sys

def color_spheres(spheres,pdb_atoms):

    dt = 3.0
    spheres_mod = []
    for sph in spheres: 
        for atom in pdb_atoms: 
            breakflag = False; # 
            d2 = (atom.X - sph.X)**2 + (atom.Y - sph.Y)**2 + (atom.Z - sph.Z)**2 - sph.radius**2 # here we calculate the distance to the surface of the sphere.
            if d2 < float(dt)**2.0:
                #print "***%s*****%s*****%6.3f****"%(atom.resname, atom.atomname, d2)
                if ((atom.resname == "ASP" and atom.atomname == ' OD1') or 
                    (atom.resname == "ASP" and atom.atomname == ' OD2') or
                    (atom.resname == "GLU" and atom.atomname == ' OE1') or 
                    (atom.resname == "GLU" and atom.atomname == ' OE2') ): 
                    #if (atom.atomname ==  # O
                    print atom.resname, atom.atomname, d2
                    sph.sphere_color = 1 # postive
                    breakflag = True; # conitue to next sphere
                if ((atom.resname == "ARG" and atom.atomname == ' NE ') or 
                    (atom.resname == "ARG" and atom.atomname == ' NH1') or
                    (atom.resname == "ARG" and atom.atomname == ' NH2') or
                    (atom.resname == "LYS" and atom.atomname == ' NZ ')): 
                    #if (atom.atomname ==  # N
                    print atom.resname, atom.atomname, d2
                    if (sph.sphere_color == 0):
                       sph.sphere_color = 2 # negative
                    elif (sph.sphere_color == 1):
                       sph.sphere_color = 8 
                    breakflag = True; # conitue to next sphere
                if ( atom.atomname == ' HN ' or 
                    (atom.resname == "SER" and atom.atomname == ' HG ') or 
                    (atom.resname == "THR" and atom.atomname == ' HG1') or 
                    (atom.resname == "TYR" and atom.atomname == ' HH ') or 
                    (atom.resname == "ASN" and atom.atomname == 'HD21') or 
                    (atom.resname == "ASN" and atom.atomname == 'HD22') or 
                    (atom.resname == "GLN" and atom.atomname == 'HE21') or 
                    (atom.resname == "GLN" and atom.atomname == 'HE22')):
                    print atom.resname, atom.atomname, d2
                    if (sph.sphere_color == 0):
                       sph.sphere_color = 3 # acceptor
                    breakflag = True; # conitue to next sphere
                if ( atom.atomname == ' O  ' or  
                    (atom.resname == "ASN" and atom.atomname == ' OD1') or
                    (atom.resname == "GLN" and atom.atomname == ' OE1')):
                    print atom.resname, atom.atomname, d2
                    if (sph.sphere_color == 0):
                       sph.sphere_color = 4 # donor
                    elif (sph.sphere_color == 3):
                       sph.sphere_color = 12 # acceptor and donor
                    breakflag = True; # conitue to next sphere
                if ( atom.atomname[1:2] == 'C' and sph.sphere_color == 0 ):
                     sph.sphere_color = 7
                if (breakflag):
                    break; # conitue to next sphere
        #print ("I AM HERE") 
        #print (sph.sphere_color) 
        spheres_mod.append(sph)
    return spheres_mod
    

def main():
    if len(sys.argv) != 4: # if no input
       print "ERORR: there need to be 3 inputs: sph inputfilename, pdb inputfilename, sph output."
       return

    fileinputsph   = sys.argv[1]
    fileinputpdb   = sys.argv[2]
    fileoutputsph  = sys.argv[3]

    print 'input_sph =' + fileinputsph
    print 'input_pdb =' + fileinputpdb
    print 'output_sph =' + fileoutputsph

    
    sphlist = sph_lib.read_sph(fileinputsph,"A","A")
    pdblist = pdb_lib.read_pdb(fileinputpdb)[0]    

    sphlistNew = color_spheres(sphlist,pdblist)

    sph_lib.write_sph(fileoutputsph,sphlistNew)

main()
