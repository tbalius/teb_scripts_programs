
import sys,os

## Writen by Trent Balius in the Shoichet Group
## calculates the tanamoto matrics. 
## fingerprint are calculated with chemaxon
## this uses a simular chemaxon comand as sea.  
## bit comparisons are calculated in python

#this function converts a string of ones and zeros to a bit
def str_to_bit(s):
#    if len(s) != 8:
#       print "warning: sting not right length"
##       print "error: sting not right length"
##       exit()
    
    ## check that the string is all zerros and ones
    for c in s:
        if not (int(c)==1 or int(c)==0):
           print "error: string not zerros and ones"
           exit()

    # note the 2^7 = 10000000
    #          2^6 = 01000000
    #          2^5 = 00100000
    #          ... 
    #      1 = 2^0 = 00000001
    #            0 = 00000000

    #i = 7 # start at 7
    i = len(s) -1 # start at 7
    #print i
    b_int = int(0)
    for c in s:
        #print bin(b_int)
        x = int(c)
        if i >= 0: 
           b_int = b_int + ((2**i) * x)
        i = i -1

    b = bin(b_int)
    #print b_int, b
    return b,b_int

# this function counts the number of ones in the bitstring
def num_bit_ones(bitstring):
    count = 0
    for c in bitstring:
        if (c!='1'):
           continue
        count = count + 1
    return count

# this function computes the tanimoto between to fingerprints
def tanimoto(fp1,fp2):
    fp1_bits = fp1.split('|')
    fp2_bits = fp2.split('|')

    if len(fp1_bits) != len(fp2_bits):
       print "ERROR: bits do not agree in lenth"

    or_num_one  = 0
    and_num_one = 0
    for i in range(len(fp1_bits)):
        #print fp1_bits[i]
        bit1,int1 = str_to_bit(fp1_bits[i])
        bit2,int2 = str_to_bit(fp2_bits[i])
        and_bit = bin(int1 & int2)
        and_num_one = and_num_one + num_bit_ones(and_bit)
        #print str(bit1) + " AND " + str(bit2) + " = " + str(bin(int1 & int2)) + ', ones = ' + str(num_bit_ones(and_bit))
        or_bit  = bin(int1 | int2)
        or_num_one = or_num_one + num_bit_ones(or_bit)
        #print str(bit1) + " OR " + str(bit2) + " = " + str(bin(int1 | int2)) +', ones = ' + str(num_bit_ones(or_bit))
        #print str(bin(bit1)) + " AND " + str(bin(bit2))
    #print and_num_one, or_num_one   
    TC = float(and_num_one) / float(or_num_one)
    #print and_num_one, or_num_one, TC
    return TC

## this function call chemaxon and computes a fingerprint
def fingerprint(SmilesString):

    # this will get the users name. need to write temp file
    name = os.popen('whoami').readlines()[0].strip()
    #print name
    #Generatemd = "/nfs/software/jchem/5.10.3/bin/generatemd"
    Generatemd = "/nfs/soft/jchem/jchem-5.10.3/bin/generatemd"
    # write smiles to file
    fh = open("/tmp/"+ name +"/temp.smi",'w')
    fh.write(SmilesString+'\n')
    fh.close()

    #os.popen("/raid3/software/openbabel/openbabel-2.2.1-32/bin/babel -ismi /tmp/tbalius/temp.smi -osdf /tmp/tbalius/temp.sdf -d")
    #os.popen("/raid3/software/openbabel/openbabel-2.2.1-32/bin/babel -isdf /tmp/tbalius/temp.sdf -osmi /tmp/tbalius/temp2.smi -d")
 
    comand = Generatemd + " c /tmp/" + name + "/temp.smi -k ECFP -2"
    print "runing the comand:"+comand
    output = os.popen(comand).readlines()
    #print "output:"+str(output)
    fp = output[0].strip('\n')
    #print fp
    return fp

## this function reads in smiles and writes out the footprints.
## it returns a footprint vector
def get_fp(infile,outfile):
  fpvec = []
  file = open(infile,'r')
  lines = file.readlines()
  file.close()
  file1 = open(outfile,'w')
  for line in lines:
     splitline = line.split()
     if len(splitline) > 2:
        print "ERROR:len(smiles) > 2"
        exit()
     print splitline

     smiles = splitline[0]
     #print "simles = " + str(smiles);
     fp = fingerprint(smiles)
     #print "fingerprint = " + str(fp);
     file1.write("fingerprint = " + str(fp)+'\n')
     fpvec.append(fp)
  file1.close()
  return fpvec

def main():
  if not (len(sys.argv) == 4 or len(sys.argv) == 5): # if no input
     print "ERORR"
     print "syntexs: python tanimoto_cal_axon.py -one smiles1 outputprefix"
     print "         this produces a squere symestric matrix of set1 with itself. "
     print "syntexs: python tanimoto_cal_axon.py -two smiles1 smiles2 outputprefix"
     print "         this produces a rectangular non-symestric matrix of set1 to set2"
     return

  oneortwo    = sys.argv[1]
  smilesfile1 = sys.argv[2]
  if oneortwo == "-one":
    outfileprefix = sys.argv[3]
  elif  oneortwo == "-two":
    smilesfile2 = sys.argv[3]
    outfileprefix = sys.argv[4]
  else:
      print "the frist parameter must be -one or -two."
      exit()

  outfile1 = outfileprefix +'.1.fp'
  fpvec1 = get_fp(smilesfile1,outfile1)
  if oneortwo == "-one":
    fpvec2 = fpvec1
  if oneortwo == "-two":
    outfile2 = outfileprefix +'.2.fp'
    fpvec2 = get_fp(smilesfile2,outfile2)

  outfileM = outfileprefix +'.matrix'


  file1 = open(outfileM,'w')
  for fp1 in fpvec1:
     flag_frist = True 
     for fp2 in fpvec2:
        TC = tanimoto(fp1,fp2)
        if (flag_frist):
           flag_frist = False
        else:
           file1.write(',')
        file1.write('%f' % TC )
     file1.write('\n' )
  file1.close()
#main()

