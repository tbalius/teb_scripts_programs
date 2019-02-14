import sys
import pdb_lib

# Written by Trent E. Balius in the Shoichet Lab at UCSF
# this is not done.  started on April 6, 2018

class cord:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class frame:
    def __init__(self, cords):
        self.cords = cords ## list of coordenates 



def mdcrd_writer(filename,cords,name):

 print "OUT coord_writer"
 filec = open(filename,'w')
 filec.write('%s\n'%(name))
 filec.write('%7d\n'%(len(cords)))
# lines = file.readlines()
 i = 0
 for crd in cords:
     for valcrd in [crd.x,crd.y,crd.z]:
       filec.write('%8.3f'%(valcrd))
       if (((i+1) % 10) == 0): 
         #print i
         filec.write('\n')
       i=i+1
 if (((i+1) % 10) != 0):
     #print i
     filec.write('\n')
 filec.close()
# frist read in numbers


 return 


def main():

    if (len(sys.argv) != 4): # if no input
        print " (1) pdb file name,"
        print " (1) crd file name,"
        print " (2) output file  ";
        return

    pdbfilename    = sys.argv[1]
    crdfilename    = sys.argv[2]
    output         = sys.argv[3]

    #cl = pdb_lib.read_pdb(pdb_file)
    pdb = pdb_lib.read_pdb(pdbfilename)[0]
    size = len(pdb) 

    j = 0
    crds = []
    for i in range(size):
            #print "j=",j,"i=",i 
            x = pdb[i].X 
            y = pdb[i].Y 
            z= pdb[i].Z 
            crd = cord(x,y,z) 
            crds.append(crd)

    mdcrd_writer(crdfilename,crds,"from "+pdbfilename)

    return;
#################################################################################################################
#################################################################################################################
main()

