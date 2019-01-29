import math, sys
import os.path
#import subprocess

from math import sqrt

#################################################################################################################
## Writen by Trent Balius
## modified in the Shoichet Group, UCSF
## based on fpalign.py from Rizzo Group.

#################################################################################################################

def seq_align(seqfile1,seqfile2):
    #cwpath = os.system("echo $CWPATH")
    #blast_command = "/usr/bin/blastp -query " + seqfile1 + " -subject " + seqfile2
    blast_command = "/mnt/nfs/home/tbalius/zzz.programs/blast/ncbi-blast-2.2.28+/bin/blastp -query " + seqfile1 + " -subject " + seqfile2
    #os.system(blast_command)
    #p = subprocess.popen(blast_command,
    #                 stdout=subprocess.PIPE)
    p = os.popen(blast_command).read()
    #print p
    for line in p.split('\n'):
        if "Expect" in line:
            #print line
            eval = line.split()[7].strip(',')
            #print line.split()[7].strip(',') 
            break

    #return
    return eval

#################################################################################################################
def mkfasta(pdbfile,seqfile):
    file1 = open( seqfile ,'w')
    if (not os.path.exists(pdbfile)):
       print pdbfile + " does not exist."
       sys.exit()
    if (os.stat(pdbfile)[6]==0):
       print pdbfile + " is empty."
       sys.exit()
    file2 = open(pdbfile,'r')

    seq = []
    seqsl = ''
    lines  =  file2.readlines()
    file2.close()

    oldres = ''
    for line in lines:
         linesplit = line.split()
         if (len(linesplit) >0 ):
             #if (linesplit[0] == "HETATM"):
             #   print "HETATM  " + line[17:26]

             if (linesplit[0] == "ATOM" ):
                 newres = line[17:26]
                 #print newres
                 if (newres == oldres): 
                     continue

                 oldres = newres  
                 resname = newres[0] + newres[1] + newres[2]
                 if   (resname == "ARG"):
                     ressl = "R"
                 elif (resname == "LYS"):
                     ressl = "K"
                 elif (resname == "TRP"):
                     ressl = "W"
                 elif (resname == "TYR"):
                     ressl = "Y"
                 elif (resname == "ASP"):
                     ressl = "D"
                 elif (resname == "GLU"):
                     ressl = "E"
                 elif (resname == "ASN"):
                     ressl = "N"
                 elif (resname == "GLN"):
                     ressl = "Q"
                 elif (resname == "PHE"):
                     ressl = "F"
                 else:
                     ressl = resname[0]
                 seqsl = seqsl + ressl
                 #print ressl, resname
    #print seqsl
    file1.write( ">sequence" + '\n' )
    file1.write( seqsl + '\n' )


    
#################################################################################################################
def align(file1,file2,output):
    # reads in data from PDB.
   
    seqfile1 = output + '.1.fasta'
    seqfile2 = output + '.2.fasta'
    mkfasta(file1,seqfile1)
    mkfasta(file2,seqfile2)
    eval = seq_align(seqfile1,seqfile2)

    return eval
#################################################################################################################
def main():
    if (len(sys.argv) != 4): # if no input
        print " This script needs the following:"
        print " (1) 2 PDB file, "
        print " (2) output prefix "
        print " # of arguments = " + str(len(sys.argv)-1)
        return

    pdbfile1 = sys.argv[1]
    pdbfile2 = sys.argv[2]
    #output = sys.argv[(len(sys.argv) - 1)]
    output = sys.argv[3]
    eval = align( pdbfile1, pdbfile2, output)
    print pdbfile1, pdbfile2, eval 
    return 
#################################################################################################################
#################################################################################################################
main()
