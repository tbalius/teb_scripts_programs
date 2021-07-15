import math, sys
import os.path

from math import sqrt

# Write by Trent E. Balius.  

def read_write_mol2_file(filename1,fileval,valtype,output,nameval):

    # now lets read in the rmsds.
    file1 = open(fileval,'r')
    dict_val = {}
    print 
    for line in file1: 
         splitline = line.split()
         print splitline
         name = splitline[0].replace(':','')
         val = splitline[1]
         if valtype == "float":
            dict_val[name] = float(val)
         elif valtype == "int":
            dict_val[name] = int(val)
         elif valtype == "str":
            #dict_val[name] = str(val)
            dict_val[name] = val
         else: 
            print ("valtype %s is not valid"%(valtype))
         
    #print dict_val     
    file1.close()

    if valtype == "float":
       FORMATESTRING = "##########%22s     %f\n" 
    elif valtype == "int":
       FORMATESTRING = "##########%22s     %d\n" 
    else:
       FORMATESTRING = "##########%22s     %s\n"

    
    # now lets re-read in the poses mol2 file and write it back out 
    # putting in the alternative rank and the rmsds in the header

    file2 = open(output+".mol2",'w')
    file3 = open(filename1,'r')
    name = ''   
    count = 1
    for line in file3:
         linesplit = line.split()
         if (len(linesplit) > 0):
             if ("@<TRIPOS>MOLECULE" in line):
                 #name = linesplit[2].split('.')[0]
                 #print name dict_val[name]
                 #print name, dict_val
                 #exit()
                 #if name in dict_val: 
                 #if name in dict_val: 
                    #file2.write("##########%22s     %f\n" % (nameval+":",dict_val[name]))
                 #else:
                    #print name 
                 #   file2.write("##########%22s     NA\n" % (nameval+":"))
                 file2.write(FORMATESTRING % (nameval+":",dict_val[str(count)]))
                 count=count+1
         file2.write(line)
    file3.close()
    file2.close()

    return 
#################################################################################################################
#################################################################################################################
def main():
    if (len(sys.argv) != 6): # if no input
        print " (1) mol2 file name," 
        print " (2) file name with stuff to add(formate: 'name value')";
        print " (3) value type: float, int, string"
        print " (4) output prefix ";
        print " (5) tc name ";
        return

    filename1 = sys.argv[1]
    fileval   = sys.argv[2]
    valtype   = sys.argv[3]
    output    = sys.argv[4]
    name      = sys.argv[5]

    print(" filename1 = %s\nfileval   = %s\nvaltype   = %s\noutput    = %s\nname      = %s\n"%(filename1,fileval,valtype,output,name))

    if valtype != "float" and valtype != "int" and valtype != "str":
       print "valtype must be one of the following: float, int, or str. " 
       exit()
       #print "we will use valtype of string."
       #valtype = "str"

    read_write_mol2_file(filename1,fileval,valtype,output,name)


    return; 
#################################################################################################################
#################################################################################################################
main()
