
## Trent Balius, Shoichet group, UCSF, 2014.08.08

## this script is bast on a script obtained from the PDB website
## http://www.rcsb.org/pdb/software/rest.do 

import urllib, urllib2

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
## Query Details
## 
##
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


for pdb in result1.split('\n'):
   print pdb
#   pdburl = 'http://www.rcsb.org/pdb/files/'+pdb+'.pdb'
#   webFile = urllib.urlopen(pdburl)
#   lines = webFile.read()
#   uniprot = {}
#   for line in lines.split('\n'):
#       splitline = line.split()
#       if (len(splitline) == 0):
#           continue
#       if (splitline[0] == "EXPDTA"):
#          print line
#       if (splitline[0] == "DBREF"):
#          if (splitline[5] == "UNP"):
#             if not (splitline[6] in uniprot):
#                uniprot[splitline[6]] = 1
#                #print splitline[6]
#                print line
#       if (splitline[0] == "HET"):
#          print line
#       if (splitline[0] == "HETNAM"):
#          print line
#       if (splitline[0] == "FORMUL"):
#          print line
#
#       if ("RESOLUTION" in line ): 
#          print line
#
#   print pdb + " has "+ str(len(uniprot.keys())) + " Uniprot id : ", 
#
#   for uniprotid in uniprot.keys(): 
#      print uniprotid,
#   print ""
#   webFile.close()
   #exit()

exit()

