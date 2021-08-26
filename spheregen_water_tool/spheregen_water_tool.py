#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# this ways copyed and then modified from:
# http://sebsauvage.net/python/gui/#import
# Written by Trent Balius (shoichet lab, 2016) 


import math,os, shutil,os.path 
import pdb_lib, sph_lib
import water_clustering as wc

def run_spheregen(num,maxradius,minradius,proberadius):
    #DOCKPATH = "/nfs/home/tbalius/zzz.github/DOCK"
    DOCKPATH = "/home/baliuste/zzz.github/DOCK"
    ligfile = "xtal-lig.mol2"
    recdms = "rec.dms"
    recpdb = "rec.pdb"
    recsph = "rec.sph"
    recsphp = "rec_mod.sph"
    #recsphpdb = "rec.sph.pdb"
    recsphpdb = "rec.sph"
    name = "rec"

    if not (os.path.isfile("./rec_ori.pdb")):
         os.system('cp rec.pdb rec_ori.pdb')

    #step one generate molecular surface.
    #DMS = DOCKPATH+"/proteins/dms/bin/dms"
    #flags = " "+recpdb+" -a -n -w 1.0 -v -o "+recdms
    #dmscmd = DMS + flags
    # -w is the probe radius
    #proberadius = 1.2
    dmscmd = DOCKPATH+"/proteins/dms/bin/dms "+recpdb+" -a -d 0.2 -g dms.log -p -n -w "+str(proberadius)+" -o "+recdms
    print "Run dms \n "+dmscmd
    os.system(dmscmd)


    # step one generate spheres.
    os.system("rm -rf OUTSPH temp1.ms temp2* temp3.atc rec.sph rec.sph.pdb* showshere.in")

    SPH = DOCKPATH+"/proteins/sphgen/bin/sphgen"

    #maxradius = 1.8
    #minradius = 1.2

    file1 = open('INSPH','w')
    #file1.write("%s\nR\nX\n0.0\n%3.1f\n%3.1f\n%s\n"%(recdms,maxradius,minradius,recsph))
    file1.write("%s\nR\nX\n-0.1\n%3.1f\n%3.1f\n%s\n"%(recdms,maxradius,minradius,recsph))
    file1.close()
    print "Run Sphgen"
    os.system(SPH)

    print "Process Spheres"
    sphlist = sph_lib.read_sph(recsph,'A','A')
    sphlist_processed = []
    for sph in  sphlist: 
        if sph.radius < maxradius and sph.radius > minradius: 
           sphlist_processed.append(sph)
    sph_lib.write_sph(recsphp,sphlist_processed)

    file2 = open("showshere.in",'w')
    file2.write( recsphp + "\n-1\nN \n" + recsphpdb+'\nN \n')
    file2.close()

#  Enter name of sphere cluster file: adfds
#  Enter cluster number to process (<0 = all): -1
#  Generate surfaces as well as pdb files (<N>/Y)? N
#  Enter name for output file prefix: adafdsf
#  Process clu0 (ALL spheres) (<N>/Y)? N

    

    ShSPH = DOCKPATH+"/proteins/showsphere/bin/showsphere < showshere.in"
    os.system(ShSPH)

    os.system("cp rec.pdb rec.pdb_num"+str(num))
    #os.system("cat "+recsphpdb+"_1.pdb | sed -e 's/C/O/g' -e 's/SPH/HOH/g' | grep -v 'TER' >> rec.pdb")
    num_waters = int(os.popen("cat "+recsphpdb+"_1.pdb | sed -e 's/C/O/g' -e 's/SPH/HOH/g' | grep -v 'TER' | wc -l ").readlines()[0])
    #print num_waters
    os.system("touch waters.pdb")
    os.system("cat "+recsphpdb+"_1.pdb | sed -e 's/C/O/g' -e 's/SPH/HOH/g' | grep -v 'TER' >> waters.pdb")
    os.system("cat waters.pdb >> rec.pdb")
    os.system("mkdir dir%d ; mv %s*.pdb dir%d/;cp rec* dir%d/"%(num,recsphpdb,num,num))
    os.system("mv INSPH OUTSPH dir%d"%(num))
    
    #SPHSEL = DOCKPATH+"/bin/sphere_selector"
    #os.system(SPHSEL + " "+recsph+" " +ligfile+" 5.0")
    #shutil.copyfile("selected_spheres.sph", "rec.5.0.sph")
    return num_waters
#/nfs/soft/openbabel/current/bin/obabel -ipdb xtal-lig.pdb -omol2 -O xtal-lig.mol2


