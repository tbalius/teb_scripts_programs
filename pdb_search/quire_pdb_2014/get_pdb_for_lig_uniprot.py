## Trent Balius, Shoichet group, UCSF, 2014.08.08

import urllib, urllib2, math



#filein = open("uniprot_lig_tanamoto_mwdiff_formula_diff.txt",'r')
filein = open("pdbtolig_file.txt",'r')

lig2pdb = {}
for line in filein:
    splitline = line.split()
    pdb = splitline[0]
    lig = splitline[1] 
    if lig in lig2pdb:
       lig2pdb[lig].append(pdb)
    else:
       lig2pdb[lig] = []
       lig2pdb[lig].append(pdb)

filein.close()

filein2 = open("pdbtouniprot_file.txt",'r')
pdb2uniprot = {}

for line in filein2:
    splitline = line.split()
    pdb = splitline[0]
    uniprot = splitline[1]
    if uniprot in pdb2uniprot:
       pdb2uniprot[pdb].append(uniprot)
    else:
       pdb2uniprot[pdb] = []
       pdb2uniprot[pdb].append(uniprot)

filein2.close()

filein3 = open("uniprot_lig_tanamoto_mwdiff_formula_diff_reduced.txt",'r')

for line in filein3:
    print line
    splitline = line.split()
    uniprot = splitline[0].strip(',')
    lig1 = splitline[2].strip(',')
    lig2 = splitline[3].strip(',')
    #print uniprot, lig1, lig2, lig2pdb[lig1], lig2pdb[lig2]
    print uniprot
    for lig in [lig1,lig2]:
      print "  "+lig
      print "    ",
      for pdb in lig2pdb[lig]: 
        if uniprot in pdb2uniprot[pdb]:
           print pdb+" ",
      print ""

    

filein2.close()
