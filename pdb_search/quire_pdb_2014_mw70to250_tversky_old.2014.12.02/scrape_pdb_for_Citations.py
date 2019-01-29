
## This script is writen by
## Trent E Balius
## 2014/02 
################################################################
## This module   
## scrapes the pdb webpage for uniprot.  
## This is modifed from ~/zzz.scripts/search_pdb_lig_code.py. 
################################################################


import sys,urllib,urllib2

def scrap_pdb_for_Citations(pdbcode):
  #url = 'http://zinc.docking.org/results/structure?structure.smiles='+smiles+'&structure.similarity=' + similarity
  #url = 'http://www.rcsb.org/pdb/explore/explore.do?structureId=' + pdbcode
  #url = "http://www.rcsb.org/pdb/explore/literature.do?structureId="+pdbcode+"&bionumber=1#"
  url = "http://www.rcsb.org/pdb/explore/pubmedArticle.do?structureId=" + pdbcode
  #print "url = " + url
  
  #page=requests.get(url)
  
  webfile = urllib.urlopen(url)
  page    = webfile.read()
  webfile.close()
  
  
  splitpage=page.split('\n')
  
  flag = False
 
  uniprot_list = [] 
  count = 0 
  id = ''
  title = ''
  for line in splitpage:
      #if "Citation" in line:
      #   print line
      if "titleIn" in line:
         #print line
         title = line.split("'")[1]
         #print title
      if "uid" in line:
    #    print line
         splitline = line.replace(';',' ').split()
         for word in splitline:
             if "uids" in word:
                 id = word.replace('"','').split('=')[1]  
                 #print '\n'+id+'\n'
    # if "pubmed" in line:
    #    print line
    #    flag = True
    # elif (flag and 'title' in line and "UniProtKB entry" in line):
    #    uniprot=line.replace(' ','_').replace('<',' ').replace('>',' ').split()[1].replace('_','')
    #    flag = False
    #    ## <li id="sub-72436952" class="zinc summary-item">
    #    #sliteline = line.replace('<',' ').replace('>',' ').replace('-',' ').replace('=',' ').replace('"','').split()
    #    #print line
    #    #print sliteline
    #    #zincid = sliteline[3]
    #    #print "Isomeric SMILES = " + smiles
    #    print str(count) + " " + uniprot + " " + pdbcode
    #    count = count+1
    #    uniprot_list.append(uniprot)
  return title, id

