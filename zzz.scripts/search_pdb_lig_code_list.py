
## This script is writen by
## Trent E Balius
## 2013/12 
################################################################
## This script  
## scrapes the pdb webpage for the smiles string for a given 
## residue name. 
################################################################


import sys,urllib,urllib2

def get_smiles(ligresid):
    #url = 'http://zinc.docking.org/results/structure?structure.smiles='+smiles+'&structure.similarity=' + similarity
    #url = 'http://www.rcsb.org/pdb/ligand/ligandsummary.do?hetId=' + ligresid
    url = 'https://www3.rcsb.org/ligand/' + ligresid
    
    #print "url = " + url
    
    #page=requests.get(url)
    
    webfile = urllib.urlopen(url)
    page    = webfile.read()
    webfile.close()
    
    #print page
    
    splitpage=page.split('\n')
    
    flag = False
    flagSmi = False
    
    #count = 0 
    for line in splitpage:
        if flagSmi: 
           break
        #print line
        if len(line.split())==0:
            continue
        if "Isomeric SMILES" in line:
        #if "chemicalIsomeric" in line:
           #print line
           #flag = True
           smilesline = ""
           count1 = 0
           for substring in line.split(" "):
                #print substring
                #if "Isomeric SMILES" in substring:
                #if "chemicalIsomeric" in line:
                if "SMILES" in substring:
                    #print substring
                    #exit()
                   flag = True
                if flag:
                   if count1 ==2:
                      #print substring
                      subsubsting = substring.replace('<',' ').replace('>',' ').split()
                      #print subsubsting[1] 
                      smiles = subsubsting[1] 
                      flagSmi = True
                      break
                   #print substring
                   if count1 == 10: 
                      exit()
                   count1 = count1 + 1
    
        #elif (flag and 'td' in line):
    #    if (flag): 
    #       smilesline = smilesline+line
    #    if (flag and '</td>' in line):
    #       #print smilesline
    #       #smiles=smilesline.replace('<',' ').replace('>',' ').split()[1]
    #       smiles=smilesline.split()[3]
    #       flag = False
    #       ## <li id="sub-72436952" class="zinc summary-item">
    #       #sliteline = line.replace('<',' ').replace('>',' ').replace('-',' ').replace('=',' ').replace('"','').split()
    #       #print line
    #       #print sliteline
    #       #zincid = sliteline[3]
    #       #print "Isomeric SMILES = " + smiles
           print smiles + " " + ligresid 
    #       count = count+1
    return smiles

#if (count == 0):
#   print "code not found"
#elif (count > 1):
#   print "something werd is happening. count > 1"

if len(sys.argv) != 2:
    print "Error: one arguments is needed"
    print "list of ligand name"
    sys.exit()

filelig     = sys.argv[1]

fh = open(filelig,'r')

fileoutput = filelig+".smi"
fileh = open(fileoutput,'w')
for line in fh:
  ligresid = line.split()[0]
  smiles = get_smiles(ligresid)
  fileh.write(smiles+' '+ligresid+'\n')

fileh.close()


