import math, sys
import os.path

import gzip

from math import sqrt

# Written by Trent Balius and Jiankun Lyu

def read_multi_db2_gz_file(input_data,molnamedic,text1):
    #file1 = open(filename,'r')
    #file1 = gzip.open(filename,'r')
    #lines  =  file1.readlines()
    lines = input_data

    print_flag = False;
    flagMline1 = True;
    #header_flag = False;
    #header = ''
    #print(lines)
    #print molname
    textall=""
    text1="" # body of the molecule
    for line in lines:
         #print(line)
         #exit()
         linesplit = line.split() #split on white space
         if (line[0] == "M" and flagMline1):
            flagMline1 = False
            name = linesplit[1]
            #print(name) 
            #print(molnamedic)
            if name in molnamedic:
                print(name+" in dict") 
                print_flag =  True

         if (print_flag):
            text1 = text1+line # add line to text1 for output

         if (line[0] == "E"):
            textall = textall + text1 
            text1 = ""
            print_flag = False
            flagMline1 = True;

    textall = textall + text1 
    
    #file1.close()
    return textall
#################################################################################################################
#################################################################################################################
def main():
    if (len(sys.argv) != 3): # if no input
        print (" (1) file with mol names you want to search for and output, ");
        print (" (2) output file for found ligands, ");
        return

    molnamefile = sys.argv[1]
    #molname     = sys.argv[2]
    output      = sys.argv[2]

    text1 = '' # text to be writen to output
    file1 = open(molnamefile,'r')
    lines = file1.readlines()
    file1.close()

    molname_dict = {}
    textAll = ""
    for molname in lines:
       #print(molname)
       molname_dict[molname.strip()] = 1
    lines_stdin = sys.stdin.readlines()
    text1 = read_multi_db2_gz_file(lines_stdin,molname_dict,text1)
    file2 = gzip.open(output,'w')
    file2.write(text1.encode())
    file2.close()

    return; 
#################################################################################################################
#################################################################################################################
main()