def run_energy_cal(waterspdb):
    # this function will run amber.

    # check if there is a tleap input file:
    # if there is not then write a defualt file, if one already exist then use that one. 
    # This way someone can perpare the receptor the way they want. 
    if not (os.path.isfile("./tleap.in")):
         #os.system('cp rec.pdb rec_ori.pdb'
         file1 = open("tleap.in",'w')
         #file1.write(" set default PBradii mbondi2 \n source leaprc.ff14SB \n \n REC = loadpdb rec_ori.pdb \n WAT = loadpdb "+waterspdb+" \n COM = combine {REC WAT} \n saveamberparm REC rec.leap.prm7 rec.leap.rst7 \n saveamberparm COM rec.wat.leap.prm7 rec.wat.leap.rst7 \n charge REC \n quit \n")
         file1.write(" set default PBradii mbondi2 \n # load the protein force field\n source leaprc.protein.ff14SB \n # load water \n source leaprc.water.tip3p \n \n REC = loadpdb rec_ori.pdb \n WAT = loadpdb "+waterspdb+" \n COM = combine {REC WAT} \n saveamberparm REC rec.leap.prm7 rec.leap.rst7 \n saveamberparm COM rec.wat.leap.prm7 rec.wat.leap.rst7 \n charge REC \n quit \n")
         file1.close()
    else:
         print "using pre-existing tleap.in"

    # cut -c 24-28 rec_ori.pdb | sort -u | wc -l
    numres = 290

    if not (os.path.isfile("./min.in")):
         file2 = open("min.in",'w')
         #file2.write(" 01mi.in: equil minimization with Cartesian restraints /n &cntrl /n imin=1, maxcyc=3000, ncyc = 1500, /n ntpr=100, /n ntwr=100000000,  /n ntr=1, /n restraint_wt=100.0, /n restraintmask= ':1-%d & !@H' /n / /n "%(numres))
         #file2.write(" min.in: minimization with GB \n &cntrl \n imin = 1, maxcyc = 100, ncyc = 50,  ntmin = 1, \n igb=1, \n ntx = 1, ntc = 1, ntf = 1, \n ntb = 0, ntp = 0, \n ntwx = 1000, ntwe = 0, ntpr = 1000, \n cut = 999.9, \n ntr = 1, \n restraintmask = '!@H=', \n restraint_wt = 0.1, \n / \n ")
         file2.write(" min.in: minimization with GB \n &cntrl \n imin = 1, maxcyc = 100, ncyc = 50,  ntmin = 1, \n igb=1, \n ntx = 1, ntc = 1, ntf = 1, \n ntb = 0, ntp = 0, \n ntwx = 1000, ntwe = 0, ntpr = 1000, \n cut = 999.9, \n ntr = 1, \n restraintmask = '!@H=', \n restraint_wt = 1.0, \n / \n ")
         file2.close()
         
    #fh = open('waters.pdb','r')
#    fh = open('waterclusters.pdb','r')
#    lines = fh.readlines()
#    fh.close()

#    fh = open('water1.pdb','w')
#    fh.write(lines[0])
#    fh.close()

    #os.system("setenv AMBERHOME = /nfs/soft/amber/amber14")
    #os.system("setenv AMBERHOME = /home/baliuste/programs/amber/amber18")
    os.environ["AMBERHOME"] = "/home/baliuste/zzz.programs/amber/amber18"
    #os.system("$AMBERHOME/bin/tleap -s -f tleap.in >! tleap.out")
    os.system("$AMBERHOME/bin/tleap -s -f tleap.in > tleap.out")

    ## minimize the receptor alone. 
    #os.system("$AMBERHOME/bin/sander -O -i min.in -o min.out -p rec.leap.prm7 -c rec.leap.rst7 -ref rec.leap.rst7 -x min.mdcrd -inf min.info -r min.rst7")
    os.system("$AMBERHOME/bin/sander -O -i min.in -o min.out -p rec.wat.leap.prm7 -c rec.wat.leap.rst7 -ref rec.wat.leap.rst7 -x min.mdcrd -inf min.info -r min.rst7")
    os.system("$AMBERHOME/bin/ambpdb -p rec.wat.leap.prm7 -c min.rst7 > min.pdb")

#radius_max = 2.0
radius_max = 1.5 
#radius_max = 1.6 

#radius_min = 1.3 
#radius_min = 1.2 
radius_min = 1.1 
#radius_min = 1.0 

probe_radius = 1.2

os.system("rm -rf dir*")
os.system("cp rec.pdb rec.pdb_ori")

num_waters = 0

for i in range(3):
   num_waters = run_spheregen(i,radius_max,radius_min,probe_radius)
   print "\n"
   print "number of waters generated: ", num_waters
   print "\n"
   if num_waters == 0: 
      break 


###cluster_water_pdb(2.0)
###water_cluster.cluster_water_pdb(infilename,distance,outfilename,den)
wc.cluster_water_pdb("rec.pdb",1.4,"waters_clusters",30)

watername = "waters_clusters_center.pdb"
#watername = "waters_clusters_median.pdb"
run_energy_cal(watername)




