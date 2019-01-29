import math, sys
import os.path

from math import sqrt

#################################################################################################################
# this function reads in a multi mol2 file and writes out indevidual mol2 
# files.  each file coresponds to a pose.
# Written by Trent Balius 
# modified by Jiankun Lyu
#################################################################################################################

def read_dock_multimol2_file_printmol2_files(file,outputprefix):
    # reads in data from mol2 file produesed by dock.

    file1 = open(file,'r')

    outputfilename = outputprefix + str("_00001.mol2") 
    file2 = open(outputfilename,'w')
    lines  =  file1.readlines()
    count = 1

    flag = True  ## flag is true for the first lin that is not a comment.

    header = ''

    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >0 ):

             if (linesplit[0][0] != "#"):
                 flag = True
             else:
                 flag = False
                 header = header + line
             if (flag and linesplit[0] == "@<TRIPOS>MOLECULE"):
                 file2.close()
                 # consider modifing this to:  outputfilename = "%s_%05d%s" % (outputprefix, count,".mol2")
                 if (count < 10):
                    outputfilename = outputprefix + str("_0000") + str(count) + str(".mol2")
                 elif (count <100):
                    outputfilename = outputprefix + str("_000") + str(count) + str(".mol2")
                 elif (count <1000):
                    outputfilename = outputprefix + str("_00") + str(count) + str(".mol2")
                 elif (count <10000):
                    outputfilename = outputprefix + str("_0") + str(count) + str(".mol2")
                 else:
                    outputfilename = outputprefix + str("_") + str(count) + str(".mol2")
                 file2 = open(outputfilename,'w')
                 file2.write(header)
                 file2.write(line)
                 count = count+1
                 #flag = False
                 header = ''
             elif (flag):
                 file2.write(line)
         else:
             file2.write(line)       
    return
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print " This script needs the following:"
        print " (1) mol2filename, "
        print " (2) outputprefix "
        return

    filename       = sys.argv[1]
    outputprefix = sys.argv[2]

    read_dock_multimol2_file_printmol2_files(filename, outputprefix)
    return 
#################################################################################################################
#################################################################################################################
main()
