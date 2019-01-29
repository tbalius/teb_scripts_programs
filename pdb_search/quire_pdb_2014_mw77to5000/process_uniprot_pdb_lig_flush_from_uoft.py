
## Trent Balius, Shoichet group, UCSF, 2014.08.08


import urllib, urllib2
import scrape_pdb_for_uniprot as spfu
import scrape_pdb_for_lig as spfl
import scrape_zinc_zincid as szzi
import tanimoto_cal_axon as tancal

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


for uniprot in uniprot_dict.keys():
    print uniprot,

    if not ( uniprot in uniprot_to_ligands_dict):
       uniprot_to_ligands_dict[uniprot] = []
 
    for pdb in uniprot_dict[uniprot]:
        if not (pdb in pdb_dict):
           print " "
           continue
        for lig in pdb_dict[pdb]:
            print lig,
            if (lig in ["UNX","UNL"]):
               continue
            if not (lig in uniprot_to_ligands_dict[uniprot]): 
               uniprot_to_ligands_dict[uniprot].append(lig)
    print ' '

print " stuff the matters::::::::::"

fileout = open("uniprot_lig_tanamoto_flush.txt",'w')
fileout.write("This file will grow\n")
fileout.close()

theshold = 0.6
for uniprot in uniprot_to_ligands_dict.keys():
    fileout = open("uniprot_lig_tanamoto_flush.txt",'a')
    if (len(uniprot_to_ligands_dict[uniprot]) > 6):
       liglist = uniprot_to_ligands_dict[uniprot]
       print uniprot, uniprot_to_ligands_dict[uniprot] 
       # put to forloops, both over the ligands (do uppper diagonal), here and cal tanamotos   
       for i in range(len(liglist)):
           lig_i = liglist[i]
           smiles_i = spfl.scrape_pdb_for_lig_smiles(lig_i)
           fp1 = tancal.fingerprint(smiles_i)
           for j in range(i+1,len(liglist)):
               lig_j = liglist[j]
               smiles_j = spfl.scrape_pdb_for_lig_smiles(lig_j)
               fp2 = tancal.fingerprint(smiles_j)
               tc = tancal.tanimoto(fp1,fp2) 
               print uniprot, " compare ", lig_i, lig_j, tc
               if (tc >= theshold):
                   fileout.write("%s, ligs: %s %s, tc = %f \n" %(uniprot, lig_i, lig_j, tc))
    fileout.close()
'''
   if pdb in pdb_dict: 
      print pdb + " is already in list"  
      continue
   pdb_dict[pdb] = pcount
   pcount = pcount + 1

   count, unprot_list = spfu.scrap_pdb_for_uniprot(pdb) 
   for id in unprot_list:
       #if id in uniprot_dict: 
       #   continue
       if not (id in uniprot_dict): 
          uniprot_dict[id] = ucount
          ucount = ucount + 1 
       
       entry = [pdb, id] 
       pdbtouniprot_filehandle.write("%s %s\n" % (pdb, id))
       pdb_to_uniprot.append(entry)

   count, lig_list = spfl.scrape_pdb_for_lig(pdb) 

   ions = ['CL','HG','ZN','MG','MN','NA','SO4','PO4']

   for lig in lig_list: 
        #if lig in lig_dict: # if the ligand is already in the dictionary then dont looked up smile
        #   continue
        if lig in ions: ## skip if any ion
           continue
        ##if lig in cofactors:

        #if not (lig in lig_dict) and not (lig in ions) : 
        if not (lig in lig_dict) : # if the ligand is already in the dictionary then dont looked up smile
           smiles = spfl.scrape_pdb_for_lig_smiles(lig)
           # consider adding molelcular weight is to low skip
           lig_dict[lig] = smiles

        entry = [pdb, lig]
        pdbtolig_filehandle.write("%s %s\n" % (pdb, lig))
        pdb_to_ligand.append(entry)
'''
pdbtolig_filehandle.close()
pdbtouniprot_filehandle.close()        
'''
   #for lig in unprot_list:

## Write out information to files
## consider creating a ProgreSQP to store this information. 

unifilehandle = open('uniprotfile.txt','w')
for id in uniprot_dict.keys():
    unifilehandle.write("%s\n" % id)
unifilehandle.close()

pdbfilehandle = open('pdbprotfile.txt','w')
for id in pdb_dict.keys():
    pdbfilehandle.write("%s\n" % id)
pdbfilehandle.close()

ligfilehandle = open('ligandfile.txt','w')
for lig in lig_dict.keys():
    zincid_list = szzi.scrape_zinc_zincid(lig_dict[lig], 0.99)
    ligfilehandle.write("%s, %s :: " % (lig, lig_dict[lig]))
    for zincid in zincid_list:
        ligfilehandle.write("%s " % zincid)
    fp = tancal.fingerprint(lig_dict[lig])
    ligfilehandle.write(":: %s" % str(fp) )
    ligfilehandle.write("\n")
ligfilehandle.close()
'''
exit()

