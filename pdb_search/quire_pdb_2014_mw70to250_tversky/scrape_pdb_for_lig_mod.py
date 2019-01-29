
## This module is writen by
## Trent E Balius
## 2014/08/08 
################################################################
## scrapes the pdb webpage for the smiles string for a given 
## residue name. 
## This is modifed from ~/zzz.scripts/search_pdb_lig_code.py. 
################################################################


import sys,urllib,urllib2

def scrape_pdb_for_lig(pdbcode):
  url = 'http://www.rcsb.org/pdb/explore/explore.do?structureId=' + pdbcode

  #print "url = " + url

  #page=requests.get(url)
  try:
    webfile = urllib.urlopen(url)
    page    = webfile.read()
    webfile.close()
  except:
  #else:
    page = ''
    print "could not open: " + url


  splitpage=page.split('\n')

  flag = False

  lig_list = []
  count = 0
  for line in splitpage:
      if "Ligand" in line:
         if "onclick" in line:
             splitline = line.split()
             #if len(splitline) == 2:
             if len(splitline) == 2 and splitline[1][len(splitline[1])-1] != '>':
                print splitline[1]
                lig_list.append(splitline[1])
                count = count + 1
  return count, lig_list


def scrape_pdb_for_lig_smiles(ligresid): 
   #ligresid     = sys.argv[1]
   
   #url = 'http://zinc.docking.org/results/structure?structure.smiles='+smiles+'&structure.similarity=' + similarity
   url = 'http://www.rcsb.org/pdb/ligand/ligandsummary.do?hetId=' + ligresid

   smiles = ''   
   #print "url = " + url
   
   #page=requests.get(url)
   
   #webfile = urllib.urlopen(url)
   #page    = webfile.read()
   #webfile.close()
   try:
     webfile = urllib.urlopen(url)
     page    = webfile.read()
     webfile.close()
   #except ValueError:
   except:
   #else:
     page = ''
     print "could not open: " + url
   
   splitpage=page.split('\n')
   
   flag = False
   
   count = 0 
   for line in splitpage:
       if "Isomeric SMILES" in line:
          #print line
          flag = True
       elif (flag and 'textarea' in line):
          smiles=line.replace('<',' ').replace('>',' ').split()[3]
          flag = False
          ## <li id="sub-72436952" class="zinc summary-item">
          #sliteline = line.replace('<',' ').replace('>',' ').replace('-',' ').replace('=',' ').replace('"','').split()
          #print line
          #print sliteline
          #zincid = sliteline[3]
          #print "Isomeric SMILES = " + smiles
          print smiles + " " + ligresid 
          count = count+1
   
   if (count == 0):
      print "code " + ligresid + " not found"
   elif (count > 1):
      print "something werd is happening. count > 1"
   
   
   #fileoutput = ligresid+".smi"
   #fileh = open(fileoutput,'w')
   #fileh.write(smiles+' '+ligresid+'\n')
   #fileh.close()
   return smiles
   
 
