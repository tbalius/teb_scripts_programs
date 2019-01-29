#!/usr/bin/python2.6
## this script is bast on a script obtained from the PDB website
## http://www.rcsb.org/pdb/software/rest.do 

import sys, urllib, urllib2



def query(queryText,url):
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


def main():
  url = 'http://www.rcsb.org/pdb/rest/search'
#  queryText = """
#    <orgPdbQuery>
#    <version>head</version>
#    <queryType>org.pdb.query.simple.StructureKeywordsQuery</queryType>
#    <description>Structure Keyword Query: find pdb systems with Unknown Function </description>
#    <queryId>D9EF6548</queryId>
#    <resultCount>3145</resultCount>
#    <runtimeStart>2013-03-14T17:11:00Z</runtimeStart>
#    <runtimeMilliseconds>88</runtimeMilliseconds>
#    <struct_keywords.pdbx_keywords.comparator>contains</struct_keywords.pdbx_keywords.comparator>
#    <struct_keywords.pdbx_keywords.value>Unknown Function</struct_keywords.pdbx_keywords.value>
#  </orgPdbQuery>
#  """
#  result1 = query(queryText,url)
#  file = open('unknownfunction_from_pdb.txt','w')
#  file.write(result1)
#  file.close()

  
  #pdblist = result1.split('\n')  
  #pdblist = result2.split('\n')  

  #file = sys.argv[1]
  #filehand = open(file,'r')
  #pdblist = filehand.readlines()
#  print pdblist


  N = len(sys.argv)
  if N == 0: 
     print " search_pdb_uniprotid_name.py pdbcode1, pdbcode2, ... , pdbcode N "
     exit()
  print str(N-1) + " pdbcodes read in :" 

  pdblist = []
  for i in range(1,N):
      print sys.argv[i]
      pdblist.append(sys.argv[i])

  file = open('unknownfunction_xray_ligand_from_pdb_reduced.txt','w')

  for pdb in pdblist:
     pdb = pdb.strip('\n')
#     if pdb[0] == '#':
#        print 'header=' + pdb 
#        continue
     #print pdb
     pdburl = 'http://www.rcsb.org/pdb/files/'+pdb+'.pdb'
     print "url = " + pdburl 
     webFile = urllib.urlopen(pdburl)
     lines = webFile.read()
     #print lines.split('\n')[0]
     uniprot = {}
     flag_small_mol = False
     for line in lines.split('\n'):
         splitline = line.split()
         if (len(splitline) == 0):
             continue
#         if (splitline[0] == "EXPDTA"):
#            print line
         if (splitline[0] == "DBREF"):
            if (splitline[5] == "UNP"):
               #print line
               if not (splitline[6] in uniprot):
                  uniprot[splitline[6]] = splitline[7]
#                 #print splitline[6]
                  #print line
#         if (splitline[0] == "HET"):
#            print line
#            num = line[13:17]
#            name = line[7:10]
#            #print name
#            #print num
#            #if (int(splitline[3])> 10): 
#            if (int(num)> 10 and name != "MSE" ): 
#                flag_small_mol = True
#         if (splitline[0] == "HETNAM"):
#            print line
#         if (splitline[0] == "FORMUL"):
#            print line
    
#         if ("RESOLUTION" in line ): 
#            print line

     print pdb + " has "+ str(len(uniprot.keys())) + " Uniprot id : " 

#     if (flag_small_mol):
#         print pdb + " has small molecule"
#         file.write(pdb+'\n')
    
     for uniprotid in uniprot.keys(): 
        print uniprotid +" -- "+uniprot[uniprotid]
    
     webFile.close()
   #exit()

  file.close() ## close file
  exit()

main()
