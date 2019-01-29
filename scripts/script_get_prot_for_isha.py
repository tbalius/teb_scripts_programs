
import os,sys
import os.path

#curl 'http://zinc15.docking.org/substances.txt:zinc_id+protomers' -F 'count=100' -F 'zinc_id=ZINC000465129598'

def get_prot(filen):

    # open file
    fh = open(filen,'r') # file handel
    prot = [] # list of protomers
    # loop over lines of the file
    for line in fh: 
        splitline = line.split() # break the line on white space
        if len(splitline)>1:  # if there are more then 3 columns in the line 
            for i in range(1,len(splitline)):
                prot.append(splitline[i]) # then add all the subsiquent columns to the list of protomers. 

    return prot


def main():

   if len(sys.argv) != 3:
      print "Error"
      exit()
   iname = sys.argv[1]
   oname = sys.argv[2]
   print "input filename = " + iname
   print "output filename = " + oname
   plist = get_prot(iname)
   db2flist = []
   ofh = open(oname,'w') # output file handel
   for p in plist:
       print p
       lp = len(p)
       if lp < 7:
          print "Error"
          exit()
       dir1 = p[lp-2:lp]
       dir2 = p[lp-4:lp-2]
       dir3 = p[lp-6:lp-4]
       print dir1, dir2, dir3

       # /nfs/dbraw/zinc/49/76/33/419497633.db2.gz
       db2file = "/nfs/dbraw/zinc/"+dir3+"/"+dir2+"/"+dir1+"/"+p+".db2.gz"
       if os.path.exists(db2file):
           #os.system('ls '+ db2file) 
           db2flist.append(db2file)
           ofh.write('%s\n'%(db2file))
   ofh.close() 
    

main()
