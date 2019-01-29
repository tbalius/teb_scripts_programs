import math, sys
import os.path

from math import sqrt


def read_multi_fpfile(filename,molname,text1):
    file1 = open(filename,'r')
    lines  =  file1.readlines()

    print_flag = False;
    #header_flag = False;
    #header = ''

    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) > 0):
             if ( molname in line ):
                print_flag =  True
             elif ("  Name:" in line):
                print_flag = False
             if (line[0] == "#"):
                continue 
 
                #header_flag = True
             #if (linesplit[0] == "TER" ):
             #   header = ''
             #   header_flag = False
#             if (linesplit[0] == "ENDMDL":
             #if (linesplit[0] == "REMARK" and linesplit[1] == "Name" and linesplit[3] == molname):
             #   print line
             #   print_flag = True
             #   header_flag = False
             #   text1 = text1+header # add header to text1 for output

             #if (header_flag): 
             #   header = header+line
             ## we will put the molecule in  
             ## file for the listed molecules (text1)
             if (print_flag):
                text1 = text1+line # add line to text1 for output

    file1.close()
    return text1
#################################################################################################################
#################################################################################################################
def main():
    if (len(sys.argv) != 4): # if no input
        print " (1) mol2 file name," 
        print " (2) file with mol names you want to search for and output, ";
        print " (3) output file for found ligands, ";
        return

    filename    = sys.argv[1]
    #molnamefile = sys.argv[2]
    molname     = sys.argv[2]
    output      = sys.argv[3]

    text1 = '' # text to be writen to output
    #file1 = open(molnamefile,'r')
    #lines = file1.readlines()
    #file1.close()

    #for molname in lines:
    #   print "searching " + filename + " for molecule " + molname
    text1 = read_multi_fpfile(filename,molname,text1)

    file2 = open(output,'w')
    file2.write(text1)
    file2.close()

    return; 
#################################################################################################################
#################################################################################################################
main()
