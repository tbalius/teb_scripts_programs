# this script makes a matrix of tc's between two sets pdb ligs (ref) and zinc mols (docked poses)

# this script requiers chemaxon.  
# put it in your path and define the license  
source /nfs/soft/jchem/current/env.csh

# source python
source /nfs/soft/python/envs/complete/latest/env.csh


set mountdir = `pwd`
cd $mountdir/workingdir/smiles

mkdir /scratch/fischer

python $mountdir/tanimoto_cal_axon.py -two pdbligands_mod2.smi zincligands_mod2.smi output2

echo "run this when safe to do so: rm /scratch/fischer/*.smi"

