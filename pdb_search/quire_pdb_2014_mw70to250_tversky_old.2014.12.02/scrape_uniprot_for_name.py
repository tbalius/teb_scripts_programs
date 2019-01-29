import sys,urllib,urllib2

## This script is writen by 
## Trent E Balius 
## this is a script to search Uniprot:
## this webpage was very helpfull.
## http://www.uniprot.org/faq/28

def get_query(query):
   #print query,
   discription = ""
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
      return
   
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
      return
   
   page = response.read(200000)
   #if "html" in page:
   #    print "Error: returned webpage: "
   #    return
   if "html" in page:
       print ": Error: returned webpage: ",
       txt_url = 'http://www.uniprot.org/uniprot/' + query +"."+ format
       webfile = urllib.urlopen(txt_url)
       page    = webfile.read()
       webfile.close()

   if page == "":
      print ", page is empty: uniprot is likely removed"
      return
   
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
      #discription = ''
      for line in lines:
         #line = line.strip('\n')
         if "ID" == line[0:2]:
             genename = line.split()[1]
             discription_list.append(genename)
             #discription = discription +", "+ genename
         if "DE" == line[0:2]:
            if "=" in line and "Name" in line:
               #discription = discription + "---" + line.split('=')[1].replace(';','')
               #discription = discription + ", " + line.split('=')[1].replace(';','')
               de = line.split('=')[1].replace(';','')
               discription_list.append(de)
         if "GN" == line[0:2]:
            if "=" in line and "Name" in line:
               #discription = discription + "---" + line.split('=')[1].split(';')[0].replace(',',"---") 
               gn = line.split('=')[1].split(';')[0].replace(',','')
               discription_list.append(gn)
               if (len(line.split(';'))> 1 and len(line.split(';')[1].split('='))>1):
                  #if (line.split(';')[1].split('=')[0] == " Synonyms"): 
                  #print line
                  gn2 = line.split(';')[1].split('=')[1].replace(',','')
                  discription_list.append(gn2)
               #   discription = discription + " --- "+ line.split(';')[1].split('=')[1].replace(',',"---")
      #print discription
      
      discription = ""
      flag_frist = True
      for disc in discription_list:

           if not flag_frist: 
              discription = discription + ', '
           else: 
              flag_frist=False

           discription = discription + disc


   return discription 


#query = sys.argv[1]
#
#d = get_query(query)
#print d
#if ( len(sys.argv) != 2):
#    print "needs a uniprot code file list"
#    exit()

#filename = sys.argv[1]
#
#fh = open(filename,'r')
#lines = fh.readlines()
#fh.close()
#
#for line in lines:
#  query = line.replace('\n','').replace(' ','')
#  #print query
#  get_query(query)
#exit()

