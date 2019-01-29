
## Trent Balius, Shoichet group, UCSF, 2014.08.08


import urllib, urllib2, math
import scrape_pdb_for_uniprot as spfu
import scrape_pdb_for_lig_mod as spfl
import scrape_zinc_zincid as szzi
import tanimoto_cal_axon as tancal


print " stuff that matters::::::::::"

filein = open("uniprot_lig_tversky_flush.txt",'r')
fileout = open("uniprot_lig_tversky_mwdiff_formula_diff.txt",'w')

lig_smiles  = {}
lig_formula = {}

#theshold = 0.6
##max_MM = 250.0
#max_MM = 500.0 # molcular Mass
#min_MM = 70.0 

#count = 0
for line in filein:

    if "This" in line: 
        continue

    #if count == 10: 
    #   exit()
    #count = count+1
  
    print line
    splitline = line.split()

    lig1 = splitline[2].strip(',')
    lig2 = splitline[3].strip(',')
    print lig1, lig2


    if (lig1 in lig_smiles):
        smiles1  = lig_smiles[lig1]
        formula1 = lig_formula[lig1]
    else:
        smiles1 = spfl.scrape_pdb_for_lig_smiles(lig1)
        if (smiles1 == ''):
             continue 
        formula1 = tancal.MolecularFormula(smiles1)
    mw1 = float(tancal.molecularMass(smiles1))

    if (lig2 in lig_smiles):
        smiles2  = lig_smiles[lig2]
        formula2 = lig_formula[lig2]
    else:
        smiles2 = spfl.scrape_pdb_for_lig_smiles(lig2)
        if (smiles2 == ''):
            continue 
        formula2 = tancal.MolecularFormula(smiles2)
        lig_smiles[lig2] = smiles2
        lig_formula[lig2] = formula2
    mw2 = float(tancal.molecularMass(smiles2))
    #smiles_j = spfl.scrape_pdb_for_lig_smiles(lig_j)
    #fp2 = tancal.fingerprint(smiles_j)
    val = tancal.compareFormula(formula1,formula2) 
    #print val
    fileout.write("%s, mwdiff = %f, formula_diff = %f \n" %(line.strip('\n'), math.fabs(mw1 - mw2), val))
    fileout.flush()
fileout.close()
filein.close()



