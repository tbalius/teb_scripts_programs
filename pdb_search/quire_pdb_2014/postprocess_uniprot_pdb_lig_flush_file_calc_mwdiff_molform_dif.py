
## Trent Balius, Shoichet group, UCSF, 2014.08.08


import urllib, urllib2, math
import scrape_pdb_for_uniprot as spfu
import scrape_pdb_for_lig_mod as spfl
import scrape_zinc_zincid as szzi
import tanimoto_cal_axon as tancal


print " stuff that matters::::::::::"

filein = open("uniprot_lig_tanamoto_flush.txt",'r')
fileout = open("uniprot_lig_tanamoto_mwdiff_formula_diff_new.txt",'w')

lig_smiles  = {}
lig_formula = {}
lig_mw = {}

# readin the smiles from a file
filein2 = open("all.smi",'r')
for line in filein2:
    splitline = line.split()
    lig = splitline[1]
    smiles = splitline[0]
    if (lig in lig_smiles):
       print "duplicate ligand: "+ line 
       continue
    lig_smiles[lig] = smiles

filein2.close()

# readin molecular formula 

filein3 = open("all.mf.txt",'r')
for line in filein3:
    splitline = line.split()
    lig = splitline[1]
    formula = splitline[0]
    #print lig, formula
    if (lig in lig_formula):
       print "duplicate ligand: "+ line
       continue
    lig_formula[lig] = formula
    print lig, formula

filein3.close()


fileout2 = open("all.smi",'a') # append new ligands/smiles to file
fileout3 = open("all.mf.txt",'a') # append new ligands/smiles to file

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

    # for ligand1
    # cheek if smiles is in dictionary has already be gotten
    if (lig1 in lig_smiles):
        smiles1  = lig_smiles[lig1]
    else: # if not know then get it. 
        smiles1 = spfl.scrape_pdb_for_lig_smiles(lig1)
        if (smiles1 == ''):
             continue 
        lig_smiles[lig1] = smiles1
        fileout2.write(smiles1+' '+lig1+'\n')

    if (lig1 in lig_formula):
        formula1 = lig_formula[lig1]
    else:
        formula1 = tancal.MolecularFormula(smiles1)
        lig_formula[lig1]=formula1 
        fileout3.write(formula1+' '+lig1+'\n')

    if (lig1 in lig_mw):
        mw1 = lig_mw[lig1]
    else:
        mw1 = float(tancal.molecularMass(smiles1))
        lig_mw[lig1] = mw1


    # for ligand2
    if (lig2 in lig_smiles):
        smiles2  = lig_smiles[lig2]
    else:
        smiles2 = spfl.scrape_pdb_for_lig_smiles(lig2)
        if (smiles2 == ''):
            continue 
        lig_smiles[lig2] = smiles2
        #fileout2.write(lig2+' '+smiles2+'\n')
        fileout2.write(smiles2+' '+lig2+'\n')

    if (lig2 in lig_formula):
        formula2 = lig_formula[lig2]
    else:
        formula2 = tancal.MolecularFormula(smiles2)
        lig_formula[lig2] = formula2
        fileout3.write(formula2+' '+lig2+'\n')

    if (lig2 in lig_mw):
        mw2 = lig_mw[lig2]
    else:
        mw2 = float(tancal.molecularMass(smiles2))
        lig_mw[lig2] = mw2

    #smiles_j = spfl.scrape_pdb_for_lig_smiles(lig_j)
    #fp2 = tancal.fingerprint(smiles_j)
    #val = tancal.compareFormula(formula1,formula2) 
    val, val2 = tancal.compareFormula_heavy(formula1,formula2) 
    #print val
    fileout.write("%s, mwdiff = %f, formula_diff = %f, formula_diff_heavy = %f \n" %(line.strip('\n'), math.fabs(mw1 - mw2), val, val2))
    fileout.flush()
fileout.close()
fileout2.close()
fileout3.close()
filein.close()



