#!/usr/bin/python2.6 

import sys
import math
import pybel


## This script calculates a symestry corrected rmsd using open babel.


## This script was modified from the web:
## https://gist.github.com/974477

def squared_distance(coordsA, coordsB):
  """Find the squared distance between two 3-tuples"""
  sqrdist = sum( (a-b)**2 for a, b in zip(coordsA, coordsB) )
  return sqrdist


def rmsd(allcoordsA, allcoordsB):
  """Find the RMSD between two lists of 3-tuples"""
  deviation = sum(squared_distance(atomA, atomB) for
  (atomA, atomB) in zip(allcoordsA, allcoordsB))
  return math.sqrt(deviation / float(len(allcoordsA)))


def main():

   if len(sys.argv) != 3: # if no input
       print "ERORR: not the right number of arguments."
       print "this script takes in to input files: reference file, dockposes file"
       return
   referencefile = sys.argv[1]
   dockposesfile = sys.argv[2]


   # Read reference pose
   reference = next(pybel.readfile("mol2", referencefile))
   # Find automorphisms involving only non-H atoms
   mappings = pybel.ob.vvpairUIntUInt()
   bitvec = pybel.ob.OBBitVec()
   lookup = []

   for i, atom in enumerate(reference):
       if not atom.OBAtom.IsHydrogen():
           bitvec.SetBitOn(i+1)
           lookup.append(i)
   success = pybel.ob.FindAutomorphisms(reference.OBMol, mappings, bitvec)

   # Find the RMSD between the reference pose and each docked pose

   xtalcoords = [atom.coords for atom in reference if not atom.OBAtom.IsHydrogen()]

   for i, dockedpose in enumerate(pybel.readfile("mol2", dockposesfile)):
       posecoords = [atom.coords for atom in dockedpose if not atom.OBAtom.IsHydrogen()]
       minrmsd = 999999999999

       for mapping in mappings:
           automorph_coords = [None] * len(xtalcoords)
           for x, y in mapping:
              automorph_coords[lookup.index(x)] = xtalcoords[lookup.index(y)]

           mapping_rmsd = rmsd(posecoords, automorph_coords)
           if mapping_rmsd < minrmsd:
               minrmsd = mapping_rmsd

       print("The RMSD is %.6f for pose %d" % (minrmsd, (i+1)))


main()
