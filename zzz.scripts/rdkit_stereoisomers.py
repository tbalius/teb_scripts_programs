
## https://www.rdkit.org/docs/source/rdkit.Chem.EnumerateStereoisomers.html
import sys
from rdkit import Chem

from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions

## all even the imposible
#m = Chem.MolFromSmiles('BrC=CC1OC(C2)(F)C2(Cl)C1')
#
#isomers = tuple(EnumerateStereoisomers(m))
#
#len(isomers)
#
#for smi in sorted(Chem.MolToSmiles(x, isomericSmiles=True) for x in isomers):
#    print(smi)
#
## only posible 
#opts = StereoEnumerationOptions(tryEmbedding=True)
#
#isomers = tuple(EnumerateStereoisomers(m, options=opts))
#
#len(isomers)
#
#for smi in sorted(Chem.MolToSmiles(x,isomericSmiles=True) for x in isomers):
#
#    print(smi)
#
## uniq
#m = Chem.MolFromSmiles('FC(Cl)C=CC=CC(F)Cl')
#
#opts = StereoEnumerationOptions(unique=True)
#
#isomers = tuple(EnumerateStereoisomers(m, options=opts))
#
#len(isomers)
#
#for smi in sorted(Chem.MolToSmiles(x,isomericSmiles=True) for x in isomers):
#    print(smi)

# opts = StereoEnumerationOptions(onlyUnassigned=False)


def main(): 

  filename = sys.argv[1]
  outfilename = sys.argv[2]
  print(filename)
  print(outfilename)
  fh = open(filename,'r')
  fhw = open(outfilename,'w')
  count = 1
  for line in fh: 
      sline = line.split()
      smi = sline[0]
      name = sline[1]
      # uniq
      m = Chem.MolFromSmiles(smi)
      opts = StereoEnumerationOptions(tryEmbedding=True,unique=True)
      #opts = StereoEnumerationOptions(tryEmbedding=True,unique=True,onlyStereoGroups=True)
      isomers = tuple(EnumerateStereoisomers(m, options=opts))
      print ('there are %d unique isomers.'%len(isomers))
      for smi in sorted(Chem.MolToSmiles(x,isomericSmiles=True) for x in isomers):
           fhw.write('%s %s_%d\n'%(smi,name,count))
           count = count + 1
  fh.close()
  fhw.close()
main()
  
