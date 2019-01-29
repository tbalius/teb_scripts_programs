import math, sys
import os.path

from math import sqrt


def read_multi_mol2file(filename,num):
    file1 = open(filename,'r')
    #lines  =  file1.readlines()

    #print_flag = False;
    #for line in lines:

    data = []

    print "reading mol2"
    for line in file1:
         linesplit = line.split() #split on white space
         if (len(linesplit) > 0):
             #if ( molname in line and "  Name:" in line):
             if ("  Name:" in line):
                name = linesplit[2]
             elif ("Total Energy:" in line):
                energy = float(linesplit[3])
                data.append([name,  energy])
    file1.close()
    print "sorting data"
    data_sort = sorted(data, key=lambda ele: ele[1])
    print "writing data"
    text1 = ""

    #max_count = 1000
    max_count = num
    count = 0 
    for ele in data_sort:
        #print ele
        text1 = text1 + "%s\t%f\n"%(ele[0],ele[1])
        if count > max_count: 
           break
        count=count+1
    print text1
    return text1
#################################################################################################################
#################################################################################################################
def main():
    if (len(sys.argv) != 4): # if no input
        print " (1) mol2 file name," 
        print " (2) number," 
        print " (3) output file  ";
        return

    filename  = sys.argv[1]
    num       = int(sys.argv[2])
    output    = sys.argv[3]

    text = read_multi_mol2file(filename,num) 

    #print text

    file2 = open(output,'w')
    file2.write(text)
    file2.close()

    return; 
#################################################################################################################
#################################################################################################################
main()
