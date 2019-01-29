#! /usr/bin/python
import sys

#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 2: # if no input
        print "This script take input file:"
        print "  (1) inputfile with 3 colomns: UNIPROT, #PDB, #CHEMBLE LIG"
        print len(sys.argv)
        return
    
    file  = sys.argv[1]
    filehandel = open(file)

    lines  =  filehandel.readlines()

    data_array = [] ## data_array 2 X N

    #initalize Matrix
    matrix = []
    for i in range(0,4):
        row = []
        for j in range(0,4):
            row.append(0)
        matrix.append(row)

    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) == 3):
            uniprot = linesplit[0]
            numpdb  = int(linesplit[1])
            numlig  = int(linesplit[2])
            print uniprot, numpdb, numlig
            if (numpdb == 0):
                catpdb=0 # cat stands for catagory or group
            elif (numpdb == 1):
                catpdb=1 # cat stands for catagory or group
            elif (numpdb > 1 and numpdb < 11):
                catpdb = 2 
            elif (numpdb > 10):
                catpdb = 3
            else:
                print "error in the PDB column"
                exit()

            if (numlig == 0):
                catlig=0 # cat stands for catagory or group
            elif (numlig == 1): # 
                catlig=1 # cat stands for catagory or group
            elif (numlig > 1 and numlig < 11): 
                catlig = 2
            elif (numlig > 10):
                catlig = 3
            else:
                print "error in the ligand column"
                exit()
            entry = [catpdb, catlig]
            data_array.append(entry)

            print catpdb,catlig
            matrix[catpdb][catlig] = matrix[catpdb][catlig] + 1;

    #print Matrix
    for i in range(0,4):
        for j in range(0,4):
             print matrix[i][j],
        print " "
    

            

        
#################################################################################################################
#################################################################################################################
main()
