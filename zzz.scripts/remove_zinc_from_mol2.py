import math, sys
import os.path

from math import sqrt

#################################################################################################################
# this function reads in a multi mol2 file and a list of zinc codes and writes out a mol2 
# file with those entries removed not in the list. 
#################################################################################################################

def read_write_dock_multimol2_remove_list(filename,listfile):
    # reads in data from mol2 file produesed by dock.

    diclist = {}
    file0 = open(listname,'r')
    for line in file0:
        splitline = line.split()
        zincname = splitline[0]
        if not zincname in diclist:
            diclist[zincname] = 1

    file1 = open(filename,'r')

    splitfilename = filename.split('.')
    if len(splitfilename) == 2:
        filename2 = splitfilename[0]+"_new.mol2"
    else:
        print "error.  file name does not have exactly one dots,'.'. "

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
         linesplit = line.split() #split on white space
         if (len(linesplit) >0 ):

             if (linesplit[0][0] != "#"):
                 flag = True
             else:
                 flag = False
                 header = header + line
                 if (len(linesplit) == 3):
                     if (linesplit[1] == "Name:"):
                         print line
                         name = linesplit[2]
                         if name in diclist:
                            #nameflag = False
                            nameflag = True
                         else:
                            #nameflag = True 
                            nameflag = False
             if (nameflag and flag and linesplit[0] == "@<TRIPOS>MOLECULE"):
                 file2 = open(outputfilename,'w')
                 file2.write(header)
                 file2.write(line)
                 count = count+1
                 #flag = False
                 header = ''
             elif (nameflag and flag):
                 file2.write(line)
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

    read_dock_multimol2_file_printmol2_files(filename,outsetname)
    return 
#################################################################################################################
#################################################################################################################
main()
