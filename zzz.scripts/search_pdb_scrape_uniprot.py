
## This script is writen by
## Trent E Balius
## 2014/02 
################################################################
## This script  
## scrapes the pdb webpage for uniprot.  
## This is modifed from ~/zzz.scripts/search_pdb_lig_code.py. 
################################################################


import sys,urllib,urllib2

def scrap_pdb_foruniprot(pdbcode):
  #url = 'http://zinc.docking.org/results/structure?structure.smiles='+smiles+'&structure.similarity=' + similarity
  url = 'http://www.rcsb.org/pdb/explore/explore.do?structureId=' + pdbcode

  #print "url = " + url
  
  #page=requests.get(url)
  
  webfile = urllib.urlopen(url)
  page    = webfile.read()
  webfile.close()
  
  
  splitpage=page.split('\n')
  
  flag = False
  
  count = 0 
  for line in splitpage:
      if "UniProtKB:" in line:
         #print line
         flag = True
      elif (flag and 'title' in line and "UniProtKB entry" in line):
         uniprot=line.replace(' ','_').replace('<',' ').replace('>',' ').split()[1].replace('_','')
         flag = False
         ## <li id="sub-72436952" class="zinc summary-item">
         #sliteline = line.replace('<',' ').replace('>',' ').replace('-',' ').replace('=',' ').replace('"','').split()
         #print line
         #print sliteline
         #zincid = sliteline[3]
         #print "Isomeric SMILES = " + smiles
         print uniprot + " " + pdbcode
         count = count+1

def main():
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
      scrap_pdb_foruniprot(pdb)
main()
