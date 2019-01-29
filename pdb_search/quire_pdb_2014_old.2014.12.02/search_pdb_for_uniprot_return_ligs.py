
## Trent Balius, Shoichet group, UCSF, 2014.08.08

## this script is bast on a script obtained from the PDB website
## http://www.rcsb.org/pdb/software/rest.do 

import sys
import urllib, urllib2
import scrape_pdb_for_uniprot as spfu
import scrape_pdb_for_lig as spfl
import scrape_zinc_zincid as szzi
import tanimoto_cal_axon as tancal

def query(queryText):
  print "query:\n", queryText
  print "querying PDB...\n"
  req = urllib2.Request(url, data=queryText)
  f = urllib2.urlopen(req)
  result = f.read()
  if result:
    print "Found number of PDB entries:", result.count('\n')
    #print "PDB entries:\n", result
  else:
    print "Failed to retrieve results"

  return result


url = 'http://www.rcsb.org/pdb/rest/search'

## This was run on the 2014/08/08. 
## Query Details: 
## Query 	Structures Found 	Conjunction 	Structures Displayed 	Search time (seconds)
## Ligand Search : Has free ligands=yes 	75217 	
## 	75217 	0.56
## Experimental Method is X-RAY 	90771 	and 	73100 	0.793
## Molecular Weight (Chemical component): Molecular weight min is 100 and Molecular weight max is 5000 	52743 	and 	51792 	2.894

# Benzene molecular weight == 78.11
# Zinc molecular weight ==  65.41 g/mol 

uniprot = sys.argv[1]

'''
  <orgPdbQuery>
    <version>head</version>
    <queryType>org.pdb.query.simple.AdvancedKeywordQuery</queryType>
    <description>Text Search for: p13053</description>
    <queryId>FFCBE86</queryId>
    <resultCount>45</resultCount>
    <runtimeStart>2014-09-05T17:17:21Z</runtimeStart>
    <runtimeMilliseconds>26</runtimeMilliseconds>
    <keywords>P13053</keywords>
  </orgPdbQuery>
'''

'''
  <orgPdbQuery>
    <version>head</version>
    <queryType>org.pdb.query.simple.AdvancedKeywordQuery</queryType>
    <description>Text Search for: Q9PTN2</description>
    <queryId>FC202821</queryId>
    <resultCount>42</resultCount>
    <runtimeStart>2014-09-05T16:34:47Z</runtimeStart>
    <runtimeMilliseconds>16</runtimeMilliseconds>
    <keywords>P11473</keywords>
  </orgPdbQuery>
'''

queryText = """
  <orgPdbQuery>
    <queryType>org.pdb.query.simple.AdvancedKeywordQuery</queryType>
    <keywords>"""+ uniprot + """</keywords>
  </orgPdbQuery>
"""


result1 = query(queryText)

#print result1

uniprot_dict   = {}
ucount = 0
pdb_dict       = {}
lig_dict       = {}
pcount =0 

#uniprot_to_pdb = []
pdb_to_uniprot = []
pdb_to_ligand = []


ligfilehandle = open(uniprot + '.ligandfile.txt','w')

pdbtolig_filehandle = open(uniprot +'.pdbtolig_file.txt','w')
pdbtouniprot_filehandle = open(uniprot + '.pdbtouniprot_file.txt','w')

#for pdb in result1.split('\n')[0:100]:
for pdb in result1.split('\n'):
   #print pdb

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

   not_a_ligand = []

   cofactors = ['HEM']
#   ATP NAP NAD ADP FAD
   not_a_ligand = not_a_ligand + cofactors
   #not_a_ligand.append(cofactors)

   #ions = ['AG','CL','CA','HG','IOD','K','ZN','MG','MN','NA','SO4','PO4']
   ions =  ["K","EU","OS","HO","AG","KR","LU","PD","RU","U1","Y1","PR","GD","MO","SM","TL","RB","PB","LI","AU","OH","YB","PT","CS","BA","NO","SR","XE","BR","CO","HG","CU","NI","CD","FE","MN","NA","CA","CL","ZN","MG", 'IOD', 'SO4','PO4',"FE2"]
   not_a_ligand = not_a_ligand + ions

   carbohydrates = ['A2G', 'BGC', 'BMA', 'FUC', 'GAL', 'GLA', 'GLC', 'MAN', 'NAG', 'NDG']
   not_a_ligand = not_a_ligand + carbohydrates
   #not_a_ligand.append(carbohydrates)

   unknown = ["UNX","UNL"]
   not_a_ligand = not_a_ligand + unknown
   #not_a_ligand.append(unknown)

   crystal_stuff = ["GOL","EDO","MPD","ACT","PEG","PGE","PG4","BME"]
   not_a_ligand = not_a_ligand + crystal_stuff

   #print not_a_ligand   
   # print lig_list

   for lig in lig_list: 
        #if lig in lig_dict: # if the ligand is already in the dictionary then dont looked up smile
        #   continue
        #if lig in ions: ## skip if any ion
        if lig in not_a_ligand: ## eg. skip if any ion
           #print lig, "in", not_a_ligand 
           continue
        ##if lig in cofactors:

        ##if not (lig in lig_dict) and not (lig in ions) : 
        if not (lig in lig_dict) : # if the ligand is already in the dictionary then dont looked up smile
           smiles = spfl.scrape_pdb_for_lig_smiles(lig)
           lig_dict[lig] = smiles

        entry = [pdb, lig]
        pdbtolig_filehandle.write("%s %s\n" % (pdb, lig))
        pdb_to_ligand.append(entry)

pdbtolig_filehandle.close()
pdbtouniprot_filehandle.close()        
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

for lig in lig_dict.keys():
    ligfilehandle.write("%s %s\n" % (lig_dict[lig], lig))
ligfilehandle.close()

exit()

