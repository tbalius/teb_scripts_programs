
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
liglist = sys.argv[2].split(';')

dic_id_to_tile   = {}
dic_id_lig_count = {}
dic_id_lig_list = {}

for lig in liglist:
   if lig == '':
      continue
   search = uniprot+" "+lig
   #search = "O00206 FUL"
   print search   
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
      if not (id in dic_id_to_tile):
          dic_id_to_tile[id] = title
      if not (id in dic_id_lig_count):
          dic_id_lig_count[id] = 1
          dic_id_lig_list[id]  = []
          dic_id_lig_list[id].append(lig)
      else:
          #print id, pdb, lig
          if not (lig in dic_id_lig_list[id]):
             dic_id_lig_count[id] = dic_id_lig_count[id] + 1
             dic_id_lig_list[id].append(lig)
          #else: 
          #   print id, lig, "all ready there"
      #print "pdb=%s; title=%s; pubmedid=%s\n" % (pdb, title, id)
      #print "pdb=%s;title=%s;pubmedid=%s;  " % (pdb, title, id)

citation   = ''
max_number = 0
for id in dic_id_to_tile.keys():
    print id,dic_id_to_tile[id],dic_id_lig_count[id]
    if dic_id_to_tile[id] == "No Primary Citation for this Structure":
       continue 
    if dic_id_lig_count[id] > max_number:
       max_number = dic_id_lig_count[id]
       citation = dic_id_to_tile[id]
print '## max--' + str(max_number) + '--' + citation
 
exit()

