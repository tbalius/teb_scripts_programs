#!/usr/bin/python
import os, sys, subprocess
from argparse import ArgumentParser
from openeye  import oechem
import numpy as np

parser = ArgumentParser(description='Thsi will prepare ligand parameters using antechamber.')
parser.add_argument('-l','--lig',  dest='lig',  help='Input ligand <pdb> file')
parser.add_argument('-g','--gaff', dest='gaff', help='GAFF version: 1, 2')

def main():
    opt = parser.parse_args()

    global which_gaff
    if opt.gaff:
        which_gaff = opt.gaff
    else:
        which_gaff = 1 # 2--> gaff2

    global lig_input_mol2
    if opt.lig:
        lig_input_mol2 = opt.lig
    else:
        lig_input_mol2 = 'lig_in.mol2'

    # ============== #
    # new protocol:
    # (1) amber bond typer --> ac file (2) openeye convert aromatic mol2 --> kekule form assignment with oechem.OEKekulize(mol) 
    # ============== #

    command = '$AMBERHOME/bin/antechamber -i %s -fi mol2 -o lig.ac -fo ac -j 2 -dr n -pf y' % lig_input_mol2
    print(command)
    subprocess.call(command, shell=True)

    molecule = oechem.OEGraphMol()

    ifs = oechem.oemolistream(lig_input_mol2)
    flavor = oechem.OEIFlavor_Generic_Default | oechem.OEIFlavor_MOL2_Default | oechem.OEIFlavor_MOL2_Forcefield
    ifs.SetFlavor(oechem.OEFormat_MOL2, flavor)
    oechem.OEReadMol2File(ifs, molecule)
    print(molecule.GetTitle())

    # Define mapping from GAFF bond orders to OpenEye bond orders.
    order_map = { 1 : 1, 2 : 2, 3: 3, 7 : 1, 8 : 2, 9 : 5, 10 : 5 }
    # Read bonds.
    infile = open('lig.ac')
    lines = infile.readlines()
    infile.close()
    antechamber_bond_types = list()
    for line in lines:
        elements = line.split()
        if elements[0] == 'BOND':
            antechamber_bond_types.append(int(elements[4]))
    oechem.OEClearAromaticFlags(molecule)
    for (bond, antechamber_bond_type) in zip(molecule.GetBonds(), antechamber_bond_types):
        #bond.SetOrder(order_map[antechamber_bond_type])
        bond.SetIntType(order_map[antechamber_bond_type])
    oechem.OEFindRingAtomsAndBonds(molecule)
    oechem.OEKekulize(molecule)
    oechem.OEAssignFormalCharges(molecule)
    oechem.OEAssignAromaticFlags(molecule, oechem.OEAroModelOpenEye)

    """
    charges = [ atom.GetFormalCharge() for atom in molecule.GetAtoms() ]
    net_charge = np.array(charges).sum()
    print("Net Charge:", net_charge)
    """
    subprocess.call('grep CHARGE lig.ac', shell=True)
    with open('lig.ac', "r") as f:
        line = f.readline()
#        if line.find("CHARGE") > -1 and len(line.split())> 2:
#            net_charge = int( float( line.split()[1] ) )
        if line.find("CHARGE") > -1:
            net_charge = int( line[line.find("(")+1:line.find(")")] )
    print("Net Charge:", net_charge)

    # Write mol2 file for this molecule.
    outmol = oechem.OEMol(molecule)
    ofs = oechem.oemolostream()
    filename = 'lig_oe.mol2'
    ofs.open(filename)
    oechem.OEWriteMolecule(ofs, outmol)
    ofs.close()

    if which_gaff == 1:
        gaff = "gaff"
    elif which_gaff == 2:
        gaff = "gaff2"

    command = "$AMBERHOME/bin/antechamber -i lig_oe.mol2 -fi mol2 -o lig_bcc.mol2 -fo mol2 -c bcc -at %s -nc %i -j 5 -pf y -dr n" \
    % (gaff, net_charge)
    print(command)
    subprocess.call(command, shell=True)

    command = "$AMBERHOME/bin/parmchk2 -i lig_bcc.mol2 -f mol2 -s %d -o lig.frcmod" % (which_gaff)
    print(command)
    subprocess.call(command, shell=True)
    

if __name__ == "__main__":
    main()


