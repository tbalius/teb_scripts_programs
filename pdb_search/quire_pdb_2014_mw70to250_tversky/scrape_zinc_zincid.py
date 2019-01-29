
## This script is writen by
## Trent E Balius
## 2013/11/29
## this is a script to search ZINC 12:

################################################################
## Search for a smiles string returns a zinc id               ##
################################################################


import sys,urllib,urllib2


def scrape_zinc_zincid(smiles, similarity): 
  #smiles     = sys.argv[1]
  #similarity = sys.argv[2]
  
  #url = 'http://zinc.docking.org/results/structure?structure.smiles='+smiles+'&structure.similarity=' + similarity
  url = 'http://zinc.docking.org/results/similar?structure.smiles='+smiles+'&structure.similarity='+ str(similarity) + "&filter.purchasability=all"
  
  print "url = " + url
  
  #page=requests.get(url)
  
  #webfile = urllib.request.urlopen(url,data=None,30)
  webfile = urllib.urlopen(url)
  page    = webfile.read()
  webfile.close()
  
  
  splitpage=page.split('\n')
   
  zincid_list = []
  for line in splitpage:
     #print line 
     if "zinc summary-item" in line:
         #print line
         ## <li id="sub-72436952" class="zinc summary-item">
         sliteline = line.replace('<',' ').replace('>',' ').replace('-',' ').replace('=',' ').replace('"','').split()
         #print line
         #print sliteline
         zincid = sliteline[3]
         print "zinc id = " + zincid
         zincid_list.append(zincid)
  return zincid_list 
  
