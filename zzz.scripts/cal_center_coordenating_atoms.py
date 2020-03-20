
#################################################################################################################
## Writen by Trent Balius at FNLCR in 2020 (took from other scripts)
#################################################################################################################
import sys,os
import pdb_lib as pdb

#DOCKBASE = "/nfs/home/tbalius/zzz.github/DOCK"

 
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
            #print(atom_list[k].resnum,atom_list[k].atomname)
            if (atom_list[k].resnum.strip()+":"+atom_list[k].atomname.strip()) in reslist:
                print(atom_list[k].resnum,atom_list[k].atomname)
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

def change_name(atom_list,reslist):

     for res in reslist:
        resnum = int(res.split(':')[0])
        atomname = res.split(':')[1]
        for k in range(0,len(atom_list)):
            if (int(atom_list[k].resnum) == resnum):
                if (atom_list[k].resname == "CYS"): 
                   #print ("I AM HERE")
                   atom_list[k].resname = "CYM"
                if (atom_list[k].resname == "HIS"):
                   if (atomname == "NE2"): # if the NE2 is coordenating the ZINC ion then it is the delta that is portonated.
                      atom_list[k].resname = "HID"
                   elif (atomname == "ND1"):  # if the ND1 is coordenating the ZINC ion then the Epsolon is protonated.
                      atom_list[k].resname = "HIE"
                   else: 
                      print("leave HIS unchanged")

def main():
    if len(sys.argv) != 4: # if no input
       print ("ERORR: there need to be 3 inputs: pdb inputfilename,  residue:atom_list, outputfileprefix.")
       print ("list is resnum1:atomname1,...,resnum1:atomnamei,...,resnumk,atomnamej,...")
       return

    fileinputpdb = sys.argv[1]
    res_string = sys.argv[2]
    fileoutput   = sys.argv[3]

    splitname = fileinputpdb.split('\\')[-1].split('.') 
    if len(splitname) != 2:
        print ("error pdb file is weird. ")
        exit()
    prefix = splitname[0] 

    print ('input_pdb =' + fileinputpdb)
    print ('sph prefix =' + prefix)
    print ('residue string =' + res_string)
    print ('output =' + fileoutput)

    residlist = []
    res_string_split = res_string.split(',') 
    residlist = res_string_split
    print res_string_split

    pdblist = pdb.read_pdb(fileinputpdb)[0]
    center = centre_of_mass(pdblist,residlist)
    #print ("%6.4f %6.4f %6.4f"%(center[0],center[1],center[2]))
    print ("HETATM    1 ZN    ZN A   1    %8.3f%8.3f%8.3f  1.00  0.00          ZN"%(center[0],center[1],center[2]))
    fh = open(fileoutput+'_zinc.pdb','w')
    fh.write("HETATM    1 ZN    ZN A   1    %8.3f%8.3f%8.3f  1.00  0.00          ZN\n"%(center[0],center[1],center[2]))
    fh.close()

    change_name(pdblist,residlist)
    pdb.output_pdb(pdblist, fileoutput+'.pdb')
    

main()
