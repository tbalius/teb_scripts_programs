#import sys,math,os,mol2
import sys,math,os
import mol2_python3 as mol2

## Writen by Trent Balius in the Shoichet Lab, UCSF
## modifed in Dec, 2016
## converts a mol2 to spheres. 

def intialize_vdw_parm(vdwfile):
    # this function reads in the vdw file.
    fileh = open(vdwfile,'r')
    vdw_dict = {}
    for line in fileh:
        if (line[0] == '!'):
           continue
        splitline = line.split()
        t = int(splitline[0])
        a = float(splitline[1]) # A^(1/2)
        b = float(splitline[2]) # B^(1/2)
        #r = (((2A/B)^(1/2))^(1/3))/2
        if a == 0 or b == 0:
           r = 0.5
        else:
           r = (math.sqrt(2.0)*a/b)**(1.0/3.0)/2.0 # radius
        print (t,a,b,r)
        vdw_dict[t] = r
    return vdw_dict

def get_radius(atype,vdw_dict):
    return vdw_dict[atype]


def write_sph(filename,mol):
    dt   = mol2.convert_sybyl_to_dock(mol) # get dock atom types.
    dockbase = os.environ.get('DOCKBASE')
    vdw_dict = intialize_vdw_parm(dockbase+'/proteins/defaults/vdw.parms.amb.mindock') 
    outsph = open(filename,'w')
    print (len(mol.atom_list))
    outsph.write("DOCK spheres generated from ligand heavy atoms\n")
    outsph.write("cluster     1   number of spheres in cluster    %d\n" % len(mol.atom_list))
    for i in range(len(mol.atom_list)): 
        radius = vdw_dict[dt[i]]
        #outsph.write("%5d%10.5f%10.5f%10.5f%8.3f%5d                                \n" % 
        outsph.write("%5d%10.5f%10.5f%10.5f%8.3f%5d 0  0\n" % (i+1,round(mol.atom_list[i].X,3), round(mol.atom_list[i].Y,3), round(mol.atom_list[i].Z,3),radius,i+1) )

    outsph.close()
    return

def main():
  if len(sys.argv) != 3: # if no input
     print ("ERORR")
     print ("this script reads in a mol2 file and writes out a sph file.")
     print ("this script takes 2 arguments: name.mol2 name.sph")
     return
  namemol2 = sys.argv[1]
  namesph = sys.argv[2]
  mol  = mol2.remove_hydrogens(mol2.read_Mol2_file(namemol2)[0])
  write_sph(namesph,mol)
main()


