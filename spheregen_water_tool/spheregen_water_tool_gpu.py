#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# this ways copyed and then modified from:
# http://sebsauvage.net/python/gui/#import
# Written by Trent Balius (shoichet lab, 2016) 


import math,os, shutil,os.path 
import pdb_lib

def run_spheregen(num):
    DOCKPATH = "/nfs/home/tbalius/zzz.github/DOCK"
    ligfile = "xtal-lig.mol2"
    recdms = "rec.dms"
    recpdb = "rec.pdb"
    recsph = "rec.sph"
    #recsphpdb = "rec.sph.pdb"
    recsphpdb = "rec.sph."
    name = "rec"

    if not (os.path.isfile("./rec_ori.pdb")):
         os.system('cp rec.pdb rec_ori.pdb')

    #step one generate molecular surface.
    DMS = DOCKPATH+"/proteins/dms/bin/dms"
    flags = " "+recpdb+" -a -n -w 1.0 -v -o "+recdms
    dmscmd = DMS + flags
    print "Run dms"
    os.system(dmscmd)


    # step one generate spheres.
    os.system("rm -rf OUTSPH temp1.ms temp2* temp3.atc rec.sph rec.sph.pdb* showshere.in")

    SPH = DOCKPATH+"/proteins/sphgen/bin/sphgen"

    maxradius = 1.8
    minradius = 1.2

    file1 = open('INSPH','w')
    file1.write("%s\nR\nX\n0.0\n%3.1f\n%3.1f\n%s\n"%(recdms,maxradius,minradius,recsph))
    file1.close()
    print "Run Sphgen"
    os.system(SPH)

    file2 = open("showshere.in",'w')
    file2.write( recsph + "\n-1\nN \n" + recsphpdb+'\nN \n')
    file2.close()
    ShSPH = DOCKPATH+"/proteins/showsphere/bin/showsphere < showshere.in"
    os.system(ShSPH)

    os.system("cp rec.pdb rec.pdb_num"+str(num))
    os.system("cat "+recsphpdb+"*.pdb | sed -e 's/C/O/g' -e 's/SPH/HOH/g' | grep -v 'TER' >> rec.pdb")
    os.system("touch waters.pdb")
    os.system("cat "+recsphpdb+"*.pdb | sed -e 's/C/O/g' -e 's/SPH/HOH/g' | grep -v 'TER' >> waters.pdb")
    os.system("mkdir dir%d ; cp rec* dir%d/"%(num,num))
    os.system("mv INSPH OUTSPH dir%d"%(num))
    
    #SPHSEL = DOCKPATH+"/bin/sphere_selector"
    #os.system(SPHSEL + " "+recsph+" " +ligfile+" 5.0")
    #shutil.copyfile("selected_spheres.sph", "rec.5.0.sph")

#/nfs/soft/openbabel/current/bin/obabel -ipdb xtal-lig.pdb -omol2 -O xtal-lig.mol2

def dist_wat(wat1,wat2):
    dist = (wat1.X-wat2.X)**2.0 + (wat1.Y-wat2.Y)**2.0 + (wat1.Z-wat2.Z)**2.0
    return math.sqrt(dist)

