
#################################################################################################################
## Writen by Trent Balius in the Shoichet Lab, UCSF in 2017
#################################################################################################################
import sys,os
#import sph_lib as sph
#import mol2 
import pdb_lib as pdb

def add_bfactors(pdbatomlist, resids, bfile):

    fh = open(bfile,'r')
    bvals = []
    minv = -99.99
    maxv = 99.99
    for line in fh:
        print line
        splitline = line.split(",")
        tempbfac = float(splitline[1])

        # cap max and min values. one reason to do this is not to exceed the pdb bfactor column lenth
        if tempbfac < minv: 
           tempbfac = minv
        if tempbfac > maxv:
           tempbfac = maxv
            
        bvals.append(tempbfac)
    atomcount = 0
    residcount = 0 
    # loop over atomlist and residlist, go though the list side by side by side. 
    # when incountered put in bfal 
    current_id = 0
    flagupdate = False 
    lastid = 0
    while atomcount < len(pdbatomlist) and residcount < len(resids): 

        if (lastid != int(pdbatomlist[atomcount].resnum)): 
           #pdbatomlist[atomcount].bfactor = bvals[residcount]
           flagupdate = False

        if int(pdbatomlist[atomcount].resnum) == int(resids[residcount]): # if current atom is next residue in the resid list
           #pdbatomlist[atomcount].bfactor = bvals[residcount]
           flagupdate = True
           residcount = residcount + 1
        if flagupdate: 
           pdbatomlist[atomcount].bfact = float(bvals[residcount-1])
           print atomcount, pdbatomlist[atomcount].atomnum, pdbatomlist[atomcount].resnum, pdbatomlist[atomcount].bfact, residcount, bvals[residcount-1]
        lastid = int(pdbatomlist[atomcount].resnum)   
        atomcount = atomcount+1
    return pdbatomlist


def main():
    if len(sys.argv) != 5: # if no input
       print "ERORR: there need to be 4 inputs: pdb inputfilename, bfactorfilename(2 colomn:resname,value)  residuelist, outputfileprefix."
       return

    fileinputpdb = sys.argv[1]
    filebfactor  = sys.argv[2]
    res_string   = sys.argv[3]
    fileoutput   = sys.argv[4]

    splitname = fileinputpdb.split('/')[-1].split('.') 
    if len(splitname) != 2:
        print "error pdb file is weird. "
        exit()
    prefix = splitname[0] 

    print 'input_pdb =' + fileinputpdb
    print 'sph prefix =' + prefix
    print 'residue string =' + res_string
    print 'output =' + fileoutput

    residlist = []
    res_string_split = res_string.split(',') 
    print res_string_split
#   if len(res_string_split) == 1: 
#       residlist.append(int(res_string_split[0]))
#   else:
    #print res_string_split
    for s in res_string_split:
       if ('-' in s):
          s_split = s.split('-')
          if (len(s_split) != 2):
             print "something is wrong with residue string."
          else:
             start = int(s_split[0])
             stop  = int(s_split[1])+1
             for i in range(start,stop):
                 residlist.append(i)
       else: 
          residlist.append(int(s)) 

    for i in range(1,len(residlist)):
        if residlist[i-1] > residlist[i]:
           print "uhoh. list is not monotonic"
           exit()

    print residlist
    #exit()

    pdblist_chains = pdb.read_pdb(fileinputpdb)
    pdblist = []
    for chain in pdblist_chains:
         pdblist = pdblist + chain
    pdblist_mod = add_bfactors(pdblist,residlist,filebfactor)
    pdb.output_pdb(pdblist_mod,fileoutput+'.pdb')

main()

