#! /usr/bin/python
import sys
import gzip

#################################################################################################################
def read_write_ism(input_file, output_ex, chunk_num):
    print "input file ="+input_file
    print "chunk_num ="+str(chunk_num)

    file1 = open(input_file,'r')
 
    lines  =  file1.readlines()
    
    count = int(0)
    count_file = int(0)
    for line in lines:
        if (count == 0):
            if (count_file < 10):
                str_count = "00"+str(count_file)
            elif (count_file > 10 and count_file< 100):
                str_count ="0"+str(count_file)
            elif (count_file > 100 and count_file< 1000):
                str_count =str(count_file)
            else:
                "edit this script to add more zeros to the output file names"

            output_file = output_ex+"_chunk"+str_count+".ism"
            print "open for writing " + output_file 
            file2 = open(output_file,'w')
            count_file=count_file + 1

        file2.write(line)
        count=count+1

        if (count > chunk_num):
            file2.close()
            print "close " + output_file 
            count = int(0)


    print str(count_file) + " output file were produced"
    return 
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 4: # if no input
        print "This Script reads in a file and brakes the file into chunks of NUM"
        print "  (1) Input file: suported formates (ISM)"
        print "  (2) Output extention"
        print "  (3) NUM "
        print len(sys.argv)
        return
    
    inputfile  = sys.argv[1]
    output_ex  = sys.argv[2]
    chunk_num  = int(sys.argv[3])
    namesplit  = inputfile.split('.')
    l = len(namesplit)
    if (namesplit[l-1] == "ism"):
       read_write_ism(inputfile,output_ex,chunk_num)
    else:
       print "ERROR: "+ inputfile + "is not a *.ism file"

    
    
#################################################################################################################
#################################################################################################################
main()