def run_energy_cal():
    # this function will run amber.

    # cluster.  we start with the frist water. find everything close, then go to the next water not alreay assigned. find everything close, repeat until all are assigned.   

    wats = pdb_lib.read_pdb("waters.pdb")
    wat_clus = []
    for i in range(len(wats)):
         wat_clus.append(0)

    clusterheads = []
    cluster = 1
    for i,wat1 in enumerate(wats):
        if wat_clus[i] != 0: # if cluster is already asigned then continue to next water 
            continue
        print "water"+str(i)+" is a clusterhead.  "
        clusterheads.append(wat1)
        for j,wat2 in enumerate(wats):
            if wat_clus[j] != 0: # if cluster is already asigned then continue to next water 
               continue
            dist = dist_wat(wat1,wat2)
            #if dist < 3.0: 
            if dist < 2.8: 
               wat_clus[j] = cluster

        cluster = cluster + 1

    pdb_lib.output_pdb(clusterheads,"waterclusters.pdb")

    # check if there is a tleap input file:
    # if there is not then write a defualt file, if one already exist then use that one. 
    # This way someone can perpare the receptor the way they want. 
    if not (os.path.isfile("./tleap.in")):
         #os.system('cp rec.pdb rec_ori.pdb'
         file1 = open("tleap.in",'w')
         file1.write(" set default PBradii mbondi2 \n source leaprc.ff14SB \n \n REC = loadpdb rec_ori.pdb \n WAT = loadpdb water1.pdb \n COM = combine {REC WAT} \n saveamberparm REC rec.leap.prm7 rec.leap.rst7 \n saveamberparm COM rec.1wat.leap.prm7 rec.1wat.leap.rst7 \n charge REC \n quit \n")
         file1.close()
    else:
         print "using pre-existing tleap.in"

    # cut -c 24-28 rec_ori.pdb | sort -u | wc -l
    numres = 290

    if not (os.path.isfile("./min.in")):
         file2 = open("min.in",'w')
         #file2.write(" 01mi.in: equil minimization with Cartesian restraints /n &cntrl /n imin=1, maxcyc=3000, ncyc = 1500, /n ntpr=100, /n ntwr=100000000,  /n ntr=1, /n restraint_wt=100.0, /n restraintmask= ':1-%d & !@H' /n / /n "%(numres))
         file2.write(" min.in: minimization with GB \n &cntrl \n imin = 1, maxcyc = 10000, ncyc = 50,  ntmin = 1, \n igb=1, \n ntx = 1, ntc = 1, ntf = 1, \n ntb = 0, ntp = 0, \n ntwx = 1000, ntwe = 0, ntpr = 1000, \n cut = 999.9, \n ntr = 1, \n restraintmask = '!@H=', \n restraint_wt = 0.1, \n / \n ")
         file2.close()
         
    #fh = open('waters.pdb','r')
    fh = open('waterclusters.pdb','r')
    lines = fh.readlines()
    fh.close()

    fh = open('water1.pdb','w')
    fh.write(lines[0])
    fh.close()

    os.system("setenv AMBERHOME /nfs/soft/amber/amber14")
    os.system("$AMBERHOME/bin/tleap -s -f tleap.in > ! tleap.out")

    # minimize the receptor alone. 
    os.system("$AMBERHOME/bin/pmemd.cuda -O -i min.in -o min.out -p rec.leap.prm7 -c rec.leap.rst7 -ref min.rst7 -x min.mdcrd -inf min.info -r min.rst7")
    #os.system("$AMBERHOME/bin/sander -O -i min.in -o min.out -p rec.leap.prm7 -c rec.leap.rst7 -ref min.rst7 -x min.mdcrd -inf min.info -r min.rst7")
     
    # loop over all waters, run a minimization on each water in the context of the receptor.
    count = 1
    for line in lines:
        name = "water_" + str(count)
        print "we are minimzing "+ name
        fh = open(name+".pdb",'w')
        fh.write(line)
        fh.close()
        os.system("python /nfs/home/tbalius/zzz.scripts/add_h_to_wat.py "+name+".pdb")
        #print "cat rec.leap.rst7 "+name+".pdb.rst7 > "+name+".rst7"
        #os.system("cat rec.leap.rst7 "+name+".pdb.rst7 > "+name+".rst7")
        fh = open('rec.leap.rst7','r')
        fh2 = open(name+'.rst7','w')
        linecount = 0
        for line in fh:
            if linecount == 1:
                num = int(line.split()[0])
                num = num+3
                fh2.write('%d\n'%num)
            else:
                fh2.write(line)
            linecount=linecount+1
        fh.close()
        fh = open(name+".pdb.rst7",'r')
        for line in fh:
            fh2.write(line)
        fh.close()
        fh2.close()
        #exit()
        os.system("$AMBERHOME/bin/ambpdb -p rec.1wat.leap.prm7 < "+name+".rst7 > before_min_"+name+".pdb")
        os.system("$AMBERHOME/bin/pmemd.cuda -O -i min.in -o min."+name+".out -p rec.1wat.leap.prm7 -c "+name+".rst7 -ref "+name+".rst7 -x min."+name+".mdcrd -inf min."+name+".info -r min."+name+".rst7")
        #os.system("$AMBERHOME/bin/sander -O -i min.in -o min."+name+".out -p rec.1wat.leap.prm7 -c "+name+".rst7 -ref "+name+".rst7 -x min."+name+".mdcrd -inf min."+name+".info -r min."+name+".rst7")
        os.system("$AMBERHOME/bin/ambpdb -p rec.1wat.leap.prm7 < min."+name+".rst7 > min."+name+".pdb")
        count = count + 1
        #if count > 10:
        #    break
        

    # sort waters on energy

    # do best frist clustering, remove all waters within 1.4 anstroms from the best, then move to next best remaining 
    
 

#os.system("rm -rf dir*")
#
#for i in range(3):
#   run_spheregen(i)

run_energy_cal()




