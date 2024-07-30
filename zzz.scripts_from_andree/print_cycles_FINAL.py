import mol2_python3 as mol2
import sys
import copy
import math

# This script is written by Andree Kolliegbo, July 2024!
# This program suggests place to break a macrocycle by filtering out the places that are branches or part of a smaller cycle

# The following classes define the graph structure for conversion
class Node:
    def __init__(self, atom):
        self.atom = atom
        self.visited = False
        self.branch = False
        self.neighbors = []

class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.visited = False

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.cycles = []
        self.num_cycles = 0
        self.macrocycle_found = False
    
    def add_node(self, atom):
        node = Node(atom)
        self.nodes[atom.num] = node
        return node

    def add_edge(self, node1_num, node2_num):
        node1 = self.nodes[node1_num]
        node2 = self.nodes[node2_num]
        edge = Edge(node1, node2)
        self.edges.append(edge)
        node1.neighbors.append(node2)
        node2.neighbors.append(node1)
 
#################### cycle traversal ############################

    def dfs_cycle(self, u, p, color, par):
        
        # Out of bounds check
        if u >= len(color):
            return
        
        # Marks branching points
        if len(self.nodes[u].neighbors) > 2:
           self.nodes[u].branch = True 

        # Check that node has been fully visited
        if color[u] == 2:
            return

        # Node has been paritally visisted, there is a cycle here
        if color[u] == 1:
            cur = p
            cycle = []
           
            # Backtrack the parents of each node using par[] 
            while cur != u:
                cycle.append(cur)
                cur = par[cur]

            # Adds to graph's list of cycles
            cycle.append(u)
            self.cycles.append(cycle)
            self.num_cycles += 1
            
            # Check if current cycle is the macrocycle
            if len(cycle) > 12:
                self.macrocycle_found = True
            return

        # Marks u as visited
        par[u] = p
        color[u] = 1

        # Calls the funtion recurisvly on the neighbors of u
        for neighbor in self.nodes[u].neighbors:
            v = neighbor.atom.num
            if v == par[u]:
                continue
            self.dfs_cycle(v, u, color, par)

        color[u] = 2

    def detect_cycles(self):
        # Initializes the color and parent arrays to 0 and -1, respectively
        num_nodes = len(self.nodes)
        self.cycles = [[] for _ in range(num_nodes)]
        color = [0] * (max(self.nodes.keys()) + 1)
        par = [-1] * (max(self.nodes.keys()) + 1)

        # Starts dfs on any unvisited nodes
        for node_num in self.nodes:
            if color[node_num] == 0:
                self.dfs_cycle(node_num, -1, color, par)

    def find_macrocycle_break_points(self):
        
        if not self.macrocycle_found:
            print("Sorry, no macrocycle found.")
            return

        macrocycle_nodes = set()
        smaller_cycle_nodes = set()

        for cycle in self.cycles:
            if len(cycle) > 12:
                macrocycle_nodes.update(cycle)
            else:
                smaller_cycle_nodes.update(cycle)

        break_points = []
        for node_num in macrocycle_nodes:
            node = self.nodes[node_num]
            if node_num in macrocycle_nodes and not node_num in smaller_cycle_nodes and not node.branch:
                break_points.append(node)
            else:
                neighbor_nums = [neighbor.atom.num for neighbor in node.neighbors]
                #print(f"Node {node_num} is connected to nodes: {neighbor_nums}")
        
        if break_points:
            print("\nAcceptable break points for the macrocycle:\n")
            for node in break_points:
                print(f"Atom: {node.atom.name}, {node.atom.type} Residue: {node.atom.resname}")
        else:
            print("\nNo acceptable break points found for the macrocycle.")

    def print_breakpoint_bonded_pairs(self, mol):
        macrocycle_nodes = set()
        smaller_cycle_nodes = set()

        for cycle in self.cycles:
            if len(cycle) > 12:
                macrocycle_nodes.update(cycle)
            else:
                smaller_cycle_nodes.update(cycle)

        break_point_bonds = []
        for edge in self.edges:
            node1 = edge.node1
            node2 = edge.node2
            if (node1.atom.num in macrocycle_nodes and node2.atom.num in macrocycle_nodes and
                node1.atom.num not in smaller_cycle_nodes and node2.atom.num not in smaller_cycle_nodes and
                not node1.branch and not node2.branch):
                break_point_bonds.append((node1, node2))

        if break_point_bonds:
            print("\nAcceptable break point bonds for the macrocycle:\n")
            for node1, node2 in break_point_bonds:
                bond_distance = self.calculate_distance(mol, node1.atom.num, node2.atom.num)
                print(f"Bond between Atom: {node1.atom.name} ({node1.atom.num}, {node1.atom.resname}) and Atom: {node2.atom.name} ({node2.atom.num}, {node2.atom.resname}) with distance: {bond_distance:.2f} Å")
        else:
            print("\nNo acceptable break point bonds found for the macrocycle.")

    def calculate_distance(self, mol, atom1num, atom2num):
        x1 = y1 = z1 = x2 = y2 = z2 = 0.0

        # Get the coordinates of the atoms
        for a in mol.atom_list:
            if a.num == atom1num:
                x1 = a.X
                y1 = a.Y
                z1 = a.Z
            elif a.num == atom2num:
                x2 = a.X
                y2 = a.Y
                z2 = a.Z

        # Calculate bond length
        bond_distance = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2) + ((z1 - z2) ** 2))
        return bond_distance

