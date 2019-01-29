#! /usr/bin/python2.7

# writen by Trent balius

# remove list from extract all file. 

import sys, os.path

def read_outdock_file_write_extract_all(path,infilename,outfile,maxenergy):
#def read_outdock_file_write_extract_all(path,infilename,extractfilename,maxenergy):

    infile = open(infilename,'r')
    lines = infile.readlines()
    infile.close()

#   if (os.path.exists(extractfilename)):
#      outfile = open(extractfilename,'a')
#   else:
#      outfile = open(extractfilename,'w')

    flag_read = False
    for line in lines:
        splitline = line.split()

        if len(splitline) ==0:
            continue

        if "we" == splitline[0]: # we reached the end of the file, docking results.
             flag_read = False

        if flag_read:         
          if len(splitline) == 21:
             energy = float(splitline[20])
             if (energy < maxenergy): 
                outfile.write("%s %s\n"%(path,line.strip('\n')))

        if  "mol#" == splitline[0]: # start of docking resutls
             flag_read = True

#   outfile.close()
    return 

def main():
   if len(sys.argv) != 4:
      print "error:  this program takes 3 argument "
      print "(1) dirlist where outdock file are.  "    
      print "(2) name of the extract all file to be written.  "    
      print "(3) max_energy to be printed.  "    
      exit()
   
   filename1     = sys.argv[1]
   output        = sys.argv[2]
   max_energy    = float(sys.argv[3])
   if (os.path.exists(output)):
       print "%s exists. stop. " % output
       exit()
   print "(1) dirlist = " + filename1
   print "(2) output = "  + output
   print "(3) energy threshold = %6.3f" % max_energy
   fh = open(filename1)  

   outfile = open(output,'w')
   for line in fh:
       print line
       #splitline = line.split() 
       pathname = line.split()[0]
       filename = line.split()[0]+'/OUTDOCK'
       #read_outdock_file_write_extract_all(pathname,filename,output,max_energy)
       read_outdock_file_write_extract_all(pathname,filename,outfile,max_energy)
   outfile.close()


main()

