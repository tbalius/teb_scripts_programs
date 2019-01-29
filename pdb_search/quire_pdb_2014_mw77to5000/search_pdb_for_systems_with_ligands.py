
## Trent Balius, Shoichet group, UCSF, 2014.08.08

## this script is bast on a script obtained from the PDB website
## http://www.rcsb.org/pdb/software/rest.do 

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

queryText = """
<orgPdbCompositeQuery version="1.0">
    <resultCount>75217</resultCount>
    <queryId>C24B6356</queryId>
 <queryRefinement>
  <queryRefinementLevel>0</queryRefinementLevel>
  <orgPdbQuery>
    <version>head</version>
    <queryType>org.pdb.query.simple.NoLigandQuery</queryType>
    <description>Ligand Search : Has free ligands=yes</description>
    <queryId>7D79993D</queryId>
    <resultCount>75217</resultCount>
    <runtimeStart>2014-08-08T21:13:30Z</runtimeStart>
    <runtimeMilliseconds>560</runtimeMilliseconds>
    <haveLigands>yes</haveLigands>
  </orgPdbQuery>
 </queryRefinement>
 <queryRefinement>
  <queryRefinementLevel>1</queryRefinementLevel>
  <conjunctionType>and</conjunctionType>
  <orgPdbQuery>
    <version>head</version>
    <queryType>org.pdb.query.simple.ExpTypeQuery</queryType>
    <description>Experimental Method is X-RAY</description>
    <queryId>CB5A2C3F</queryId>
    <resultCount>90771</resultCount>
    <runtimeStart>2014-08-08T21:13:31Z</runtimeStart>
    <runtimeMilliseconds>793</runtimeMilliseconds>
    <mvStructure.expMethod.value>X-RAY</mvStructure.expMethod.value>
  </orgPdbQuery>
 </queryRefinement>
 <queryRefinement>
  <queryRefinementLevel>2</queryRefinementLevel>
  <conjunctionType>and</conjunctionType>
  <orgPdbQuery>
    <version>head</version>
    <queryType>org.pdb.query.simple.ChemFormulaWeightQuery</queryType>
    <description>Molecular Weight (Chemical component): Molecular weight min is 100 and Molecular weight max is 5000</description>
    <queryId>DA2CC690</queryId>
    <resultCount>52743</resultCount>
    <runtimeStart>2014-08-08T21:13:32Z</runtimeStart>
    <runtimeMilliseconds>2894</runtimeMilliseconds>
    <molecularWeightComparator>between</molecularWeightComparator>
    <molecularWeightMin>77</molecularWeightMin>
    <molecularWeightMax>5000</molecularWeightMax>
  </orgPdbQuery>
 </queryRefinement>
</orgPdbCompositeQuery>
"""


result1 = query(queryText)

uniprot_dict   = {}
ucount = 0
pdb_dict       = {}
lig_dict       = {}
pcount =0 

#uniprot_to_pdb = []
pdb_to_uniprot = []
pdb_to_ligand = []


ligfilehandle = open('ligandfile.txt','w')

pdbtolig_filehandle = open('pdbtolig_file.txt','w')
pdbtouniprot_filehandle = open('pdbtouniprot_file.txt','w')

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
   not_a_ligand.append(cofactors)

   ions = ['AG','CL','CA','HG','IOD','K','ZN','MG','MN','NA','SO4','PO4']
   not_a_ligand.append(ions)

   #carbohydrates = [ 'A2G' 'BGC' 'NAG', 'MAN','BMA', 'FUC',  'NDG']
   carbohydrates = ['A2G', 'BGC', 'BMA', 'FUC', 'GAL', 'GLA', 'GLC', 'MAN', 'NAG', 'NDG']
   not_a_ligand.append(carbohydrates)

   unknown = ["UNX","UNL"]
   not_a_ligand.append(unknown)

   # print lig_list

   for lig in lig_list: 
        #if lig in lig_dict: # if the ligand is already in the dictionary then dont looked up smile
        #   continue
        #if lig in ions: ## skip if any ion
        if lig in not_a_ligand: ## eg. skip if any ion
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

#ligfilehandle = open('ligandfile.txt','w')
#for lig in lig_dict.keys():
#    zincid_list = szzi.scrape_zinc_zincid(lig_dict[lig], 0.99)
#    ligfilehandle.write("%s, %s :: " % (lig, lig_dict[lig]))
#    for zincid in zincid_list:
#        ligfilehandle.write("%s " % zincid)
#    fp = tancal.fingerprint(lig_dict[lig])
#    ligfilehandle.write(":: %s" % str(fp) )
#    ligfilehandle.write("\n")
#ligfilehandle.close()

exit()

