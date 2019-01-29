import math, sys
import os.path, os
import urllib,urllib2
#import subprocess

from math import sqrt

#################################################################################################################
## Writen by Trent E Balius
## in the Brian K Shoichet Group, University of Toronto

#################################################################################################################

def seq_align(seqfile1,seqfile2):
    #cwpath = os.system("echo $CWPATH")
    #blast_command = "/usr/bin/blastp -query " + seqfile1 + " -subject " + seqfile2
    blast_command = "/mnt/nfs/home/tbalius/zzz.programs/blast/ncbi-blast-2.2.28+/bin/blastp -query " + seqfile1 + " -subject " + seqfile2
    #os.system(blast_command)
    #p = subprocess.popen(blast_command,
    #                 stdout=subprocess.PIPE)
    eval = "-1000"
    p = os.popen(blast_command).read()
    print p

    for line in p.split('\n'):
        if "Expect" in line:
            #print line
            eval = line.split()[7].strip(',')
            #print line.split()[7].strip(',') 
            break
        if line == "***** No hits found *****": 
            print line 
            eval = "100"
            break

    if eval == "-1000":
       print "Warning: something went wrong..."

    #return
    return eval

#################################################################################################################
# this function gets the uniprot sequence from webpage.
#################################################################################################################
def get_uniprot_seq(uniprot):
   print uniprot
   fasta_url = 'http://www.uniprot.org/uniprot/' + uniprot + '.fasta'
   webFile = urllib.urlopen(fasta_url)
   lines = webFile.read()

   genename = ''
   if len(lines.split('\n')) > 1:
      #print "I AM HERE"
      first_line = lines.split('\n')[0]
      #print first_line
      splitline = first_line.split()
      #print splitline
      splitfeld = splitline[0].split('|')
      #print splitfeld
      genename = splitfeld[2]
      if 'Uncharacterized' in first_line: 
          print 'Uncharacterized'
   

   file = open(uniprot + '.fasta','w')
   file.write(lines)
   return genename


#################################################################################################################
def main():
    if (len(sys.argv) != 3): # if no input
        print " This script needs the following:"
        print " (1) Uniprot list file, "
        print " (2) output prefix "
        print " # of arguments = " + str(len(sys.argv)-1)
        return

    uniprotlistfile = sys.argv[1]
    output = sys.argv[2]

    file1 = open(uniprotlistfile,'r')
    uniprotlist  =  file1.readlines()

    outputmatrixfile = output + '.matrix.csv' 
    file2 = open(outputmatrixfile,'w')

    outputlogfile = output + '.log.txt' 
    file_log = open(outputlogfile,'w')

    ## get fasta files from the web.  
    N = len(uniprotlist)
    genenamelist = []
    for i in range(N):
        uniprot1 = uniprotlist[i].strip('\n')
        uniprotfile1 =  uniprot1 +".fasta" 
        genename1 = get_uniprot_seq(uniprot1)
        genenamelist.append(genename1)

    # calculate blast score for pairs.
    for i in range(N):
        uniprot1 = uniprotlist[i].strip('\n')
        genename1 = genenamelist[i] 
        uniprotfile1 =  uniprot1 +".fasta"
        if os.path.getsize(uniprot1 +".fasta") == 0:
           continue
        for j in range(i,N):
        #for j in range(0,N):
            uniprot2 = uniprotlist[j].strip('\n')
            genename2 = genenamelist[j] 
            uniprotfile2 =  uniprot2 +".fasta"
            #uniprot2 = uniprotlist[j].strip('\n')
            #uniprotfile2 =  uniprot2 +".fasta"
            #genename2 = get_uniprot_seq(uniprot2)
            if os.path.getsize(uniprot2 +".fasta") == 0:
               continue
            eval = seq_align(uniprotfile1, uniprotfile2)
            print uniprot1, uniprot2, eval
            print genename1, genename2, eval
            #file_log.write( uniprot1+', '+uniprot2+', '+str(eval)+'\n' )
            file_log.write( genename1+', '+genename2+', '+str(eval)+'\n' )
            file2.write(str(eval))
            if (j != N): 
                file2.write(', ')
        file2.write('\n')
    return 
#################################################################################################################
#################################################################################################################
main()
