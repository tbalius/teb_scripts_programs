#! /usr/bin/python
import sys
import gzip

#################################################################################################################
def read_write_db2(input_file, output_prefix):
    print "input file ="+input_file

    file1 = open(input_file,'r')
 
    lines  =  file1.readlines()
    name =""
    count = int(0)
    count_file = int(0)
    flag_Mfirst = True # we want to only assign the name if it is the frist M line, and the first after the E line

    for line in lines:
        if (count == 0):
            if (line[0] == "M"):
                if (flag_Mfirst):
                    name = line.split()[1]
                    flag_Mfirst = False 
            if (count_file < 10):
                str_count = "000"+str(count_file)
            elif (count_file >= 10 and count_file< 100):
                str_count ="00"+str(count_file)
            elif (count_file >= 100 and count_file< 1000):
                str_count ="0" + str(count_file)
            elif (count_file >= 1000 and count_file< 10000):
                str_count = str(count_file)
            else:
                print "edit this script to add more zeros to the output file names"
                sys.exit()

            output_file = output_prefix+"_"+name+"_chunk"+str_count+".db2"
            print "open for writing " + output_file 
            file2 = open(output_file,'w')
            count_file=count_file + 1

        file2.write(line)
        count=count+1

        #print line[0:4]
        if (line[0:1] == "E"):
        #if (line[0:4] == "M NC"):
            print line
            file2.close()
            print "close " + output_file 
            name =""
            count = int(0)
            flag_Mfirst = True 


    print str(count_file) + " output file were produced"
    return 
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print "This Script reads in a file and brakes the file into chunks '^M NC'"
        print "  (1) Input file: suported formates (db2)"
        print "  (2) Output prefix"
        print len(sys.argv)
        return
    
    inputfile  = sys.argv[1]
    output_prefix  = sys.argv[2]
    read_write_db2(inputfile,output_prefix)

    
    
#################################################################################################################
#################################################################################################################
main()
