#! /usr/bin/python
import sys

#################################################################################################################
#################################################################################################################
def write_mod_pdb(pdb_file,pdb_out):
    ## reads in pdb id how meny residues are in each chain
    file1 = open(pdb_file,'r')
    lines  =  file1.readlines()
    newfile = '' # this is going to be written to file2 if there is a modification
    flagWriteFile = False
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 1):
            if (linesplit[0] == "ATOM" or linesplit[0] == "HETATM"):
                lenline = len(line)
                if ( line[16] == ' '):
                      newfile = newfile+line
                elif(line[16] == 'A'):
                      newfile = newfile+line[0:16]+' '+line[17:lenline]
                else:
                      flagWriteFile = True
                     
 
    file1.close()

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
        print "Writes a new pdbfile with only one conformation, the A conformation."
        print "python pdb_one_conf.py input.pdb output.pdb"
        print len(sys.argv)
        return
    
    pdb_file  = sys.argv[1]
    pdb_out   = sys.argv[2]

    write_mod_pdb(pdb_file,pdb_out)
    
    
#################################################################################################################
#################################################################################################################
main()
