#! /usr/bin/python
import sys

# Writen by Trent Balius, Dec, 2013
  ## this sript adds model delinators
  ## to dock output

#################################################################################################################
#################################################################################################################
def write_mod_pdb(pdb_file,pdb_out):
    ## reads in pdb
    file1 = open(pdb_file,'r')
    lines  =  file1.readlines()
    newfile = '' # this is going to be written to file2 if there is a modification
    flagWriteFile = True
    #newfile = newfile+'MODEL 1'

    falgNewModel = True
    countModels = 1
    for line in lines:
         #print line
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 1):
            if (falgNewModel):
               newfile = newfile+'MODEL '+ str(countModels)+'\n'
               falgNewModel = False
            if (linesplit[0] == "REMARK" ):
                newfile = newfile+line
            if (linesplit[0] == "ATOM" or linesplit[0] == "HETATM"):
                #print line
                #lenline = len(line)
                newfile = newfile+line
                #if ( line[16] == ' '):
                #      newfile = newfile+line
                #elif(line[16] == 'A'):
                #      newfile = newfile+line[0:16]+' '+line[17:lenline]
                #else:
                #      flagWriteFile = True
            if (linesplit[0] == "TER"):
                #print line
                newfile = newfile+'TER\nENDMDL\n'
                falgNewModel = True
                countModels = countModels + 1
 
    file1.close()
    print "This pdb contained " + str(countModels-1) + " models"

    #if (countModels < 2):
    #    flagWriteFile = false

    if (flagWriteFile):
       file2 = open(pdb_out,'w')
       file2.write(newfile)
       file2.close()
    else:
       print "No modification."

    return
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print "This function takes as input a pdb file"
        print "Writes a new pdbfile with model info."
        print "This is writen by Trent Balius"
        print "python pdb_one_conf.py input.pdb output.pdb"
        print len(sys.argv)
        return
    
    pdb_file  = sys.argv[1]
    pdb_out   = sys.argv[2]

    write_mod_pdb(pdb_file,pdb_out)
    
    
#################################################################################################################
#################################################################################################################
main()
