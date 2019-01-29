import math, sys
import os.path
import gzip
from math import sqrt

#################################################################################################################
# this function reads in a multi eel(modified pdb file formate) file and writes out indevidual eel 
# files.  each file coresponds to a pose.
#################################################################################################################

def read_dock_eel_file_print_eel_files(file,outputprefix):
    # reads in data from eel file produesed by dock.

    if not (os.path.exists(file)):
        print file + "does not exist. \n\n Exiting script . . ."
        exit() 
    splitfile = file.split('.')
    N = len(splitfile)-1
    print splitfile[N]
    if (splitfile[N] == 'gz'):
       file1 = gzip.open(file, 'rb')
    else:
       file1 = open(file,'r')

    lines  =  file1.readlines()
    #outputfilename = outputprefix + str(".001.eel") 
    count = 1
    outputfilename = outputprefix + str("_0000") + str(count) + str(".eel")
    file2 = open(outputfilename,'w')

    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >0 ):
             #if (linesplit[0] == "TER"):
             if (linesplit[0] == "ENDMDL"):
                 file2.write(line)
                 file2.close()
                 count = count + 1
                 if (count < 10):
                    outputfilename = outputprefix + str("_0000") + str(count) + str(".eel")
                 elif (count <100):
                    outputfilename = outputprefix + str("_000") + str(count) + str(".eel")
                 elif (count <1000):
                    outputfilename = outputprefix + str("_00") + str(count) + str(".eel")
                 elif (count <10000):
                    outputfilename = outputprefix + str("_0") + str(count) + str(".eel")
                 else:
                    outputfilename = outputprefix + str("_") + str(count) + str(".eel")
                 file2 = open(outputfilename,'w')
             else:
                 file2.write(line)
    file1.close()
    # remove last empty file the name will be outputfilename 
    os.system('rm ' + outputfilename )

    return
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print " This script needs the following:"
        print " (1) eel file (like a pdb file formate)  "
        print " (2) outputprefix "
        return

    filename       = sys.argv[1]
    outputprefix = sys.argv[2]

    read_dock_eel_file_print_eel_files(filename, outputprefix)
    return 
#################################################################################################################
#################################################################################################################
main()
