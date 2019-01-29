
## this script is bast on a script obtained from the PDB website
## http://www.rcsb.org/pdb/software/rest.do 

import sys, urllib, urllib2



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


def main():
  url = 'http://www.rcsb.org/pdb/rest/search'
  #result1 = query(queryText)
  #pdblist = result1.split('\n')  

  file = sys.argv[1]
  filehand = open(file,'r')
  pdblist = filehand.readlines()
#  print pdblist

  for pdb in pdblist:
     pdb = pdb.strip('\n')
     if pdb[0] == '#':
        print 'header=' + pdb 
        continue
     #print pdb
     pdburl = 'http://www.rcsb.org/pdb/files/'+pdb+'.pdb'
     print "url = " + pdburl 
     webFile = urllib.urlopen(pdburl)
     lines = webFile.read()
     #print lines.split('\n')[0]
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

main()
