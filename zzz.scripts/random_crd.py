import sys
import random
#import pdb_lib

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



def coord_writer(filename,cords,name):

 print ("OUT coord_writer")
 filec = open(filename,'w')
 filec.write('%s\n'%(name))
 filec.write('%7d\n'%(len(cords)))
# lines = file.readlines()
 for i,crd in enumerate(cords):
     filec.write('%12.7f%12.7f%12.7f'%(crd.x,crd.y,crd.z))
     if (((i+1) % 2) == 0): 
         #print i
         filec.write('\n')
 if (((i+1) % 2) != 0):
     #print i
     filec.write('\n')
 filec.close()
# frist read in numbers


 return 


def main():

    if (len(sys.argv) != 4): # if no input
        print (" (1) number of atoms")
        print (" (2) tightness of random generated cords")
        print (" (3) crd output file  ");
        return

    num            = int(sys.argv[1])
    tight          = float(sys.argv[2])
    output         = sys.argv[3]

    j = 0
    crds = []
    for i in range(0,num):
            #print "j=",j,"i=",i 
            x = tight*(random.random()-0.5)
            y = tight*(random.random()-0.5)
            z = tight*(random.random()-0.5)
            crd = cord(x,y,z) 
            crds.append(crd)

    coord_writer(output,crds,"random crds.")

    return;
#################################################################################################################
#################################################################################################################
main()

