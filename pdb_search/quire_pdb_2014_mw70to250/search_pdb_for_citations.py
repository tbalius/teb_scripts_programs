
## Trent Balius, Shoichet group, UCSF, 2014.08.08

## this script is bast on a script obtained from the PDB website
## http://www.rcsb.org/pdb/software/rest.do 

import urllib, urllib2, sys
import scrape_pdb_for_Citations as spfC
#import scrape_pdb_for_uniprot as spfu
#import scrape_pdb_for_lig as spfl
#import scrape_zinc_zincid as szzi
#import tanimoto_cal_axon as tancal

def query(queryText):
#  print "query:\n", queryText
#  print "querying PDB...\n"
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

uniprot = sys.argv[1]
lig = sys.argv[2]
search = uniprot+" "+lig
#search = "O00206 FUL"

queryText = """
  <orgPdbQuery>
    <version>head</version>
    <queryType>org.pdb.query.simple.AdvancedKeywordQuery</queryType>
    <description>Text Search for: o00206 ful</description>
    <keywords>""" + search + """</keywords>
  </orgPdbQuery>
"""
result1 = query(queryText)

#for pdb in result1:
for pdb in result1.split('\n'):
   if pdb == '': continue
   #count, unprot_list = spfu.scrap_pdb_for_uniprot(pdb) 
   title, id = spfC.scrap_pdb_for_Citations(pdb) 
   #print "pdb=%s; title=%s; pubmedid=%s\n" % (pdb, title, id)
   print "pdb=%s;title=%s;pubmedid=%s;  " % (pdb, title, id)

exit()

