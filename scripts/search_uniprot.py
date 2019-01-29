import sys,urllib,urllib2

## This script is writen by 
## Trent E Balius 
## this is a script to search Uniprot:
## this webpage was very helpfull.
## http://www.uniprot.org/faq/28

if ( len(sys.argv) != 2):
    print "needs a uniprot code"
    exit()

uniprot = sys.argv[1]
format  = 'txt'
print uniprot

##url = 'http://www.uniprot.org/uniparc/'
url = 'http://www.uniprot.org/uniprot/'
params = {
  'query':uniprot,
  'format':format
#  'format':'xls'
#  'format':'fasta'
}
#
data = urllib.urlencode(params)
request = urllib2.Request(url, data)
request.add_header('User-Agent', 'Python contact')

try:
  response = urllib2.urlopen(request)
except urllib2.HTTPError as e:
   print e.code, e.reason

code_desc = {}
code_desc[200] = "The request was processed successfully."
code_desc[400] = "Bad request. There is a problem with your input."
code_desc[404] = "Not found. The resource you requested doesn't exist."
code_desc[410] = "Gone. The resource you requested was removed."
code_desc[500] = "Internal server error. Most likely a temporary problem, but if the problem persists please contact us."
code_desc[503] = "Service not available. The server is being updated, try again later."

if response.code != 200:
   print response.code
   print code_desc[response.code]

page = response.read(200000)

#print page

if page == "":
   print "page is empty"
   

if "html" in page:
    print "Error: returned webpage: ",
    txt_url = 'http://www.uniprot.org/uniprot/' + uniprot +"."+ format
    webfile = urllib.urlopen(txt_url)
    page    = webfile.read()
    webfile.close()

#    exit()
#print page


lines = page.split('\n')
if format == 'xls':
   print len(lines) - 1

   splitline1 = lines[0].split('\t')

   for i in range(1,len(lines)-1):
      print "#######  line " + str(i) + "  #######" 
      splitline2 = lines[i].split('\t')
      if len(splitline1) != len(splitline2): 
         print "len(splitline1) != len(splitline2)"
         exit()
      for i in range(len(splitline1)):
         print splitline1[i]+":"+splitline2[i]

query = uniprot
if format == 'txt':
  discription = query
  for line in lines:
     #line = line.strip('\n')
     if "ID" == line[0:2]:
         genename = line.split()[1]
         discription = discription +", "+ genename
     if "GN" == line[0:2]:
        if "=" in line and "Name" in line:
           #print line
           discription = discription + " --- " + line.split('=')[1].split(';')[0] + " --- "+ line.split(';')[1].split('=')[1]
     if "DE" == line[0:2]:
        if "=" in line and "Name" in line:
           discription = discription + ", " + line.split('=')[1].replace(';','')
  print discription



