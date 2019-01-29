import math, sys
import os.path

from math import sqrt

#################################################################################################################
# this function reads in two lists and writes two files not_in_one.txt and not_in_two.txt
#################################################################################################################

def diff_list(list1file,list2file):
    # reads in data from mol2 file produesed by dock.

    diclist = {} # may have 3 values o if only in one and t if only in two and b if in both
    # read in list 1
    file1 = open(list1file,'r')
    for line in file1:
        splitline = line.split()
        zincname = splitline[0]
        if not zincname in diclist:
            diclist[zincname] = 'o'

    file1.close()
    # read in list 2
    file2 = open(list2file,'r')
    for line in file2:
        splitline = line.split()
        zincname = splitline[0]
        if not zincname in diclist:
            diclist[zincname] = 't'
        else: 
            if diclist[zincname] == 'o': # if it is in both lists
               diclist[zincname] = 'b'
    file2.close()

    file3 = open('not_in_two.txt','w')
    file4 = open('not_in_one.txt','w')
    file5 = open('in_both.txt','w')

    for key in diclist.keys():
        if diclist[key] == 'o':
           file3.write('%s\n'%key)
        elif diclist[key] == 't':
           file4.write('%s\n'%key)
        elif diclist[key] == 'b':
           file5.write('%s\n'%key)
    file3.close()
    file4.close()
    file5.close()

    return
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print " This script needs the following:"
        print " (1) listfile1, "
        print " (2) listfile2 "
        print " This script reads in 2 lists and writes out the differences. "
        return

    list1name       = sys.argv[1]
    list2name       = sys.argv[2]

    diff_list(list1name,list2name) 
    return 
#################################################################################################################
#################################################################################################################
main()
