
## this script is bast on a script obtained from the PDB website
## http://www.rcsb.org/pdb/software/rest.do 
## this script will loop over a list of pdb and retrun the number of uniports asosiated with each. 

## I want to report two things here:
## (1) number of pdb with 1, 2, 3, etc. unprot codes. 
## (2) number of uniprot codes in the list  
## I will try and explain better

import sys, urllib, urllib2

def main():
  url = 'http://www.rcsb.org/pdb/rest/search'
  #file = open('unknownfunction_xray_ligand_from_pdb.txt','w')
  #file.write(result2)
  #file.close()

  file = sys.argv[1]

  fileh = open(file)
  pdblist = fileh.readlines()
  fileh.close() ## close file

  #print pdblist

  uniprot_all = {}
  pdb_uniprot_num = {} ## keeps track of the number of pdbs with 1,2,3 uniprot codes. 

  fileh1 = open("/raid1/people/tbalius/public_html/data/withOneUniprot.txt",'w')
  fileh2 = open("/raid1/people/tbalius/public_html/data/withNoUniprot.txt",'w')

  for pdb in pdblist:
     pdb = pdb.strip('\n')

     #print pdb

     if len(pdb) != 4: 
        print "Error: "+ file + "contains weird pdb: " + pdb 

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
         if (splitline[0] == "DBREF"):
            if (splitline[5] == "UNP"):
               ## this is for the current pdb
               if not (splitline[6] in uniprot):
                  uniprot[splitline[6]] = 1
                  #print splitline[6]
                  #print line
               ## over the whole list of pdb
               if not (splitline[6] in uniprot_all):
                  uniprot_all[splitline[6]] = 1
               else: 
                  uniprot_all[splitline[6]] = uniprot_all[splitline[6]] + 1
              
     
     numOfUniprot = str(len(uniprot.keys()))
     print pdb + " has "+ numOfUniprot + " Uniprot id : ", 

     if not (numOfUniprot in pdb_uniprot_num):
        pdb_uniprot_num[numOfUniprot] = 1
     else:
        pdb_uniprot_num[numOfUniprot] = pdb_uniprot_num[numOfUniprot] + 1

     for uniprotid in uniprot.keys(): 
        print uniprotid,
     print ""

     ## print pdb to file if uniprot = 1
     if (numOfUniprot == '1'):
         print "writing "+ pdb + " to file "
         fileh1.write( pdb + ' \n')
     
     ## print pdb to file if uniprot = 0
     if (numOfUniprot == '0'):
         print "writing "+ pdb + " to file "
         fileh2.write( pdb + '  \n')

     webFile.close()
   #exit()
  fileh1.close()
  fileh2.close()

  print "\nHow meny pdbs have a certain number of uniprots?\n"
  print "# uniprots, # pdb with uniprot quantity"

  htmltext = """
HTML :   <hr width="100%">
HTML :   <table width="800" border="1">
HTML :   <tr>
HTML :    <td> <h3> # uniprots </h3> </td> 
HTML :    <td> <h3> # pdb with uniprot quantity </h3> </td> 
HTML :   </tr>
  """

  keyslist = pdb_uniprot_num.keys()
  #print keyslist
  keyslist.sort()
  for key in keyslist: 
     print key, pdb_uniprot_num[key]
     htmltext = htmltext + "\nHTML :   <tr> \nHTML :    <td> " + str(key) + " </td> \n"
     if key == "0":
        htmltext = htmltext + "HTML :    <td> <a href=\"data/withNoUniprot.txt\"> " + str(pdb_uniprot_num[key]) + "  </a> </td> \nHTML :    </tr> \n"
     elif key == "1":
        htmltext = htmltext + "HTML :    <td> <a href=\"data/withOneUniprot.txt\"> " + str(pdb_uniprot_num[key]) + "  </a> </td> \nHTML :    </tr> \n"
     else:
        htmltext = htmltext + "HTML :    <td> " + str(pdb_uniprot_num[key]) + " </td> \nHTML :    </tr> \n"

  print ""
  print htmltext

  print "\n How meny uniprot codes: \n"
  print len(uniprot_all.keys())

  exit()

main()
