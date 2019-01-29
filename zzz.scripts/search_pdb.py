
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

##queryText = 
#<?xml version="1.0" encoding="UTF-8"?>
#<orgPdbQuery>
#<version>B0907</version>
#<queryType>org.pdb.query.simple.ExpTypeQuery</queryType>
#<description>Experimental Method Search : Experimental Method=SOLID-STATE NMR</description>
#<mvStructure.expMethod.value>SOLID-STATE NMR</mvStructure.expMethod.value>
#</orgPdbQuery>
#"""


#queryText = """
#<orgPdbQuery>    
#    <queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>
#    <description>Simple query for a list of UniprotKB Accession IDs: P50225</description>   
#    <accessionIdList>P50225</accessionIdList>
#</orgPdbQuery>
#"""

#result0 = query(queryText)
#
#print result0 

##queryText = """
#<?xml version="1.0" encoding="UTF-8"?>
#
#<orgPdbQuery>
# <version>B0905</version>
# <queryType>org.pdb.query.simple.OrganismQuery</queryType>
# <description>Organism Search : Organism Name=$organism_name </description>
#
# <organismName>%s</organismName>
#</orgPdbQuery>
#""" % 'human'
#""" % 'nipah'

#queryText = """
#<orgPdbQuery>
#  <queryType>org.pdb.query.simple.ReleaseDateQuery</queryType>
#    <database_PDB_rev.date.comparator>between</database_PDB_rev.date.comparator>
#    <database_PDB_rev.date.min>2012-12-30</database_PDB_rev.date.min>
#    <database_PDB_rev.date.max>2013-12-30</database_PDB_rev.date.max>
#    <database_PDB_rev.mod_type.value>1</database_PDB_rev.mod_type.value>
#</orgPdbQuery>
#"""

queryText = """
<orgPdbCompositeQuery version="1.0">
    <resultCount>78278</resultCount>
    <queryId>429417E1</queryId>
 <queryRefinement>
  <queryRefinementLevel>0</queryRefinementLevel>
  <orgPdbQuery>
    <version>head</version>
    <queryType>org.pdb.query.simple.ExpTypeQuery</queryType>
    <description>Experimental Method is X-RAY</description>
    <queryId>BEB0A0D6</queryId>
    <resultCount>78278</resultCount>
    <runtimeStart>2013-03-13T18:05:50Z</runtimeStart>
    <runtimeMilliseconds>849</runtimeMilliseconds>
    <mvStructure.expMethod.value>X-RAY</mvStructure.expMethod.value>
  </orgPdbQuery>
 </queryRefinement>
 <queryRefinement>
  <queryRefinementLevel>1</queryRefinementLevel>
  <conjunctionType>and</conjunctionType>
  <orgPdbQuery>
    <version>head</version>
    <queryType>org.pdb.query.simple.ReleaseDateQuery</queryType>
    <description>Released between 2013-01-01 and 2013-03-13 </description>
    <queryId>DCBDDDB6</queryId>
    <resultCount>1784</resultCount>
    <runtimeStart>2013-03-13T18:05:51Z</runtimeStart>
    <runtimeMilliseconds>57</runtimeMilliseconds>
    <database_PDB_rev.date.comparator>between</database_PDB_rev.date.comparator>
    <database_PDB_rev.date.min>2013-01-01</database_PDB_rev.date.min>
    <database_PDB_rev.date.max>2013-03-13</database_PDB_rev.date.max>
    <database_PDB_rev.mod_type.comparator><![CDATA[<]]></database_PDB_rev.mod_type.comparator>
    <database_PDB_rev.mod_type.value>1</database_PDB_rev.mod_type.value>
  </orgPdbQuery>
 </queryRefinement>
</orgPdbCompositeQuery>
"""


result1 = query(queryText)


for pdb in result1.split('\n'):
   print pdb
   pdburl = 'http://www.rcsb.org/pdb/files/'+pdb+'.pdb'
   webFile = urllib.urlopen(pdburl)
   lines = webFile.read()
   uniprot = {}
   for line in lines.split('\n'):
       splitline = line.split()
       if (len(splitline) == 0):
           continue
       if (splitline[0] == "EXPDTA"):
          print line
       if (splitline[0] == "DBREF"):
          if (splitline[5] == "UNP"):
             if not (splitline[6] in uniprot):
                uniprot[splitline[6]] = 1
                #print splitline[6]
                print line
       if (splitline[0] == "HET"):
          print line
       if (splitline[0] == "HETNAM"):
          print line
       if (splitline[0] == "FORMUL"):
          print line

       if ("RESOLUTION" in line ): 
          print line

   print pdb + " has "+ str(len(uniprot.keys())) + " Uniprot id : ", 

   for uniprotid in uniprot.keys(): 
      print uniprotid,
   print ""
   webFile.close()
   #exit()

exit()

