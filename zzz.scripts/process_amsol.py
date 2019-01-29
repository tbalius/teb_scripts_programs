import mol2  ## this is a libary Trent Balius and Sudipto Mukherjee wrote. 
import math, sys
import os.path
import gzip
from math import sqrt

#################################################################################################################
# Written by Trent E Balius, B. Shoichet lab, Nov. 2013
# this script reads in a amsol outputfiles (wat and hex)
# and processes them. 
# this is a replacement for the following scripts:  
#   $DOCK_BASE/etc/SubstrSolv2.pl
# consider adding in writing amsol input files and runing amsol itself in future.  
#################################################################################################################

## 
def is_int(a):
    """Returns true if a can be an integer"""
    try:
        int (a)
        return True
    except:
        return False


#################################################################################################################
#################################################################################################################
def process_amsol_file(file,outputprefix,watorhex):
    # reads in data amsol output.

    if not (os.path.exists(file)):
        print file + "does not exist. \n\n Exiting script . . ."
        exit()

    ## read in both gzip and uncompresed file.
    splitfile = file.split('.')
    N = len(splitfile)-1
    print splitfile[N]
    if (splitfile[N] == 'gz'):
       file1 = gzip.open(file, 'rb')
    else:
       file1 = open(file,'r')

    ## open up output file
    outputfilename = outputprefix +watorhex +str(".log") 
    file2 = open(outputfilename,'w')
    lines  =  file1.readlines()
    count = 1

    name = ''
    numatoms = 0
    list = []
    list = []

    ## loops over the file
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) == 2 and is_int(linesplit[1]) and name == ''): # get the name and atom cout.
             file2.write(line)
             name     = linesplit[0]
             numatoms = int(linesplit[1])
         if (len(linesplit) == 8 and is_int(linesplit[0]) ):  ## this gets that per-atom brake down of solvation calculation.
             file2.write(line)
             list.append(linesplit)
         elif (len(linesplit) == 5 and linesplit[0] == "CS" and linesplit[1] == "Contribution" ): ## get it's the total info
             #total = linesplit 
             file2.write(line)
         elif (len(linesplit) == 6 and linesplit[0] == "Total:" ): ## get it's the total info
             total = linesplit 
             file2.write(line)
    file2.close()
            
    return list,total,name,numatoms

#################################################################################################################
#################################################################################################################
def diff_amsol_files(atom_listwat,totwat,atom_listhex,tothex,name,numatom,outputprefix):
    ## this function will compare hex with wat and predue an output.solv file:
    ## *.solv has the following format:
    ##
    ## 1M17  52  0.0   -16.55   436.86     7.27    -9.28
    ## -0.1645   -0.19  19.39    0.56    0.37
    ## -0.6804    0.77   5.64   -0.98   -0.21
    ## -0.3203    0.27   6.50   -0.84   -0.57
    ## -0.1644   -0.92  13.19    0.70   -0.22 
    ##
    ##
    ## here the frist line is name, atom count, formal charge, delta Polarization free energy, 
    ## the following lines are the per-atom brake down
    ## column 1 is partail charge from hex
    ## column 2 is delta (wat - hex) Polarization free energy (kcal) 
    ## column 3 is Area  (CD)  (Ang**2) from hex
    ## column 4 is G-CD (kcal)
    ## column 5 is Total Solv. free energy (kcal)

    N = len(atom_listwat)
    if len(atom_listwat) != len(atom_listwat):
        print "Error: len(atom_listwat) != len(atom_listwat):" + str(len(atom_listwat))+" != "+str(len(atom_listhex))
        exit()

    if N != numatom:
        print "Error: len(atom_listwat) != numatom: " + str(N) +" != "+str(numatom)
        exit()

    fileline = ''## generate string output to write to a file

    for i in range(N):
        for j in range(0,8):
           print atom_listwat[i][j] +" -- "+ atom_listhex[i][j] +';  ',
        print "\n",

    # initialize the arrays.
    Chghex  = []; Polhex  = []; SAA     = []; 
    Apolhex = []; Polwat  = []; Apolwat = [];
    Pol     = []; Apol    = []; Atmsolv = [];
    for i in range(N):
        Chghex.append(0.0)
        Polhex.append(0.0)
        SAA.append(0.0)
        Apolhex.append(0.0)
        Pol.append(0.0)
        Polwat.append(0.0)
        Apolwat.append(0.0)
        Pol.append(0.0)
        Apol.append(0.0)
        Atmsolv.append(0.0) 

    Chghexsum = 0
    Polhexsum = 0
    SAAsum = 0
    apolsum = 0
    energy_sum = 0
    totpol = 0
    totapol = 0
    tot = 0
    for i in range(N):
           Chghex[i]  = float(atom_listhex[i][2]);
           Polhex[i]  = float(atom_listhex[i][3]);
           SAA[i]     = float(atom_listhex[i][4]);
           Apolhex[i] = float(atom_listhex[i][5]);
           Polwat[i]  = float(atom_listwat[i][3]);
           Apolwat[i] = float(atom_listwat[i][5]);
           ## sums
           Chghexsum = Chghexsum + Chghex[i]
           Polhexsum = Polhexsum + Polhex[i]
           SAAsum = SAAsum + SAA[i]
           apolsum = apolsum + Apolhex[i]
           energy_sum = energy_sum + float(atom_listhex[i][6]);

    print tothex
    print Chghexsum, Polhexsum, SAAsum, apolsum, energy_sum 
    print len(tothex)
    cs_coeff = (float(tothex[4]) - apolsum)/float(tothex[3])
    print "CS coeff: ",cs_coeff;

    for i in range(N): # do substraction
           Pol[i] = Polwat[i] - Polhex[i];
           totpol = totpol + Pol[i];
           Apol[i] = Apolwat[i] - Apolhex[i] - cs_coeff * SAA[i];
           totapol = totapol + Apol[i];
           Atmsolv[i] = Pol[i] + Apol[i];
           tot = tot + Atmsolv[i];

    ## write out the solvation file 
    file = open(outputprefix+'.solv','w')
    file.write( "%s %3d %4.1f %8.2f %8.2f %8.2f %8.2f\n" % (name,numatom,float(totwat[1]),totpol,float(totwat[3]),totapol,tot))  # formal charge is the same for water or hexadecane
    for i in range(N):
           file.write("%8.4f%8.2f%7.2f%8.2f%8.2f\n" % (Chghex[i],Pol[i],SAA[i],Apol[i],Atmsolv[i]))
    file.close()


#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 4: # if no input
        print " This script needs the following:"
        print " (1) amsol water output file "
        print " (2) amsol hex output file "
        print " (2) outputprefix "
        return

    filenamewat    = sys.argv[1]
    filenamehex    = sys.argv[2]
    outputprefix   = sys.argv[3]

    atom_list_wat,tot_wat,name_wat,numat_wat = process_amsol_file(filenamewat,outputprefix,"wat")
    atom_list_hex,tot_hex,name_hex,numat_hex = process_amsol_file(filenamehex,outputprefix,"hex")

    if (name_hex != name_wat or numat_hex != numat_wat):
        print "Error: Name or Atom counts do not agree"
    #else:
        print "Wat-name      = " + name1 
        print "Wat-atom cout = " + str(numat1)
        print "Hex-name      = " + name2 
        print "Hex-atom cout = " + str(numat2)

    diff_amsol_files(atom_list_wat, tot_wat, atom_list_hex, tot_hex, name_wat, numat_wat, outputprefix)

    return 
#################################################################################################################
#################################################################################################################
main()
