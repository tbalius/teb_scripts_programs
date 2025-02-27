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
#  DOCK6 colors
#    null
#    hydrophobic
#    acceptor
#    donor
#    polar
#    
##########################################################################################

import sph_lib 
import pdb_lib
import sys

def color_spheres(spheres,pdb_atoms):

    #dt = 2.5
    #dt = 3.0
    dt = 3.5
    #dt = 4.0
    spheres_mod = []
    for sph in spheres: 
        print("sphere index = %4d"%sph.index)
        #print("sphere color start = %3d"%sph.sphere_color)
        for atom in pdb_atoms: 
            breakflag = False; # 
            #d2 = (atom.X - sph.X)**2 + (atom.Y - sph.Y)**2 + (atom.Z - sph.Z)**2 - sph.radius**2 # here we calculate the distance to the surface of the sphere.
            d2 = (atom.X - sph.X)**2 + (atom.Y - sph.Y)**2 + (atom.Z - sph.Z)**2  
            if d2 <= float(dt)**2.0:
                print "***%s*****%s*****%6.3f****"%(atom.resname, atom.atomname, d2)
                if ((atom.resname == "ASP" and atom.atomname == ' OD1') or 
                    (atom.resname == "ASP" and atom.atomname == ' OD2') or
                    (atom.resname == "GLU" and atom.atomname == ' OE1') or 
                    (atom.resname == "GLU" and atom.atomname == ' OE2') ): 
                    #if (atom.atomname ==  # O
                    print atom.resname, atom.atomname, d2
                    if (sph.sphere_color == 0 or sph.sphere_color == 1):
                        sph.sphere_color = 2 # acceptor
                    elif (sph.sphere_color == 3):
                       sph.sphere_color = 4 # polar
                    #breakflag = True; # conitue to next sphere
                if ( atom.atomname == ' N  ' or 
                    (atom.resname == "SER" and atom.atomname == ' OG ') or 
                    (atom.resname == "THR" and atom.atomname == ' OG1') or 
                    (atom.resname == "TYR" and atom.atomname == ' OH ') or 
                    (atom.resname == "ASN" and atom.atomname == ' ND2') or 
                    (atom.resname == "GLN" and atom.atomname == ' NE2')): 
                    print "rec atom donor", atom.resname, atom.atomname, d2
                    if (sph.sphere_color == 0 or sph.sphere_color == 1):
                       sph.sphere_color = 2 # acceptor
                    elif (sph.sphere_color == 3):
                       sph.sphere_color = 4 # polar
                if ((atom.resname == "ARG" and atom.atomname == ' NE ') or 
                    (atom.resname == "ARG" and atom.atomname == ' NH1') or
                    (atom.resname == "ARG" and atom.atomname == ' NH2') or
                    (atom.resname == "LYS" and atom.atomname == ' NZ ')): 
                    #if (atom.atomname ==  # N
                    #print atom.resname, atom.atomname, d2
                    print "rec atom donor", atom.resname, atom.atomname, d2
                    if (sph.sphere_color == 0 or sph.sphere_color == 1):
                       sph.sphere_color = 3 # donor
                    elif (sph.sphere_color == 2):
                       sph.sphere_color = 4 # polar
                if ( atom.atomname == ' O  ' or  
                    (atom.resname == "ASN" and atom.atomname == ' OD1') or
                    (atom.resname == "GLN" and atom.atomname == ' OE1')):
                    print "rec atom acceptor", atom.resname, atom.atomname, d2
                    if (sph.sphere_color == 0 or sph.sphere_color == 1):
                       sph.sphere_color = 3 # donor
                    elif (sph.sphere_color == 2):
                       sph.sphere_color = 4 # polar; acceptor and donor
                print atom.atomname + " "+ atom.atomname[1:2] 
                if ( atom.atomname[1:2] == 'C'):
                    print "Hydrophobic", atom.resname, atom.atomname, d2
                if ( atom.atomname[1:2] == 'C' and sph.sphere_color == 0 ):
                    sph.sphere_color = 1
        #print("sphere color end = %3d"%sph.sphere_color)
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

    header = ""
    header = header + "color   null          0 \n"
    header = header + "color   hydrophobic   1 \n"
    header = header + "color   donor         2 \n"
    header = header + "color   acceptor      3 \n"
    header = header + "color   polar         4 \n"

    sph_lib.write_sph_header(fileoutputsph,sphlistNew,header)

main()
