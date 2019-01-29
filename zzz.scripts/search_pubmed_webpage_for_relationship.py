import sys,urllib,urllib2

## This script is writen by 
## Trent E Balius 
## 2013/11/01
## this is a script to search Pubmed:
## this webpage was very helpfull.
## http://www.uniprot.org/faq/28

################################################################
## readable by a human,                                       ##
## I search uniprot with a genename and return stuff          ##
## that is more understadable by pubmed or a human.           ##
################################################################
def get_query_uniprot(query):
   print query
   url = 'http://www.uniprot.org/uniprot/'
   format = 'txt'
   params = {
     'query':query,
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
      return query
   
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
      return query
   
   page = response.read(200000)
   if "html" in page:
       print ": Error: returned webpage: "
       txt_url = 'http://www.uniprot.org/uniprot/' + query +"."+ format
       webfile = urllib.urlopen(txt_url)
       page    = webfile.read()
       webfile.close()

   if page == "":
      print ", page is empty: uniprot is likely removed"
      return query
   
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
          entry        = ''
          entry_name   = ''
          protein_name = ''
          for i in range(len(splitline1)):
            #print splitline1[i]+":"+splitline2[i]
            if (splitline1[i] == "Entry"): 
                entry = splitline2[i]
            elif (splitline1[i] == "Entry name"): 
                entry_name = splitline2[i]
            elif (splitline1[i] == "Protein names"): 
                protein_name = splitline2[i]
          print entry+", "+entry_name+", "+ protein_name
   if format == 'txt':
      #discription = query
      discription_list = []
      for line in lines:
         #line = line.strip('\n')
         if "ID" == line[0:2]:
             genename = line.split()[1]
             discription_list = discription_list + [ genename ]
         if "DE" == line[0:2]:
            if "=" in line and "Name" in line:
               discription_list =  discription_list + line.split('=')[1].split(';')
         if "GN" == line[0:2]:
            if "=" in line and "Name" in line:
               discription_list = discription_list + line.split('=')[1].split(';')[0].split(',') 
               if (len(line.split(';'))> 1 and len(line.split(';')[1].split('='))>1):
                  discription_list = discription_list + line.split(';')[1].split('=')[1].split(',')
      discription = ''
      count = 0 
      for discrip in discription_list:
          if len(discrip) < 3: ## this will get-rid-of blake entrees and small names like NA for Neuraminidase 
             continue
          #if count == 0: # the frist 
          if discription == '':
              discription = discription + '" ' + discrip + ' " [Title/Abstract] '
          else: 
             discription = discription +' OR " ' + discrip + ' " [Title/Abstract] '
          #count = count + 1
      print discription

   return discription


def get_query_pubmed(query):
   print query
   url = 'http://www.ncbi.nlm.nih.gov/pubmed'
   #format = 'txt'
   params = {
     'db':'pubmed',
     'term':query,
   #  'format':format
   #  'format':'xls'
   #  'format':'fasta'
   }
   #
   data = urllib.urlencode(params)
   request = urllib2.Request(url, data)
   request.add_header('User-Agent', 'Python contact')
   
   string = ''
   try:
     response = urllib2.urlopen(request)
   except urllib2.HTTPError as e:
      print e.code, e.reason
      exit()
      #return string
   
   page = response.read(200000)
#   if "html" in page:
#       print "Error: returned webpage: "
#       exit()
       #return string
   flag = False
   for line in page.split('\n'):
       #print line
       if "Results:" in line:
          print line
          for ele in line.replace('<','*').replace('>','*').split('*'):
             if "Results:" in ele:
                print ele

                N = len(ele.split())
                #if (N != 2) or (N != 5) :
                #   print " some thing strange is hapening"
                print ele.split()[N-1]
                flag = True
                string = string + ele.split()[N-1] # append string
   if not (flag):
      print "No results"
   return string
   
def run_quiry(query1,query2):
   human_name1 = get_query_uniprot(query1) # readable by a human,  I search uniprot with a genename and return stuff that is more understadable by pubmed or a human.
   human_name2 = get_query_uniprot(query2)
   query = '('+human_name1+')  AND ('+ human_name2+')'
   return get_query_pubmed(query)

if not (len(sys.argv) == 3 or len(sys.argv) == 4):
    print "syntex:"
    print "python ~/zzz.scripts/search_pubmed_webpage_for_relationship.py -q AAKG1_HUMAN MK14_HUMAN"
    print "python ~/zzz.scripts/search_pubmed_webpage_for_relationship.py -f file"
    print "file syntex: "
    print "query1,query2" 

    exit()

fouth = open('output','w')

flag   = sys.argv[1]

if flag == "-q":
   query1 = sys.argv[2]
   query2 = sys.argv[3]
   result = run_quiry(query1,query2)
   fouth.write('%s,%s,%s\n'%(query1,query2,result))
elif (flag == "-f"):
   filename = sys.argv[2]
   fh = open(filename,'r')
   lines = fh.readlines()
   fh.close()
   for line in lines:
       print line 
       splitline = line.split(',')
       splitline2 = splitline[0].split('---')
       query1 = splitline2[0]
       query2 = splitline2[1]
       result = run_quiry(query1,query2)
       fouth.write('%s,%s,%s\n'%(query1,query2,result))

fouth.close()

exit()

