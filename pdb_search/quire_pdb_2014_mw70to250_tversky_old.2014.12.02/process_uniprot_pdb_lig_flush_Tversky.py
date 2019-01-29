
## Trent Balius, Shoichet group, UCSF, 2014.08.08


import urllib, urllib2
import scrape_pdb_for_uniprot as spfu
import scrape_pdb_for_lig as spfl
import scrape_zinc_zincid as szzi
import tanimoto_tversky_cal_axon as tancal

uniprot_dict   = {}
ucount = 0
pdb_dict       = {}
lig_dict       = {}
pcount =0 

pdb_to_uniprot = []
pdb_to_ligand = []

uniprot_to_ligands_dict = {}

#ligfilehandle = open('ligandfile.txt','w')

pdbtouniprot_filehandle = open('pdbtouniprot_file.txt','r')
pdbtolig_filehandle = open('pdbtolig_file.txt','r')

for line in pdbtouniprot_filehandle:
    splitline = line.split()
    uniprot = splitline[1]
    pdb = splitline[0]
    if not (uniprot in uniprot_dict):
        uniprot_dict[uniprot] = []
    uniprot_dict[uniprot].append(pdb)

#for pdb in result1.split('\n')[0:100]:
for line in pdbtolig_filehandle:
   splitline = line.split()
   pdb = splitline[0]
   lig = splitline[1]
   if not (pdb in pdb_dict):
      pdb_dict[pdb] = []
   pdb_dict[pdb].append(lig)

not_a_ligand = []

cofactors = ['HEM']
#   ATP NAP NAD ADP FAD
 
not_a_ligand = not_a_ligand + cofactors

#ions = ['AG','CL','CA','CD','CU1','PT','HG','IOD','K','ZN','MG','MN','NI','NA','SO4','PO4']
ions =  ["K","EU","OS","HO","AG","KR","LU","PD","RU","U1","Y1","PR","GD","MO","SM","TL","RB","PB","LI","AU","OH","YB","PT","CS","BA","NO","SR","XE","BR","CO","HG","CU","NI","CD","FE","MN","NA","CA","CL","ZN","MG", 'IOD', 'SO4','PO4']
not_a_ligand = not_a_ligand + ions

#carbohydrates = [ 'A2G' 'BGC' 'NAG', 'MAN','BMA', 'FUC',  'NDG']
carbohydrates = ['A2G', 'BGC', 'BMA', 'FUC', 'GAL', 'GLA', 'GLC', 'MAN', 'NAG', 'NDG']
not_a_ligand = not_a_ligand + carbohydrates

unknown = ["UNX","UNL"]
not_a_ligand = not_a_ligand + unknown

crystal_stuff = ["GOL","EDO","MPD","ACT","PEG","PGE","PG4","BME"]
not_a_ligand = not_a_ligand + crystal_stuff

#print not_a_ligand
#
#exit()

for uniprot in uniprot_dict.keys():
    print uniprot,

    if not ( uniprot in uniprot_to_ligands_dict):
       uniprot_to_ligands_dict[uniprot] = []
 
    for pdb in uniprot_dict[uniprot]:
        if not (pdb in pdb_dict):
           print " "
           continue
        for lig in pdb_dict[pdb]:
            #if (lig in ["UNX","UNL"]):
            if (lig in not_a_ligand):
                continue
            print lig,
            if not (lig in uniprot_to_ligands_dict[uniprot]): 
               uniprot_to_ligands_dict[uniprot].append(lig)
    print ' '

print " stuff that matters::::::::::"

fileout = open("uniprot_lig_tversky_flush.txt",'w')
fileout.write("This file will grow\n")
fileout.close()

lig_smiles = {}
lig_fp = {}

theshold = 0.6
max_MM = 250.0
#max_MM = 500.0

#fileout = open("uniprot_lig_tversky.txt",'w')
for uniprot in uniprot_to_ligands_dict.keys():
    fileout = open("uniprot_lig_tversky_flush.txt",'a')
    if (len(uniprot_to_ligands_dict[uniprot]) > 6):
       liglist = uniprot_to_ligands_dict[uniprot]
       print uniprot, uniprot_to_ligands_dict[uniprot] 
       # put to forloops, both over the ligands (do uppper diagonal), here and cal tverkys   
       for i in range(len(liglist)):
           lig_i = liglist[i]
           if (lig_i in lig_smiles):
               smiles_i = lig_smiles[lig_i]
               fp1      = lig_fp[lig_i]
           else:
               smiles_i = spfl.scrape_pdb_for_lig_smiles(lig_i)
               M = tancal.molecularMass(smiles_i)
               if float(M) > max_MM:
                   print lig_i, M 
                   continue
               #H = tancal.heavyAtoms(smiles_j)
               fp1 = tancal.fingerprint(smiles_i)
               lig_smiles[lig_i] = smiles_i
               lig_fp[lig_i] = fp1

           for j in range(i+1,len(liglist)):
               lig_j = liglist[j]
               if (lig_j in lig_smiles):
                   smiles_j = lig_smiles[lig_j]
                   fp2      = lig_fp[lig_j]
               else:
                   smiles_j = spfl.scrape_pdb_for_lig_smiles(lig_j)
                   M = tancal.molecularMass(smiles_j)
                   if float(M) > max_MM: 
                      continue
                   #H = tancal.heavyAtoms(smiles_j)
                   fp2 = tancal.fingerprint(smiles_j)
                   lig_smiles[lig_j] = smiles_j
                   lig_fp[lig_j] = fp2
               #smiles_j = spfl.scrape_pdb_for_lig_smiles(lig_j)
               #fp2 = tancal.fingerprint(smiles_j)
               tv = tancal.tversky_index(fp1,fp2,0.2,0.2) 
               print uniprot, " compare ", lig_i, lig_j, tv
               if (tv >= theshold):
                   fileout.write("%s, ligs: %s %s, tv = %f \n" %(uniprot, lig_i, lig_j, tv))
    fileout.close()
pdbtolig_filehandle.close()
pdbtouniprot_filehandle.close()        
exit()

