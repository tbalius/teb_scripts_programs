#! /usr/bin/python
import sys
import gzip

#################################################################################################################
def read_db2_write_stats(input_file, output_file):
    print "input file ="+input_file

    split_input = input_file.split('.')
    if (split_input[len(split_input)-1]=='gz'):
        file1 = gzip.open(input_file,'r')
    elif (split_input[len(split_input)-1]=='db2'):
        file1 = open(input_file,'r')
    file2 = open(output_file,'w')
 
    lines  =  file1.readlines()
    name =""
    count = int(0)
    count_file = int(0)
    flag_Mfirst = True # we want to only assign the name if it is the frist M line, and the first after the E line
    totavgnumofconf = 0.0
    totcountconf = 0
    totcountset  = 0

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
            count_file=count_file + 1

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
            avgnumofconf = avgnumofconf/countset
            print "# of Conf = %d"%countconf 
            print "# of set  = %d"%countset 
            print "avg # of confs/set = %f"%avgnumofconf 
        #if (line[0:4] == "M NC"):
            #print line
            #file2.close()
            #print "close " + output_file 
            #name =""
            #count = int(0)
            flag_Mfirst = True 


    #print str(count_file) + " output file were produced"
    totavgnumofconf = totavgnumofconf/totcountset
    print "tot # of Conf = %d"%totcountconf 
    print "tot # of set  = %d"%totcountset 
    print "tot avg # of confs/set = %f"%totavgnumofconf 
    return 
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print "This Script reads in a file and writes out stats '^M NC'"
        print "  (1) Input file: suported formates (db2)"
        print "  (2) Output file for stat file"
        print len(sys.argv)
        return
    
    inputfile  = sys.argv[1]
    outputfile = sys.argv[2]
    read_db2_write_stats(inputfile,outputfile)

    
    
#################################################################################################################
#################################################################################################################
main()
