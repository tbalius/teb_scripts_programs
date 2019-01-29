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
       return max

print " stuff that matters::::::::::"

filein = open("uniprot_lig_tversky_mwdiff_formula_diff.txt",'r')
fileout = open("uniprot_max_linked_list_size.txt",'w')

uniprot_old = ''
sublist = []
lines = []

for line in filein:

    if "This" in line:
        continue
    print line
    splitline = line.split()
    uniprot = splitline[0].strip(',')
    lig1 = splitline[2].strip(',')
    lig2 = splitline[3].strip(',')
    mfd  = float(splitline[13])

    if (mfd>4.0): # if the molecular formula difference is grater than 4 then skip the line (pair)
         print "skiped"
         continue

    if uniprot_old != uniprot:
       max = find_linked_list_count(lines)
       print uniprot_old, max 
       if (max > 5):
           fileout.write(uniprot_old+" "+str(max)+'\n')
       lines = []
       uniprot_old = uniprot

    lines.append(lig1+' '+lig2)

find_linked_list_count(lines)
print uniprot_old, max 
if (max > 5):
    fileout.write(uniprot_old+" "+str(max)+'\n')

filein.close()
fileout.close()

