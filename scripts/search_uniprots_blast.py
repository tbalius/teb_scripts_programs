import os,sys,urllib,urllib2


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

# this function gets the uniprot from webpage.
def get_uniprot(uniprot):
   print uniprot
   fasta_url = 'http://www.uniprot.org/uniprot/' + uniprot + '.fasta'
   webFile = urllib.urlopen(fasta_url)
   lines = webFile.read()
   file = open(uniprot + '.fasta','w')
   file.write(lines)
   return 



if ( len(sys.argv) != 3):
    print "needs two uniprot code"
    exit()

uniprot1 = sys.argv[1]
uniprot2 = sys.argv[2]

get_uniprot(uniprot1)
get_uniprot(uniprot2)
eval = seq_align(uniprot1+'.fasta',uniprot2+'.fasta')
print uniprot1, uniprot2, eval

