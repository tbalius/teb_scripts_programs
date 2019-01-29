#! /usr/bin/python
import sys
import gzip

#################################################################################################################
def read_write_db2(input_file, output_prefix,namelist):
    print "input file ="+input_file

    file1 = open(input_file,'r')
 
    lines  =  file1.readlines()
    name =""
    count = int(0)
    count_file = int(0)
    flag_Mfirst = True # we want to only assign the name if it is the frist M line, and the first after the E line
    flag_write = True
    for line in lines:
        if (count == 0):
            if (line[0] == "M"):
                if (flag_Mfirst):
                   name = line.split()[1].split('.')[0]
                   if not (name in namelist):
                      flag_write = False
                   flag_Mfirst = False 
            if (flag_write):
              print "name ("+name+") IS in namefile."
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
            else:
              print "name ("+name+") is NOT in namefile."

        if (flag_write):
            file2.write(line)
        #else don't print the lines
        count=count+1

        #print line[0:4]
        if (line[0:1] == "E"):
        #if (line[0:4] == "M NC"):
            print line
            if (flag_write):
               file2.close()
               print "close " + output_file 
            name =""
            flag_write = True
            flag_Mfirst = True
            count = int(0)


    print str(count_file) + " output file were produced"
    return 
#################################################################################################################
#################################################################################################################
def read_list(input_file):
    file1 = open(input_file,'r')
    lines  =  file1.readlines()
    listname = []
    for line in lines:
         name = line.split('.')[0]
         if not (name in listname):
            listname.append(name)
    return listname
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 4: # if no input
        print "This Script reads in a file and brakes the file into chunks '^M NC'"
        print "  (1) Input file: suported formates (db2)"
        print "  (2) Output extention"
        print "  (3) Input file with list of zinc names"
        print len(sys.argv)
        return
    
    inputfile  = sys.argv[1]
    output_prefix  = sys.argv[2]
    listfile   = sys.argv[3]

    listname = read_list(listfile)
    read_write_db2(inputfile,output_prefix,listname)

    
    
#################################################################################################################
#################################################################################################################
main()
