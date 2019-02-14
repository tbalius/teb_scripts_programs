
import sys
import sph_lib as sph
#import mol2 
#import pdb_lib as pdb
import random

# Written by Trent E. Balius, Shoichet Lab, UCSF, in 2019.

def random_samp(p,n):
    print "in random_samp" 
    h = 0
    for i in range(n):
           ran = random.random()
           if (ran <= p):
               print "ran:", ran
               h = h + 1

    return h

def main():
    if len(sys.argv) != 4: # if no input
       print "ERORR: there needs to be 3 inputs: probablity that its a hit, number of molecules tested, number of times to run "
       print " python /nfs/home/tbalius/zzz.scripts/error_estamates.py 0.37 16 1000"
       exit()

    prob          = float(sys.argv[1])
    num_in_sample = int(sys.argv[2])
    num_of_sample = int(sys.argv[3])
    print "prob,num_in_sample,num_of_sample",prob,num_in_sample,num_of_sample  
    if (prob > 1.0): 
        "error. prob must be less than 1.0"
 
    samples = []
    E = 0
    E2 = 0
    for i in range(num_of_sample):
        numhits = random_samp(prob,num_in_sample)
        samp_hitrate = float(numhits)/float(num_in_sample)
        print "numhits, num_in_sample, samp_hitrate:",numhits, num_in_sample, samp_hitrate
        E = E + samp_hitrate
        E2 = E2 + samp_hitrate**2.0
        samples.append(samp_hitrate)
    E = E / float(num_of_sample)
    E2 = E2 / float(num_of_sample)
    var = E2 - E**2.0
    standdev = var**(1./2.)
    print "E, E2, var, standdev", E, E2, var, standdev

main()
