import math, sys
import os.path

from math import sqrt

# Written by Trent Balius in the Shoichet Lab at UCSF

def read_multi_mol2file(filename):
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
             elif ("Ligand Charge:" in line):
                #charge = int(linesplit[3])
                charge = float(linesplit[3])
                data.append([name, charge, energy])
    file1.close()
    print "sorting data"
    data_sort = sorted(data, key=lambda ele: ele[2])
    print "writing data"
    text1 = ""

    dic = {}
    for  ele in data_sort:
         dic[ele[1]] = 0

    max_count = 1000
    count = 0 
    for ele in data_sort:
        #print ele
        text1 = text1 + "%s,%f,%f\n"%(ele[0],ele[1],ele[2])
        if count < max_count: 
           dic[ele[1]]=dic[ele[1]]+1
        else:
           break
        count=count+1
    for key in dic.keys():
        print key, dic[key]
    print filename,
    for key in dic.keys():
        print dic[key],
    print ""
    return text1
#################################################################################################################
#################################################################################################################
def main():
    if (len(sys.argv) != 3): # if no input
        print " (1) mol2 file name," 
        print " (2) output file  ";
        return

    filename    = sys.argv[1]
    output      = sys.argv[2]

    text = read_multi_mol2file(filename) 

    #print text

    file2 = open(output,'w')
    file2.write(text)
    file2.close()

    return; 
#################################################################################################################
#################################################################################################################
main()
