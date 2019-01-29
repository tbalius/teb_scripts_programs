
import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print "Error: one argument is needed"

pdbcode = sys.argv[1]

url = 'http://www.rcsb.org/pdb/explore/explore.do?structureId='+pdbcode+'#'

page=requests.get(url)
if (page.status_code != 200):  #200 is okay, everything else is not
    print "there is a problem"
    print "page.status_code ==" + str(page.status_code)
    sys.exit()

print page.encoding #Gives you the encoding type
page.encoding = 'utf-8'
print page.encoding #Gives you the encoding type

page_text=page.text

f = open('temp.txt','w')
f.write(page_text)
f.close()

splitpage=page_text.split('\n')
#splitpage=page_text.split(':')
Gene_flag = False
Gene_string = ''
Uniprot_string = ''

for line in splitpage:
   if "Link to UniProtKB entry" in line:
#      print line.replace('>',' ').replace('<',' ')
#      print line.replace('>',' ').replace('<',' ').split()[14]
      Uniprot_string = line.replace('>',' ').replace('<',' ').split()[14]
   if "Gene Names" in line:
      Gene_flag = True
   if Gene_flag:
      if not "<" in line:
#         print line
         Gene_string = Gene_string +' '+ line.replace('\n','').replace(' ','').replace('\t','')
      if "</tr>" in line: 
         Gene_flag = False 

print Uniprot_string + " " + Gene_string

soup = BeautifulSoup(page_text.replace('\n',''))
#soup = BeautifulSoup(page_text.replace('\n','').replace('\xa0','?'))
#print list(soup.prettify())

#text = soup.get_text()
#f = open('temp2.txt','w')
#f.write(text)
#f.close()

#print text.encode('utf-8')

#
i=0
for tag in soup.find_all(True):
    print i 
    print(tag)
    i = i + 1
#print soup.title.name
#
##soup.prettify()
#
##f.write(str(soup))
#
#
##print soup
#
##soup.find_all('b')
#
#print "\n\n############\n\n"


##print soup.find_all("b")
#
##print soup.find_all(class_="Uniprot")
#soup2 = soup.find_all('a',class_="se_searchLink tooltip")
##soup2 = soup.find_all('Uniprot')
#
##for s in soup2:
#   print list(s)
#   print s

