
import sys
import requests


def search_pdb_web(pdbcode):
   url = 'http://www.rcsb.org/pdb/explore/explore.do?structureId='+pdbcode+'#'
   page=requests.get(url)
   if (page.status_code != 200):  #200 is okay, everything else is not
    print "there is a problem"
    print "page.status_code ==" + str(page.status_code)
    sys.exit()

   #print page.encoding #Gives you the encoding type
   page.encoding = 'utf-8'
   #print page.encoding #Gives you the encoding type

   page_text=page.text

   #f = open('temp.txt','w')
   #f.write(page_text)
   #f.close()

   splitpage=page_text.split('\n')
   Gene_flag = False
   Gene_string = ''
   Uniprot_string = ''

   for line in splitpage:
      if "Link to UniProtKB entry" in line:
         Uniprot_string = line.replace('>',' ').replace('<',' ').split()[14]
      if "Gene Names" in line:
         Gene_flag = True
      if Gene_flag:
         if not "<" in line:
            Gene_string = Gene_string +' '+ line.replace('\n','').replace(' ','').replace('\t','')
         if "</tr>" in line: 
            Gene_flag = False 

   print Uniprot_string + " " + Gene_string

if len(sys.argv) != 2:
    print "Error: one argument is needed"

pdbcode = sys.argv[1]
search_pdb_web(pdbcode)

