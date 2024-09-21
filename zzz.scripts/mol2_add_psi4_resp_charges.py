
# Written by Trent Balius and Stanley Tan, September 2024. 

import sys
import mol2_python3 as mol2

def main():
    mol2file = sys.argv[1]
    chargefile = sys.argv[2]
    outfile = sys.argv[3]
    print ('mol2 file = %s'%mol2file)
    print ('charge file = %s'%chargefile)
    print ('mol2 outfile = %s'%outfile)
    mol = mol2.read_Mol2_file(mol2file)[0]
    print(len(mol.atom_list))
    cfh = open(chargefile,'r')
    read_charge_flag = False
    charges = []
    for line in cfh:
        if (read_charge_flag):
            if 'Center' in line:
                continue
            if ('Total Charge:' in line):
                print("done")
                read_charge_flag = False
                continue
            sline = line.split()
            respcharge = float(sline[3])
            charges.append(respcharge)
            print (line)
        if "Electrostatic Potential Charges" in line: 
            read_charge_flag = True

    print(len(mol.atom_list))
    for i in range(len(mol.atom_list)):
        mol.atom_list[i].Q = charges[i]
    
    mol2.write_mol2(mol,outfile)


main()