#################### bemis-murko inspired alg ############################

    def remove_single_nodes(self):
        # Removes dangly bits until all_singles is true again
        all_singles = True  
        
        # For each neighbor in each node list
        for node_num, node in list(self.nodes.items()):
            neighbor_nums = [neighbor.atom.num for neighbor in node.neighbors]

            # If the node only has 1 neighbor then its a dangly peice and will have another dangly neighbor on another layer
            if len(neighbor_nums) == 1:
                neighbor = node.neighbors[0]
                neighbor.neighbors.remove(node)
                node.neighbors.remove(neighbor)
                all_singles = False  # Not all singles yet
                del self.nodes[node_num]  # Remove the single connection node

        return all_singles
     
    # Removes residues that have no atoms after scaffold trimming
    def remove_edges_with_dangly_nodes(self):
        node_num_dict = {}
        new_edge_list = []

        for node_num, node in list(self.nodes.items()):
            node_num_dict[node_num] = 1
        for edge in self.edges:
            if edge.node1.atom.num in node_num_dict and edge.node2.atom.num in node_num_dict:
                new_edge_list.append(edge)

        return new_edge_list

    # Removes residues that have no atoms after scaffold trimming
    def remove_dangly_res(self, mol):
        node_num_dict = {}  # Tells us if the atom exists in the molecule or not
        new_res_list = copy.copy(mol.residue_list)  # Res_nums of still existing residues

        # Initializes the node dictionary
        for node_num, node in list(self.nodes.items()):
            node_num_dict[node_num] = 1

        # Deletes any residues without a node in the remaining graph structure
        for res_num in list(mol.residue_list.keys()): 
            current_list = new_res_list[res_num]
            res_index = 0
            for atom in current_list:
                if atom.num not in node_num_dict:
                    del (current_list[res_index])
                res_index += 1

        return new_res_list

    # Print node list
    def print_node_list(self):
        print(len(self.nodes), " # total nodes")
        for node_num, node in list(self.nodes.items()):
            print(node_num, node.atom.name)

    # Function to print residue list
    def print_residue_list(self, mol):
        for res_num in list(mol.residue_list.keys()):
            atoms = [atom.num for atom in mol.residue_list[res_num]]
            print(res_num, atoms)

    # Converts the graph to a mol2 file (for testing purposes)
    def convert_to_mol(self, mol, header, name):
        atom_list = []
        bond_list = []
        mol_new = copy.copy(mol)

        # Convert nodes to atom_list and populate the atom_dic
        for node_num, node in self.nodes.items():
            atom_obj = node.atom
            atom_list.append(atom_obj)

        # Convert edges to bond_list using the new atom indices from atom_dic
        bond_num = 1
        for edge in self.edges:
            a1_num = edge.node1.atom.num
            a2_num = edge.node2.atom.num
            bond_obj = mol2.bond(a1_num, a2_num, bond_num, '1')  # Assuming bond type '1' for simplicity
            bond_list.append(bond_obj)
            bond_num += 1

        # Create the new Mol object
        mol_new.header = header
        mol_new.name = name
        mol_new.atom_list = atom_list
        mol_new.bond_list = bond_list
        mol_new.residue_list = self.remove_dangly_res(mol)

        return mol_new


#################### main driver code ############################

def main():
  
    # Read in arguments
    if len(sys.argv) != 2:
        print("\nUsage:    python3    print_breakpoints.py    input_file_prefix\n")
        sys.exit(1)
 
    infile = f"{sys.argv[1]}.mol2"
    mol_list = mol2.read_Mol2_file(infile)
    mol = mol_list[0]
    outfile = f"breakpoints_{sys.argv[1]}.txt"
    print("\noutput has been  written to ", outfile, "\n")
    sys.stdout = open(outfile,'wt')
    
    # Create graph from mol object
    graph = Graph()
    for atom in mol.atom_list:
        graph.add_node(atom)
    for bond in mol.bond_list:
        graph.add_edge(bond.a1_num, bond.a2_num)

    # Murcko-inspired pruning process
    counter = 0
    all_singles_removed = graph.remove_single_nodes()
    while not all_singles_removed:
        counter += 1
        all_singles_removed = graph.remove_single_nodes()

    graph.edges = graph.remove_edges_with_dangly_nodes()

    # Detect cycles
    graph.detect_cycles()
    print("Total cycles: ", graph.num_cycles)

    # Find breakpoints
    graph.find_macrocycle_break_points()
    graph.print_breakpoint_bonded_pairs(mol)

if __name__ == "__main__":
    main()
