#!/usr/bin/env python2.7
from __future__ import division
import os
import sys
import logging
from openeye.oechem import *
from openeye.oeomega import *
import numpy as np


def set_defaults(omega, limitConfs=200, energyWindow=12):
    # File Parameters
    omega.SetCommentEnergy(True)
    #omega.SetIncludeInput(False)
    omega.SetIncludeInput(True)
    omega.SetRotorOffset(False) #Enkhee
    omega.SetSDEnergy(False)
    omega.SetWarts(True)
    # 3D Construction Parameters
    omega.SetBuildForceField('mmff94s')
    omega.SetCanonOrder(True)
    omega.SetFixDeleteH(True)
    omega.SetDielectric(1.0)
    omega.SetExponent(1.0)
    omega.SetFixRMS(0.15)
    #omega.SetFixRMS(0.01)# jklyu modify this to keep more conformors
    omega.SetFromCT(False)
    omega.SetFixMaxMatch(1)
    omega.SetFixUniqueMatch(True)
    # Structure Enumeration Parameters
    omega.SetEnumNitrogen(False)
    omega.SetEnumRing(False)#Enkhee  # TS & MK 20160524 (from False) (Improves ring pucker sampling)
    # Torsion Driving Parameters
    omega.SetEnergyWindow(energyWindow)  # JJI 20160329  # TS & MK 20160524 (from 6)
    omega.SetMaxConfs(limitConfs)
    omega.SetMaxRotors(-1)
    omega.SetMaxSearchTime(120.0)
    omega.SetRangeIncrement(5)
    omega.SetRMSThreshold(0.50)  # JJI 20160329 # TS & MK 20160524 (from .5)
    #omega.SetRMSThreshold(0.01)  # jklyu modify this to keep more conformors
    omega.SetSearchForceField('mmff94s')
    
    omega.SetTorsionDrive(True)
    #omega.SetTorsionDrive(False)
    # Stereochemsitry
    #omega.SetStrictStereo(False)
    omega.SetStrictAtomTypes(False)

# Parse arguments here
infile = sys.argv[1]
limitConfs = int(sys.argv[2])

if os.environ.get('OMEGA_ENERGY_WINDOW', '').strip() != '':
    energyWindow = int(os.environ['OMEGA_ENERGY_WINDOW'])
else:
    energyWindow = 15.0

#if os.environ.get('OMEGA_MAX_CONFS', '').strip() != '':
#    limitConfs = int(os.environ['OMEGA_MAX_CONFS'])
#else:
#    limitConfs = 200

logging.warn('Setting energy window to %d and max confs to %d' % (energyWindow, limitConfs))


inroot, inext = os.path.splitext(infile)

mol = OEGraphMol()
ifs = oemolistream(infile)
print(inroot, inext)
if inext == ".pdb":
    flavor = OEIFlavor_Generic_Default | OEIFlavor_PDB_Default | OEIFlavor_PDB_ALL
    ifs.SetFlavor(OEFormat_PDB, flavor)
    OEReadPDBFile(ifs, mol)
elif inext == ".mol2":
    flavor = OEIFlavor_Generic_Default | OEIFlavor_MOL2_Default | OEIFlavor_MOL2_Forcefield
    ifs.SetFlavor(OEFormat_MOL2, flavor)
    OEReadMol2File(ifs, mol)
print(mol.GetTitle())

# Add explicit hydrogens.
#OEDetermineConnectivity(mol)
#OEFindRingAtomsAndBonds(mol)
#OEPerceiveBondOrders(mol)
#OEDetermineAromaticRingSystems(mol)
#OEAssignAromaticFlags(mol) # check aromaticity
#print("Number of aromatic atoms =", oechem.OECount(mol, oechem.OEIsAromaticAtom()))
#OEAssignImplicitHydrogens(mol)
#OEAssignFormalCharges(mol)
#charges = [ atom.GetFormalCharge() for atom in mol.GetAtoms() ]
#net_charge = np.array(charges).sum()
#print("Net Charge:", net_charge)

omega = OEOmega()
set_defaults(omega, limitConfs=limitConfs, energyWindow=energyWindow)

oechem.OEDetermineComponents(mol)
count, ringlist = oechem.OEDetermineRingSystems(mol)

print ('energy: ', omega.GetEnergyWindow())
print ('conf: ', omega.GetMaxConfs() )

outfile = "ligand_confs.mol2" 
ofs = oemolostream(outfile)
molcopy = oechem.OEMol(mol)
if omega(molcopy):
    OEWriteMolecule(ofs, molcopy)
ofs.close()


