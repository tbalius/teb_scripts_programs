import mol2_python3 as mol2
import sys
import copy

# part 3 of the macrocycle breaking project
# written by Andree Kolliegbo, july 2024

'''
ok so the thought process for this script is to basically just replace the old file with the new coordinates , but repeat it for all of the poses constructed in the new mol2 file

input: close_cycle.py    orignal_macrocycle.mol2     docked_w_dummy.mol2
'''

def replace_coordinates(original_atom_list, new_atom_list):
    # Replaces the x, y, z coords of each atom in the mol2 file
    for i in range(len(original_atom_list)):
        original_atom_list[i].X = new_atom_list[i].X
        original_atom_list[i].Y = new_atom_list[i].Y
        original_atom_list[i].Z = new_atom_list[i].Z

    return original_atom_list


def main():
    # Arguments
    if len(sys.argv) != 3:
        print(" Usage:    python3     close_cycle.py       original_macrocycle.mol2       dock_output.mol2")
        sys.exit(1)

    original_file = sys.argv[1]
    converted_file = sys.argv[2]
    outfile = f"closed_{sys.argv[2]}"
    # Read in the original mol2 file
    original_mol_list = mol2.read_Mol2_file_head(original_file)

    # Error checkin
    if len(original_mol_list) != 1:
        raise ValueError("The original mol2 file should contain exactly one molecule.")
    original_mol = original_mol_list[0]


    # Read in the converted mol2 file
    converted_mol_list = mol2.read_Mol2_file(converted_file)
        
    for converted_mol in converted_mol_list:
        # Create a copy of the original molecule
        new_mol = copy.deepcopy(original_mol)
        # Replace the coordinates
        new_mol.atom_list = replace_coordinates(new_mol.atom_list, converted_mol.atom_list)
        # Write the new molecule to the output file
        mol2.append_mol2(new_mol, outfile)

if __name__ == "__main__":
    main()

