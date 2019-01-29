
setenv AMBERHOME /nfs/soft/amber/amber14

#grep -v 'H$' receptor.pdb > rec.pdb

cat << EOF > tleap.lig.in
set default PBradii mbondi2
# load the protein force field
source leaprc.ff14SB
# load in GAFF
source leaprc.gaff

# load ligand and covalent parameters.  
loadamberparams lig/lig.ante.charge.frcmod
loadamberprep lig/lig.ante.charge.prep

# load pdb file 
LIG = loadpdb lig/lig.ante.pdb 

saveamberparm LIG lig.leap.prm7 lig.leap.rst7

quit
EOF

#$AMBERHOME/bin/tleap 
$AMBERHOME/bin/tleap -s -f tleap.lig.in > ! tleap.lig.out
