# this was otained from here http://www.rdkit.org/docs/Cookbook.html on April 13, 2016

""" contribution from Andrew Dalke """
# modifed by Trent Balius
import sys
from rdkit import Chem
from rdkit.Chem import AllChem

# Download this from http://pypi.python.org/pypi/futures
#from concurrent import futures


# The parameters (molecule and number of conformers) are passed via a Python
def generateconformations(m, n, maxAttempts=1000, pruneRmsThresh=0.1, useExpTorsionAnglePrefs=True, useBasicKnowledge=True, enforceChirality=True):
    m = Chem.AddHs(m)
    #ids=AllChem.EmbedMultipleConfs(m, numConfs=n)
    ids=AllChem.EmbedMultipleConfs(m, numConfs=n,maxAttempts=maxAttempts, pruneRmsThresh=pruneRmsThresh, useExpTorsionAnglePrefs=useExpTorsionAnglePrefs, useBasicKnowledge=useBasicKnowledge, enforceChirality=enforceChirality, numThreads=0)
    for cid in ids:
        #AllChem.UFFOptimizeMolecule(m, confId=cid)
        AllChem.MMFFOptimizeMolecule(m, confId=cid)
    # EmbedMultipleConfs returns a Boost-wrapped type which
    # cannot be pickled. Convert it to a Python list, which can.
    #rmslist =[]
    #AllChem.AlignMolConformers(m, RMSlist=rmslist)
    AllChem.AlignMolConformers(m)
    #rms = AllChem.GetConformerRMS(m, 1, 9, prealigned=True)

    return m, list(ids)

smi_input_file  = sys.argv[1]
sdf_output_file = sys.argv[2]

n = int(sys.argv[3])

writer = Chem.SDWriter(sdf_output_file)

suppl = Chem.SmilesMolSupplier(smi_input_file, titleLine=False)
i = 0
for mol in suppl:
    print i
    molc,ids = generateconformations(mol, n)
    for id in ids:
        writer.write(molc, confId=id)
    i=i+1
writer.close()
