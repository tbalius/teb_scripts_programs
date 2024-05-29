
import mol2_python3 as mol2
import sys

#  This is written by Trent E. Balius 

# started on 2023.11.08 at FNLCR



def main ():
    print ("this file requiers the mol2 libary writen by trent balius and sudipto mukherjee")
    
    print ("syntex: mol2_get_frist_mol.py input_file output_file ")
    
    if ( len(sys.argv) != 3 ):
       print("syntex error ...")
       exit(0)
    
    #flag_submap = False
    infile = sys.argv[1]
    outfile = sys.argv[2]
    
    print("in = %s"%infile)
    print("out = %s"%outfile)

    mol_list2 = mol2.read_Mol2_file(infile)
    boolfirst = True
    print(len(mol_list2))
    for mol in mol_list2: 
        if len(mol.atom_list) == 0: 
            continue
        if (boolfirst):
            mol2.write_mol2(mol,outfile)
            boolfirst = False
        else: 
            mol2.append_mol2(mol,outfile)
    
main() 
