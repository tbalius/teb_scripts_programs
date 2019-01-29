## Trent Balius, Shoichet group, UCSF, 2014.08.08

import urllib, urllib2, math
import scrape_pdb_for_uniprot as spfu
import scrape_pdb_for_lig_mod as spfl
import scrape_zinc_zincid as szzi
import tanimoto_cal_axon as tancal


def find_linked_list_count(lines):
       list = []
       sublist = []
       #sublist.append(lig1)
       #sublist.append(lig2)

       #print "lines = ", lines
       while (len(lines)>0):
             #print "sublist = ",sublist
             num = len(lines)
             for i in range(len(lines)):
                #print lines[i]
                splitline = lines[i].split()
                lig1 = splitline[0]
                lig2 = splitline[1]
                if (lig1 in sublist) and not (lig2 in sublist):
                    sublist.append(lig2)
                    del lines[i]
                    break
                elif (lig2 in sublist) and not (lig1 in sublist):
                    sublist.append(lig1)
                    del lines[i]
                    break
                elif ((lig2 in sublist) and (lig1 in sublist)):
                    del lines[i]
                    break
                elif (len(sublist) == 0):
                    sublist.append(lig1)
                    sublist.append(lig2)
                    del lines[i]
                    break
             #print num, len(lines)
             if (num  == len(lines) or len(lines) == 0):
                #print "I AM HERE ", sublist
                list.append(sublist)
                sublist = []
                #sublist.append(lig1)
                #sublist.append(lig2)
       #print "list = ",list
       max = 0
       for sublist in list:
           #print len(sublist) 
           #print sublist         
           if (max < len(sublist)):
               max = len(sublist)
       return max, list

def write_list_to_file(uniprot_old, fileout3, pdb2uniprot, lig2pdb, list):
    fileout3.write('\n')
    fileout3.write(uniprot_old)
    fileout3.write("\n")
    for sublist in list:
       fileout3.write(str(len(sublist))+' ')
       # print out the ligands
       print sublist
       for lig in sublist:
           fileout3.write(lig+" ")
       fileout3.write("\n")

       all_pdb = ''    
       for lig in sublist:
           fileout3.write("    ")
           fileout3.write(lig+": ")
           for pdb in lig2pdb[lig]:
              if not (pdb in pdb2uniprot):
                  print "Warning: "+pdb+" not in pdb2uniprot"
                  fileout3.write("("+pdb+" ???) ")
                  continue
              if uniprot_old in pdb2uniprot[pdb]:
                  print pdb
                  fileout3.write(pdb)
                  fileout3.write(' ')
                  all_pdb = all_pdb + ' ' + pdb
           fileout3.write("\n")
       fileout3.write("    all pdbs: "+all_pdb+"\n") 



print " stuff that matters::::::::::"

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
    if pdb in pdb2uniprot:
       pdb2uniprot[pdb].append(uniprot)
    #   print pdb2uniprot[pdb] 
    #   exit()
    else:
       pdb2uniprot[pdb] = []
       pdb2uniprot[pdb].append(uniprot)
filein2.close()

#
#



#filein = open("uniprot_lig_tanamoto_mwdiff_formula_diff.txt",'r')
filein = open("uniprot_lig_tanamoto_mwdiff_formula_diff_new.txt",'r')
fileout = open("uniprot_max_linked_list_size.txt",'w')
fileout2 = open("uniprot_lig_tanamoto_mwdiff_formula_diff_reduced.txt",'w')
fileout3 = open("uniprot_max_linked_list.txt",'w')

uniprot_old = ''
#sublist = []
lines = []
writelines = ''

for line in filein:

    if "This" in line:
        continue
    print line
    splitline = line.split()
    uniprot = splitline[0].strip(',')
    lig1 = splitline[2].strip(',')
    lig2 = splitline[3].strip(',')
    #mfd  = float(splitline[13])
    mfd  = float(splitline[16])
    tc   = float(splitline[6])

    #if (mfd>4.0): # if the molecular formula difference is grater than 4 then skip the line (pair)
    if (mfd>1.0): # if the molecular formula difference heavy atoms is grater than 1 then skip the line (pair)
         print "skiped"
         continue
    #if (mfd == 0.0 and tc == 1.0):
    #    print "skiped because ligs are isomers"
    #    continue

    if uniprot_old != uniprot:
       max, list = find_linked_list_count(lines)
       print uniprot_old, max 
       if (max > 5):
           fileout.write(uniprot_old+" "+str(max)+'\n')
           fileout2.write(writelines) # will right out all line the for uniprot that pass (max>5) and the mfd>4.0
           write_list_to_file(uniprot_old, fileout3, pdb2uniprot, lig2pdb, list)

       lines = []
       writelines = ''
       uniprot_old = uniprot

    lines.append(lig1+' '+lig2)
    writelines=writelines+line # this will  

max, list = find_linked_list_count(lines)
print uniprot_old, max 
if (max > 5):
    fileout.write(uniprot_old+" "+str(max)+'\n')
    fileout2.write(writelines) # will right out all line the for uniprot that pass (max>5) and the mfd>4.0
    write_list_to_file(uniprot_old, fileout3, pdb2uniprot, lig2pdb, list)



filein.close()
fileout.close()
fileout2.close()
fileout3.close()

