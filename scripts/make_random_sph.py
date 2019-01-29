
import sys
import sph_lib as sph
#import mol2 
#import pdb_lib as pdb
import random

def randomomize_sph(sphs,maxval): 
    sphlist = []

    for sph in sphs:
        sphnew = sph
        # used to move it in posive derection only. 
        #sphnew.X = sphnew.X + maxval*random.random()
        #sphnew.Y = sphnew.Y + maxval*random.random()
        #sphnew.Z = sphnew.Z + maxval*random.random()
        # now, it to move in all directions, as below. 
        sphnew.X = sphnew.X + maxval*(random.random()-0.5) # [0,1] -> [-0.5,0.5] -> [-mv/2.0,mv/2.0]
        sphnew.Y = sphnew.Y + maxval*(random.random()-0.5)
        sphnew.Z = sphnew.Z + maxval*(random.random()-0.5) 
        sphlist.append(sphnew)
           
    return sphlist

def main():
    if len(sys.argv) != 4: # if no input
       print "ERORR: there needs to be 3 inputs: sph inputfilename, max random value, outputfilename."
       return

    fileinputsph = sys.argv[1]
    maxval       = float(sys.argv[2])
    fileoutput   = sys.argv[3]
   

    print 'input_sph =' + fileinputsph
    print 'output =' + fileoutput

    list  = sph.read_sph(fileinputsph,'A','A')
    list2 = randomomize_sph(list,maxval)
    sph.write_sph(fileoutput,list2)

main()
