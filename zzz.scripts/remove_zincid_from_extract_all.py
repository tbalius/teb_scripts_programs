import math, sys
import os.path

from math import sqrt

#################################################################################################################
# this function reads in an extract all file  and writes out a 
# file with those entries removed not in the list. 
#################################################################################################################

def read_write_dock_extract_all_kept_list(filename,listfile):
    # reads in data from mol2 file produesed by dock.

    diclist = {}
    file0 = open(listfile,'r')
    for line in file0:
        splitline = line.split()
        zincname = splitline[0]
        if not zincname in diclist:
            #print zincname 
            diclist[zincname] = 1

    file1 = open(filename,'r')

    splitfilename = filename.split('.')
    print filename
    if len(splitfilename) == 2:
        filename2 = splitfilename[0]+"_new.txt"
    if len(splitfilename) == 4:
        filename2 = splitfilename[0]+"."+splitfilename[1]+"."+splitfilename[2]+"_new.txt"
    else:
        print "error.  file name does not have right number of dots,'.', in filename. "
        exit()

    file2 = open(filename2,'w')

    #outputfilename = outputprefix + str("_00001.mol2") 
    #file2 = open(outputfilename,'w')
    lines  =  file1.readlines()
    count = 1

    flag = True  ## flag is true for the first lin that is not a comment.

    header = ''
    #header_old = ''
    nameflag = False

    for line in lines:
        line = line.strip('\n')
        splitline = line.split()
        #id = "ZI"+splitline[2].split('.')[0]
        id = splitline[2].split('.')[0]
        #print id
        #print diclist.keys()
        if id in diclist:
           print id
           file2.write(line+'\n') 
    #file2.write(header)
    #file2.write(line)
    file1.close()
    file2.close()
    return
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print " This script needs the following:"
        print " (1) mol2filename, "
        print " (2) listfile "
        print " This script reads in a multi mol2 file and a list of zinc codes and writes out a mol2 file with those codes in list. "
        return

    filename       = sys.argv[1]
    listname       = sys.argv[2]

    read_write_dock_extract_all_kept_list(filename,listname)
    return 
#################################################################################################################
#################################################################################################################
main()
