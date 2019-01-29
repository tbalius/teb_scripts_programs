
import sys,os, math

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

## this function call chemaxon and computes the molecular Mass of the molecule
def molecularMass(SmilesString):
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

    comand = Generatemd + " c /tmp/" + name + "/temp.smi -k Mass"
    print "runing the comand:"+comand
    output = os.popen(comand).readlines()
    #print output
    #print "output:"+str(output)
    #outlines = output.split('\n')
    #lastline = outlines[len(outlines)-1]
    lastline = output[len(output) - 1]
    #print lastline
    mass = lastline.split()[1]
    #print mass
    #print fp
    return mass

def heavyAtoms(SmilesString):
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

    comand = Generatemd + " c /tmp/" + name + "/temp.smi -k Heavy"
    print "runing the comand:"+comand
    output = os.popen(comand).readlines()
    #print "output:"+str(output)
    #outlines = output.split('\n')
    #lastline = outlines[len(outlines)-1]
    lastline = output[len(output) - 1]
    heavy = lastline.split()[1]

    print output,outlines,lastline,heavy
    #print fp
    return heavy

#def is_integer(s):
#    try:
#        int(s)
#        return True
#    except ValueError:
#        return False

def check_element(ele):
    elements = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Uut', 'Fl', 'Uup', 'Lv', 'Uus', 'Uuo']
    #print ele, (ele in elements)
    if (ele in elements):
        return True
    return False

## write a new funcition here to calculate the molecular formulae
# /nfs/soft/jchem/jchem-5.10.3/bin/cxcalc formula "CN(C)c1cccc2c(cccc12)S(=O)(=O)NCCCCCCCCCCC(O)=O"
def MolecularFormula(SmilesString):
    cxcalc  = "/nfs/soft/jchem/jchem-5.10.3/bin/cxcalc"
    comand = cxcalc + " formula \""+ SmilesString+"\""
    output = os.popen(comand).readlines()
    lastline = output[len(output) - 1]
    formula = lastline.split()[1]
    return formula

def dictionary_Formula(formula1):
    dict = {}

    flag_n = False
    temp_s = ''
    temp_n = ''
    for i in range(0,len(formula1)):
        s = formula1[i]
        if (s.isalpha() and not flag_n):
           temp_s_old = temp_s
           temp_s = temp_s  + s
           if (not check_element(temp_s) and len(temp_s)>1): # if only one atom of an element then there may not be a number 
              print "not an element: " + temp_s
              if check_element(temp_s_old):
                 print "an element: " + temp_s_old
                 dict[temp_s_old] = int(1)
                 temp_s = s
              else:
                 print "error not an element::"
                 print temp_s_old
                 exit()
           if (i == (len(formula1)-1)): # if at end of sting
              temp_n = 1
              #print temp_s, temp_n 
              #dict[temp_s] = int(temp_n)
        elif (s.isdigit()): 
           temp_n = temp_n + s
           flag_n = True
           #if (i == (len(formula1)-1)): # if at end of string
           #   temp_n = temp_n + s
           #   #print temp_s, temp_n 
           #   #dict[temp_s] = int(temp_n)
        elif (s.isalpha() and flag_n):
           flag_n = False
           dict[temp_s] = int(temp_n)
           print temp_s, temp_n 
           temp_s = s
           temp_n = ''
           if (i == (len(formula1)-1)): # if at end of string
              temp_n = 1
        if (i == (len(formula1)-1)): # if at end of string
           print temp_s, temp_n 
           dict[temp_s] = int(temp_n)
    
    return dict

def compareFormula(formula1,formula2):
    print formula1, formula2
    dict1 = dictionary_Formula(formula1)   
    dict2 = dictionary_Formula(formula2)   

    allkeys = dict1.keys()
    allkeys = allkeys + dict2.keys()

    uniqkeys = []
    for key in allkeys:
        if not key in uniqkeys:
           uniqkeys.append(key)
           print key
    val =  0
    for key in uniqkeys:
        if not key in dict1:
           dict1[key] = 0
        if not key in dict2:
           dict2[key] = 0
        print key, dict1[key], dict2[key], math.fabs(dict1[key]-dict2[key])
        val = val + math.fabs(dict1[key]-dict2[key])
    print "formula diff all = " + str(val)
    #print "heavy = " + str(val)
    return val


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

