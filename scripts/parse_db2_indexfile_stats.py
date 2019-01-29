#! /usr/bin/python
import sys
import gzip
import os
import os.path

#################################################################################################################
def read_db2_write_stats(input_file, output_file,flagappend):
    print "input file ="+input_file

    if not (os.path.exists(input_file)):
       print input_file+" does not exist."
       return 0,0,0,0
    split_input = input_file.split('.')
    if (split_input[len(split_input)-1]=='gz'):
        file1 = gzip.open(input_file,'r')
    elif (split_input[len(split_input)-1]=='db2'):
        file1 = open(input_file,'r')

    if flagappend:
       file2 = open(output_file,'a')
    else:
       file2 = open(output_file,'w')
 
    lines  =  file1.readlines()
    name =""
    count = int(0)
    count_hier = int(0) # count the hierarchies
    flag_Mfirst = True # we want to only assign the name if it is the frist M line, and the first after the E line
    totavgnumofconf = 0.0
    totcountconf = 0
    totcountset  = 0

    name = ""
    for line in lines:
        splitline = line.split()
        if (count == 0):
            if (line[0] == "M"):
                avgnumofconf = 0.0
                countconf = 0
                countset  = 0
                flag_Conf = False # 
                flag_Set  = False
                if (flag_Mfirst):
                    name = line.split()[1]
                    flag_Mfirst = False 
            #count_file=count_file + 1

        #file2.write(line)
        #count=count+1

        if (line[0:1] == "C"):
            flag_Conf = True 

        if (line[0:1] == "S"):
            flag_Set = True
            flag_Conf = False

        if (line[0:1] == "D"):
            flag_Set = False
 
        if (flag_Conf):
            countconf = countconf+1
            totcountconf = totcountconf+1


        if (flag_Set):
             #print line 
             if len(splitline) == 7:
                #print line
                #print len(splitline)
                numofconf = int(splitline[3])
                #print numofconf
                avgnumofconf = float(numofconf)+avgnumofconf
                countset = countset + 1
                totavgnumofconf = float(numofconf)+totavgnumofconf
                totcountset = totcountset + 1

        #print line[0:4]
        if (line[0:1] == "E"):
            count_hier = count_hier + 1
            avgnumofconf = avgnumofconf/countset
            print "name = %s"%name 
            print "# of Conf = %d"%countconf 
            print "# of set  = %d"%countset 
            print "avg # of confs/set = %f"%avgnumofconf 
            file2.write( "name = %s\n"%name )
            file2.write( "# of Conf = %d\n"%countconf) 
            file2.write( "# of set  = %d\n"%countset )
            file2.write( "avg # of confs/set = %f\n"%avgnumofconf )
            flag_Mfirst = True 


    #print str(count_file) + " output file were produced"
    totavgnumofconf = totavgnumofconf/totcountset
    avgcountconf = totcountconf/count_hier
    avgcountset = totcountset/count_hier
    print "db2 file = %s"%input_file
    print "tot # of Conf = %d"%totcountconf 
    print "tot # of set  = %d"%totcountset 
    print "# of hierarchies = %d"%count_hier
    print "avg # of Conf = %d"%avgcountconf
    print "arg # of set  = %d"%avgcountset
    print "tot avg # of confs/set = %f"%totavgnumofconf 
    file2.write( "\ndb2 file = %s\n"%input_file )
    file2.write( "tot # of Conf = %d\n"%totcountconf )
    file2.write( "tot # of set  = %d\n"%totcountset )
    file2.write( "# of hierarchies = %d\n"%count_hier )
    file2.write( "avg # of Conf = %d\n"%avgcountconf )
    file2.write( "arg # of set  = %d\n"%avgcountset )
    file2.write( "tot avg # of confs/set = %f\n"%totavgnumofconf )
    file2.write( "\n" )
    file1.close()
    file2.close()
    return totcountconf,totcountset,totavgnumofconf,count_hier
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print "This Script reads in a file and writes out stats '^M NC'"
        print "  (1) Input file: db2 index file, file with one paths to db2 file on each line"
        print "  (2) Output file for stat file"
        print len(sys.argv)
        return
    
    inputfile  = sys.argv[1]
    outputfile = sys.argv[2]
    
    infile = open(inputfile,'r')

    flagapp = False
    afcountC = 0
    afcountS = 0 
    afcountH = 0 # hierarchies
    afavgnumofCperS = 0.0
    filecount = 0
    for line in infile:
       db2file = line.strip()
       print db2file
       countC,countS,avgnumofCperS,countH = read_db2_write_stats(db2file,outputfile,flagapp)
       afcountC = afcountC + countC
       afcountS = afcountS + countS
       afcountH = afcountH + countH
       afavgnumofCperS = afavgnumofCperS + avgnumofCperS
       filecount = filecount + 1
       flagapp = True
    afavgnumofCperS = afavgnumofCperS/filecount
    print "all file tot # of Conf = %d"%afcountC
    print "all file tot # of set  = %d"%afcountS
    print "all file # of hierarchies = %d"%afcountH
    print "all file avg # of Conf = %d"%(afcountC/afcountH)
    print "all file arg # of set  = %d"%(afcountS/afcountH)
    print "all file tot avg # of confs/set = %f"%afavgnumofCperS
    file2 = open(outputfile,'a')
    file2.write( "\n\nall file tot # of Conf = %d\n"%afcountC )
    file2.write( "all file tot # of set  = %d\n"%afcountS )
    file2.write( "all file # of hierarchies = %d\n"%afcountH )
    file2.write( "all file avg # of Conf = %d\n"%(afcountC/afcountH) )
    file2.write( "all file arg # of set  = %d\n"%(afcountS/afcountH) )
    file2.write( "all file tot avg # of confs/set = %f\n"%afavgnumofCperS )
    infile.close()
    file2.close() 

    
    
#################################################################################################################
#################################################################################################################
main()
