#! /usr/bin/python
import sys
import gzip

#################################################################################################################
def read_write_indock(input_file, output_file):
    print "input file ="+input_file
    print "output file ="+output_file

    file1 = open(input_file,'r')
    lines  =  file1.readlines()
    file1.close()
    file2 = open(output_file,'w')
 
    
    for line in lines:
        splitline = line.split()
        if ("electrostatic_scale" == splitline[0]):
            file2.write("gist_scale                    -1.0 #scaling factors to be applied to gist score\n")
        elif ("rec_number" == splitline[0]):
            recnum = int(line.split()[1])
        elif ("solvmap_file" == splitline[0]):
            if (recnum == 1):
               file2.write("gist_file                     ../../../gist_grids/gist-EswPlusEww_ref2.dx\n")
               file2.write("gist_aprox                    0\n")
            else:
               file2.write("gist_file                     ../../../gist_grids/gist-zero.dx\n")
               file2.write("gist_aprox                    0\n")
        if ('../' in line):
            line = line.replace('../','../../../')
        file2.write(line)
    file2.close()
    return 
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print "This Script reads in a INDOCK file"
        print "  (1) Input file: INDOCK"
        print "  (2) Output file: INDOCK_gist"
        print len(sys.argv)
        return
    
    inputfile  = sys.argv[1]
    outputfile  = sys.argv[2]
    read_write_indock(inputfile,outputfile)

    
    
#################################################################################################################
#################################################################################################################
main()
