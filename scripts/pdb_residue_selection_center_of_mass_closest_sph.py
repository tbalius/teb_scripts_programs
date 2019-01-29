
#################################################################################################################
## Writen by Trent Balius in the Shoichet Lab, UCSF in 2015
#################################################################################################################
import sys,os
import sph_lib as sph
#import mol2 
import pdb_lib as pdb

DOCKBASE = "/nfs/home/tbalius/zzz.github/DOCK"

def run_dms_sph(rec_pdb_name,prefix):
    rec_ms_name = prefix+'.ms'
    rec_sph_name = prefix+'.sph'
    os.system("rm -rf OUTSPH temp1.ms temp2* temp3.atc "+rec_ms_name+" "+rec_sph_name+" showshere.in")

    DMS = DOCKBASE+"/proteins/dms/bin/dms "+rec_pdb_name+" -a -d 0.2 -g dms.log -p -n -o "+rec_ms_name
    os.system(DMS)

    SPH = DOCKBASE+"/proteins/sphgen/bin/sphgen"

    maxradius = 4.0
    minradius = 1.0

    file1 = open('INSPH','w')
    file1.write("%s\nR\nX\n0.0\n%3.1f\n%3.1f\n%s\n"%(rec_ms_name,maxradius,minradius,rec_sph_name))
    file1.close()
    print "Run Sphgen"
    os.system(SPH)
 
def convert_sph_to_pdb(sphname,pdbname):

    file2 = open("showshere.in",'w')
    file2.write( sphname + "\n-1\nN \n" + pdbname+'\nN \n')
    file2.close()
    ShSPH = DOCKBASE+"/proteins/showsphere/bin/showsphere < showshere.in"
    os.system(ShSPH)


#def center_of_mass():
def centre_of_mass(atom_list,reslist):
        # Dictionary of atomic weights of elements
        #atom_mass = {'O':15.9994 ,'N':14.00674 ,'C':12.011 ,'F':18.9984032 ,'Cl':35.4527 ,'Br':79.904
        #,'I':126.90447 ,'H':1.00794 ,'B':10.811 ,'S':32.066 ,'P':30.973762 ,'Li':6.941 ,'Na':22.98968
        #,'Mg':24.3050 ,'Al':26.981539 ,'Si':28.0855 ,'K':39.0983 ,'Ca':40.078 ,'Cr':51.9961 ,'Mn':54.93805
        #,'Fe':55.847 ,'Co':58.93320 ,'Cu':63.546 ,'Zn':65.39 ,'Se':78.96 ,'Mo':95.94 ,'Sn':118.710 ,'LP':0.0 }

        #cmass = [0,0,0]
        centroid = [0,0,0]
        molecular_weight = 0
        count = 0
        for k in range(0,len(atom_list)):
            if int(atom_list[k].resnum) in reslist:
                #print atom_list[k].atomname, atom_list[k].atomname[1]
                #element = atom_list[k].atomname.replace(" ","")[0] # this a good aprox for a protein.
                #if (atom_list[k].atomname == "FE  "): 
                #    element = 'Fe'
                #cmass[0] += atom_list[k].X * atom_mass[element]
                #cmass[1] += atom_list[k].Y * atom_mass[element]
                #cmass[2] += atom_list[k].Z * atom_mass[element]
                centroid[0] += atom_list[k].X
                centroid[1] += atom_list[k].Y
                centroid[2] += atom_list[k].Z
                #molecular_weight += atom_mass[element]
                count = count+1
        #print "Molecular Weight =",molecular_weight
        #cmass[0] /= molecular_weight
        #cmass[1] /= molecular_weight
        #cmass[2] /= molecular_weight
        print "number of atoms in reslist: " + str(count)
        centroid[0] /= count
        centroid[1] /= count
        centroid[2] /= count
        #print 'Centroid =',centroid
        #return cmass
        return centroid

def closest_sphs_to_center(sphs,center,N): 
    d_min   = []
    sphlist = []

    print "number of spheres to find = %d"%N

    if N > len(sphs): 
       print "Error: number of spheres to find excides the number of spheres."
       exit()


    for i in range(0,N):
       d_min.append(1000.0)
       sphlist.append(sphs[0])
    for sph in sphs:
        d2 = (center[0] - sph.X)**2 + (center[1] - sph.Y)**2 + (center[2] - sph.Z)**2
        for i in range(0,N):
           if d2 <= d_min[i]:
              #print range(N-2,i-1,-1)
              #print range(i,N-1)
              for j in range(N-2,i-1,-1): # we need to move the values down the list
                  #print d_min[j]
                  d_min[j+1] = d_min[j]
                  sphlist[j+1] = sphlist[j]
              sphlist[i] = sph # replace the value
              d_min[i]   = d2
              break           # break out of the loop and go to the next sph
                
                #break
    #sphlist.append(minsph)
    #sphlist.append(min2sph)
    return sphlist

def main():
    if len(sys.argv) != 4: # if no input
       print "ERORR: there need to be 3 inputs: pdb inputfilename,  residuelist, outputfileprefix."
       return

    fileinputpdb = sys.argv[1]
    #fileinputsph = sys.argv[2]
    #res_string = sys.argv[3]
    #fileoutput   = sys.argv[4]
    res_string = sys.argv[2]
    fileoutput   = sys.argv[3]

    splitname = fileinputpdb.split('\\')[-1].split('.') 
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

    run_dms_sph(fileinputpdb,prefix)
    list1 = sph.read_sph(prefix+".sph","A","A")

    pdblist = pdb.read_pdb(fileinputpdb)
    center = centre_of_mass(pdblist,residlist)
    print center
    list2 = closest_sphs_to_center(list1, center,4)
    sph.write_sph(fileoutput+".sph",list2)
    # add center to list and write agian to new file
    #tmp_sphere = sphere(index,x,y,z,r,atomnum,clust,col) 
    tmp_sphere = sph.sphere(2,center[0],center[1],center[2],0.7,2,0,0) 
    list2.append(tmp_sphere)
    sph.write_sph(fileoutput+"_and_center.sph",list2)
    convert_sph_to_pdb(fileoutput+".sph",fileoutput)

main()
