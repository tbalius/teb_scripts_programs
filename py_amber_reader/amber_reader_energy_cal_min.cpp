// 
// The programe amber_reader_energy_cal_min.cpp is based on
//
// amber_reader_frame_by_frame_var.cpp
// C++ translation of amber_reader_frame_by_frame_var.py
// Original author (Python): Trent E. Balius
// Translation: ChatGPT

/*
 * C++ translation of: amber_reader_frame_by_frame_var.py
 *
 * Original author (Python):
 *   Trent E. Balius
 *   Stony Brook University
 *   Started 2010-02-27
 *
 * C++ translation:
 *   Generated with the assistance of ChatGPT (OpenAI)
 *   from the original Python script by Trent E. Balius.
 *
 */

// TEB adding in bonded terms, a full energy evaluation (2025/11/22) 
// and minimization. 
// This includes modified non-bonded functional forms. 
// thinking about adding in monte carlo optimizer. 
//
// g++ amber_reader_energy_cal_min.cpp -O2 -Wall -Wextra -o amber_reader_energy 

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>
#include <cstdlib>
#include <algorithm>
#include <iomanip>

struct Bond {
    int atom1;
    int atom2;
    double forceC;
    double ideal;
};

struct Angle {
    int atom1;
    int atom2;
    int atom3;
    double forceC;
    double ideal;
};

struct Dihedral {
    int atom1;
    int atom2;
    int atom3;
    int atom4;
    double forceC;
    double period;
    double phase; 
    double ele14scale;//SCEE_SCALE; // 1-4 Scale for ele 
    double vdw14scale;//SCNB_SCALE; // 1-4 scale for vdw
};

struct Parm {
    std::vector<int> RESIDUE_POINTER;
    std::vector<std::string> RESIDUE_ARRAY;   // size N atoms
    std::vector<std::string> ATOM_NAME;       // size N atoms
    std::vector<std::string> AMBER_ATOM_TYPE; // size N atoms
    std::vector<int> ATOM_TYPE_INDEX;         // size N atoms
    std::vector<double> CHARGE;               // size N atoms
    std::vector<double> MASS;                 // size N atoms
    std::vector<std::vector<double>> M_LJA;   // MxM matrix
    std::vector<std::vector<double>> M_LJB;   // MxM matrix
    std::vector<Bond> bonds;
    std::vector<Angle> angles;
    std::vector<Dihedral> diheds;
    std::vector<std::vector<int>> M_bonded;   // MxM matrix for if something is 1-2,1-3,1-4 -> 
};


struct Cord {
    double x;
    double y;
    double z;
};

struct Frame {
    std::vector<Cord> cords;
};

static std::vector<std::string> split_whitespace(const std::string &line) {
    std::vector<std::string> result;
    std::istringstream iss(line);
    std::string tmp;
    while (iss >> tmp) {
        result.push_back(tmp);
    }
    return result;
}

static std::string strip_newline(const std::string &s) {
    std::string r = s;
    if (!r.empty() && (r.back() == '\n' || r.back() == '\r')) {
        while (!r.empty() && (r.back() == '\n' || r.back() == '\r')) {
            r.pop_back();
        }
    }
    return r;
}

static std::string remove_spaces(const std::string &s) {
    std::string r;
    for (char c : s) {
        if (c != ' ') r.push_back(c);
    }
    return r;
}

// Debug-print matrix of doubles (not used by main, kept for parity)
static void print_matrix(const std::vector<std::vector<double>> &M) {
    for (size_t i = 0; i < M.size(); i++) {
        for (size_t j = 0; j < M[i].size(); j++) {
            std::printf("%10.1f", M[i][j]);
        }
        std::printf("\n");
    }
}

// Debug-print matrix of ints (not used by main, kept for parity)
static void print_matrix_d(const std::vector<std::vector<int>> &M) {
    for (size_t i = 0; i < M.size(); i++) {
        for (size_t j = 0; j < M[i].size(); j++) {
            std::printf("%4d", M[i][j]);
        }
        std::printf("\n");
    }
}

Parm parm_reader(const std::string &filename) {
    std::ifstream file(filename.c_str());
    if (!file) {
        std::cerr << "Error opening parm file: " << filename << "\n";
        std::exit(1);
    }

    // Storage vectors
    std::vector<std::string> TITLE;
    std::vector<int> POINTERS;
    std::vector<std::string> ATOM_NAME;
    std::vector<double> CHARGE;
    std::vector<double> MASS;
    std::vector<int> ATOM_TYPE_INDEX;
    std::vector<int> NUMBER_EXCLUDED_ATOMS;
    std::vector<int> NONBONDED_PARM_INDEX;
    std::vector<std::string> RESIDUE_LABEL;
    std::vector<int> RESIDUE_POINTER;
    std::vector<double> BondFC;   // force constant
    std::vector<double> BondI;    // ideal bond lenth
    std::vector<double> AngleFC;  // force constant
    std::vector<double> AngleI;   // ideal bond lenth
    std::vector<double> DihedFC;  // force constant
    std::vector<double> DihedPer; // PERIODICITY
    std::vector<double> DihedPha; // PHASE
    std::vector<double> SCEE_SCALE_V; // 1-4 Scale for ele 
    std::vector<double> SCNB_SCALE_V; // 1-4 scale for vdw
    std::vector<double> LENNARD_JONES_ACOEF;
    std::vector<double> LENNARD_JONES_BCOEF;
    std::vector<Bond> bonds;
    std::vector<Angle> angles;
    std::vector<Dihedral> dihedrals;
    std::vector<int> temp_bond_array;
    std::vector<int> temp_angle_array;
    std::vector<int> temp_dihed_array;
    std::vector<std::string> AMBER_ATOM_TYPE;
    // (other fields omitted since not used later; kept logic similar)

    // Flags
    bool F_TITLE                      = false;
    bool F_POINTERS                   = false;
    bool F_ATOM_NAME                  = false;
    bool F_CHARGE                     = false;
    bool F_MASS                       = false;
    bool F_ATOM_TYPE_INDEX            = false;
    bool F_NUMBER_EXCLUDED_ATOMS      = false;
    bool F_NONBONDED_PARM_INDEX       = false;
    bool F_RESIDUE_LABEL              = false;
    bool F_RESIDUE_POINTER            = false;
    bool F_BOND_FORCE_CONSTANT        = false;
    bool F_BOND_EQUIL_VALUE           = false;
    bool F_ANGLE_FORCE_CONSTANT       = false;
    bool F_ANGLE_EQUIL_VALUE          = false;
    bool F_DIHEDRAL_FORCE_CONSTANT    = false;
    bool F_DIHEDRAL_PERIODICITY       = false;
    bool F_DIHEDRAL_PHASE             = false;
    bool F_SCEE_SCALE_FACTOR          = false;
    bool F_SCNB_SCALE_FACTOR          = false;
    // %FLAG SCEE_SCALE_FACTOR  // consider adding.  1-4 electrostatic scaling constant. 1.0/1.2 
    // %FLAG SCNB_SCALE_FACTOR  // consider adding.  1-4 VDW scaling constant. 1.0/2.0
    bool F_SOLTY                      = false;
    bool F_LENNARD_JONES_ACOEF        = false;
    bool F_LENNARD_JONES_BCOEF        = false;
    bool F_BONDS_INC_HYDROGEN         = false;
    bool F_BONDS_WITHOUT_HYDROGEN     = false;
    bool F_ANGLES_INC_HYDROGEN        = false;
    bool F_ANGLES_WITHOUT_HYDROGEN    = false;
    bool F_DIHEDRALS_INC_HYDROGEN     = false;
    bool F_DIHEDRALS_WITHOUT_HYDROGEN = false;
    bool F_EXCLUDED_ATOMS_LIST        = false;
    bool F_HBOND_ACOEF                = false;
    bool F_HBOND_BCOEF                = false;
    bool F_HBCUT                      = false;
    bool F_AMBER_ATOM_TYPE            = false;
    bool F_TREE_CHAIN_CLASSIFICATION  = false;
    bool F_JOIN_ARRAY                 = false;
    bool F_IROTAT                     = false;
    bool F_RADII                      = false;
    bool F_SCREEN                     = false;

    std::string line;
    while (std::getline(file, line)) {
        std::string line_raw = line;
        auto split_line = split_whitespace(line_raw);

        if (split_line.size() > 1) {
            if (split_line[0] == "%FLAG") {
                // reset all flags
                F_TITLE                      = false;
                F_POINTERS                   = false;
                F_ATOM_NAME                  = false;
                F_CHARGE                     = false;
                F_MASS                       = false;
                F_ATOM_TYPE_INDEX            = false;
                F_NUMBER_EXCLUDED_ATOMS      = false;
                F_NONBONDED_PARM_INDEX       = false;
                F_RESIDUE_LABEL              = false;
                F_RESIDUE_POINTER            = false;
                F_BOND_FORCE_CONSTANT        = false;
                F_BOND_EQUIL_VALUE           = false;
                F_ANGLE_FORCE_CONSTANT       = false;
                F_ANGLE_EQUIL_VALUE          = false;
                F_DIHEDRAL_FORCE_CONSTANT    = false;
                F_DIHEDRAL_PERIODICITY       = false;
                F_DIHEDRAL_PHASE             = false;
                F_SCEE_SCALE_FACTOR          = false;
                F_SCNB_SCALE_FACTOR          = false;
                F_SOLTY                      = false;
                F_LENNARD_JONES_ACOEF        = false;
                F_LENNARD_JONES_BCOEF        = false;
                F_BONDS_INC_HYDROGEN         = false;
                F_BONDS_WITHOUT_HYDROGEN     = false;
                F_ANGLES_INC_HYDROGEN        = false;
                F_ANGLES_WITHOUT_HYDROGEN    = false;
                F_DIHEDRALS_INC_HYDROGEN     = false;
                F_DIHEDRALS_WITHOUT_HYDROGEN = false;
                F_EXCLUDED_ATOMS_LIST        = false;
                F_HBOND_ACOEF                = false;
                F_HBOND_BCOEF                = false;
                F_HBCUT                      = false;
                F_AMBER_ATOM_TYPE            = false;
                F_TREE_CHAIN_CLASSIFICATION  = false;
                F_JOIN_ARRAY                 = false;
                F_IROTAT                     = false;
                F_RADII                      = false;
                F_SCREEN                     = false;
            }

            if (split_line[0] == "%FLAG" && split_line[1] == "TITLE")
                F_TITLE = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "POINTERS")
                F_POINTERS = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "ATOM_NAME")
                F_ATOM_NAME = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "CHARGE")
                F_CHARGE = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "MASS")
                F_MASS = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "ATOM_TYPE_INDEX")
                F_ATOM_TYPE_INDEX = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "NUMBER_EXCLUDED_ATOMS")
                F_NUMBER_EXCLUDED_ATOMS = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "NONBONDED_PARM_INDEX")
                F_NONBONDED_PARM_INDEX = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "RESIDUE_LABEL")
                F_RESIDUE_LABEL = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "RESIDUE_POINTER")
                F_RESIDUE_POINTER = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "BOND_FORCE_CONSTANT")
                F_BOND_FORCE_CONSTANT = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "BOND_EQUIL_VALUE")
                F_BOND_EQUIL_VALUE = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "ANGLE_FORCE_CONSTANT")
                F_ANGLE_FORCE_CONSTANT = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "ANGLE_EQUIL_VALUE")
                F_ANGLE_EQUIL_VALUE = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "DIHEDRAL_FORCE_CONSTANT")
                F_DIHEDRAL_FORCE_CONSTANT = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "DIHEDRAL_PERIODICITY")
                F_DIHEDRAL_PERIODICITY = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "DIHEDRAL_PHASE")
                F_DIHEDRAL_PHASE = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "SCEE_SCALE_FACTOR")
                F_SCEE_SCALE_FACTOR = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "SCNB_SCALE_FACTOR")
                F_SCNB_SCALE_FACTOR = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "SOLTY")
                F_SOLTY = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "LENNARD_JONES_ACOEF")
                F_LENNARD_JONES_ACOEF = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "LENNARD_JONES_BCOEF")
                F_LENNARD_JONES_BCOEF = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "BONDS_INC_HYDROGEN")
                F_BONDS_INC_HYDROGEN = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "BONDS_WITHOUT_HYDROGEN")
                F_BONDS_WITHOUT_HYDROGEN = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "ANGLES_INC_HYDROGEN")
                F_ANGLES_INC_HYDROGEN = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "ANGLES_WITHOUT_HYDROGEN")
                F_ANGLES_WITHOUT_HYDROGEN = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "DIHEDRALS_INC_HYDROGEN")
                F_DIHEDRALS_INC_HYDROGEN = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "DIHEDRALS_WITHOUT_HYDROGEN")
                F_DIHEDRALS_WITHOUT_HYDROGEN = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "EXCLUDED_ATOMS_LIST")
                F_EXCLUDED_ATOMS_LIST = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "HBOND_ACOEF")
                F_HBOND_ACOEF = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "HBOND_BCOEF")
                F_HBOND_BCOEF = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "HBCUT")
                F_HBCUT = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "AMBER_ATOM_TYPE")
                F_AMBER_ATOM_TYPE = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "TREE_CHAIN_CLASSIFICATION")
                F_TREE_CHAIN_CLASSIFICATION = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "JOIN_ARRAY")
                F_JOIN_ARRAY = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "IROTAT")
                F_IROTAT = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "RADII")
                F_RADII = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "SCREEN")
                F_SCREEN = true;
        }

        // Now parse values for each active flag block
        if (F_POINTERS) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 8);
                    field = remove_spaces(field);
                    if (!field.empty()) {
                        POINTERS.push_back(std::atoi(field.c_str()));
                    }
                    i += 8;
                }
            }
        }
        if (F_ATOM_NAME) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 4);
                    if (!field.empty())
                        ATOM_NAME.push_back(field);
                    i += 4;
                }
            }
        }
        if (F_CHARGE) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        CHARGE.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }
        if (F_MASS) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        MASS.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }
        if (F_ATOM_TYPE_INDEX) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 8);
                    field = remove_spaces(field);
                    if (!field.empty())
                        ATOM_TYPE_INDEX.push_back(std::atoi(field.c_str()));
                    i += 8;
                }
            }
        }
        if (F_NONBONDED_PARM_INDEX) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 8);
                    field = remove_spaces(field);
                    if (!field.empty())
                        // Python: append(int(field)-1)
                        NONBONDED_PARM_INDEX.push_back(std::atoi(field.c_str()) - 1);
                    i += 8;
                }
            }
        }
        if (F_RESIDUE_LABEL) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 4);
                    if (!field.empty())
                        RESIDUE_LABEL.push_back(field);
                    i += 4;
                }
            }
        }
        if (F_RESIDUE_POINTER) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 8);
                    field = remove_spaces(field);
                    if (!field.empty())
                        RESIDUE_POINTER.push_back(std::atoi(field.c_str()));
                    i += 8;
                }
            }
        }
        if (F_BOND_FORCE_CONSTANT) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        BondFC.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }

        if (F_BOND_EQUIL_VALUE) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        BondI.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }

        if (F_ANGLE_FORCE_CONSTANT) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        AngleFC.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }

        if (F_ANGLE_EQUIL_VALUE) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        AngleI.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }

        if (F_DIHEDRAL_FORCE_CONSTANT) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        DihedFC.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }

        if (F_DIHEDRAL_PERIODICITY) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        DihedPer.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }

        if (F_DIHEDRAL_PHASE) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        DihedPha.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }

        if (F_SCEE_SCALE_FACTOR) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        SCEE_SCALE_V.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }
        
        if (F_SCNB_SCALE_FACTOR) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        SCNB_SCALE_V.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }

        if (F_LENNARD_JONES_ACOEF) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        LENNARD_JONES_ACOEF.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }
        if (F_LENNARD_JONES_BCOEF) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 16);
                    field = remove_spaces(field);
                    if (!field.empty())
                        LENNARD_JONES_BCOEF.push_back(std::atof(field.c_str()));
                    i += 16;
                }
            }
        }

        
        if (F_BONDS_INC_HYDROGEN) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                //std::cout << s << std::endl;
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 8);
                    field = remove_spaces(field);
                    if (!field.empty())
                        //temp_array.push_back(std::atof(field.c_str()));
                        //std::cout << field.c_str() << std::endl;
                        temp_bond_array.push_back(std::atoi(field.c_str()));
                        //temp_array.push_back(field.c_str());
                    i += 8;
                }
            //exit(0);
            }

        }

        if (F_BONDS_WITHOUT_HYDROGEN) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 8);
                    field = remove_spaces(field);
                    if (!field.empty())
                        //temp_array.push_back(std::atof(field.c_str()));
                        temp_bond_array.push_back(std::atoi(field.c_str()));
                        //temp_array.push_back(field.c_str());
                    i += 8;
                }
            }
        }

        if (F_ANGLES_INC_HYDROGEN) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                //std::cout << s << std::endl;
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 8);
                    field = remove_spaces(field);
                    if (!field.empty())
                        //temp_array.push_back(std::atof(field.c_str()));
                        //std::cout << field.c_str() << std::endl;
                        temp_angle_array.push_back(std::atoi(field.c_str()));
                        //temp_array.push_back(field.c_str());
                    i += 8;
                }
            //exit(0);
            }

        }

        if (F_ANGLES_WITHOUT_HYDROGEN) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 8);
                    field = remove_spaces(field);
                    if (!field.empty())
                        //temp_array.push_back(std::atof(field.c_str()));
                        temp_angle_array.push_back(std::atoi(field.c_str()));
                        //temp_array.push_back(field.c_str());
                    i += 8;
                }
            }
        }

        if (F_DIHEDRALS_INC_HYDROGEN) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                //std::cout << s << std::endl;
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 8);
                    field = remove_spaces(field);
                    if (!field.empty())
                        //temp_array.push_back(std::atof(field.c_str()));
                        //std::cout << field.c_str() << std::endl;
                        temp_dihed_array.push_back(std::atoi(field.c_str()));
                        //temp_array.push_back(field.c_str());
                    i += 8;
                }
            //exit(0);
            }

        }

        if (F_DIHEDRALS_WITHOUT_HYDROGEN) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 8);
                    field = remove_spaces(field);
                    if (!field.empty())
                        //temp_array.push_back(std::atof(field.c_str()));
                        temp_dihed_array.push_back(std::atoi(field.c_str()));
                        //temp_array.push_back(field.c_str());
                    i += 8;
                }
            }
        }

        if (F_AMBER_ATOM_TYPE) {
            if (!line.empty() && line[0] != '%') {
                std::string s = strip_newline(line);
                for (size_t i = 0; i < s.size();) {
                    std::string field = s.substr(i, 4);
                    if (!field.empty())
                        AMBER_ATOM_TYPE.push_back(field);
                    i += 4;
                }
            }
        }
    }

    int msize = CHARGE.size(); //number of atoms.
    std::vector<std::vector<int>> M_bonded;   // MxM matrix for if something is 1-2,1-3,1-4 -> 0 if not bonded, 2 if 1-2, 3 if 1-3, and 4 if 1-4 
    M_bonded.assign(msize+1, std::vector<int>(msize+1, 0));

    //std::vector<Bond> tbonds;
    // bonds
    int count_b = 0;
    for (size_t i = 0; i < temp_bond_array.size(); i++) {
         int a1, a2, bc;
         if (count_b == 0){
            a1 = temp_bond_array[i];
            count_b = count_b + 1;
         }else if (count_b == 1){
            a2 = temp_bond_array[i];
            count_b = count_b + 1;
         }else if (count_b == 2){
            bc = temp_bond_array[i];
            Bond bond;
            bond.atom1 = a1;
            bond.atom2 = a2;
            //std::cout            << a1 << " " << a2 << " " << bc << std::endl ;
            bond.forceC = BondFC[bc-1];
            bond.ideal = BondI[bc-1];
            //std::cout << "BOND: " << bond.atom1 << " " ;
            //std::cout             << bond.atom2 << " " ; 
            //std::cout             << bond.forceC << " " ; 
            //std::cout             << bond.ideal << std::endl ; 
   
            //tbonds.push_back(bond);
            bonds.push_back(bond);
            count_b = 0;
            //std::cout             << a1/3 << " " << a2/3 << std::endl;
            //std::cout             <<  M_bonded[a1/3][a2/3] << std::endl;
            M_bonded[a1/3][a2/3] = 2; //a2 / 3.0 + 1 on [1, ..., N], a2 / 3.0 on [0, ..., N - 1]
            M_bonded[a2/3][a1/3] = 2;
            //std::cout             <<  M_bonded[a1/3][a2/3] << std::endl;
            //exit(0);
         }
    }



    //std::vector<Angle> tangles;
    // angles
    int count_a = 0;
    for (size_t i = 0; i < temp_angle_array.size(); i++) {
         int a1, a2, a3, bc;
         if (count_a == 0){
            a1 = temp_angle_array[i];
            count_a = count_a + 1;
         }else if (count_a == 1){
            a2 = temp_angle_array[i];
            count_a = count_a + 1;
         }else if (count_a == 2){
            a3 = temp_angle_array[i];
            count_a = count_a + 1;
         }else if (count_a == 3){
            bc = temp_angle_array[i];
            Angle angle;
            angle.atom1 = a1;
            angle.atom2 = a2;
            angle.atom3 = a3;
            //std::cout            << a1 << " " << a2 << " " << bc << std::endl ;
            angle.forceC = AngleFC[bc-1];
            angle.ideal = AngleI[bc-1];
            //std::cout << "ANGLE: " << angle.atom1 << " " ;
            //std::cout              << angle.atom2 << " " ; 
            //std::cout              << angle.atom3 << " " ; 
            //std::cout              << angle.forceC << " " ; 
            //std::cout              << angle.ideal << std::endl ; 
   
            //tangles.push_back(angle);
            angles.push_back(angle);
            count_a = 0;
            M_bonded[a1/3][abs(a3)/3] = 3; // a3/3.0+1
            M_bonded[abs(a3)/3][a1/3] = 3; // a3/3.0+1
         }
    }


    //std::vector<Dihedral> tdiheds;
    // dihedral angles
    int count_d = 0;
    //std::cout << "temp_dihed_array.size() = " << temp_dihed_array.size() << std::endl;
    //std::cout << " num dihed = " << temp_dihed_array.size() / 5 << std::endl;
    //exit(0);
    for (size_t i = 0; i < temp_dihed_array.size(); i++) {
         int a1, a2, a3, a4, bc;
         if (count_d == 0){
            a1 = temp_dihed_array[i];
            count_d = count_d + 1;
         }else if (count_d == 1){
            a2 = temp_dihed_array[i];
            count_d = count_d + 1;
         }else if (count_d == 2){
            a3 = temp_dihed_array[i];
            count_d = count_d + 1;
         }else if (count_d == 3){
            a4 = temp_dihed_array[i];
            count_d = count_d + 1;
         }else if (count_d == 4){
            bc = temp_dihed_array[i];
            Dihedral dihed;
            dihed.atom1 = a1;
            dihed.atom2 = a2;
            dihed.atom3 = a3;
            dihed.atom4 = a4;
            //std::cout            << a1 << " " << a2 << " " << a3 << " " << a4 << " " << bc << std::endl ;
            //std::cout    << DihedFC[bc-1]  << std::endl ;
            dihed.forceC = DihedFC[bc-1];
            dihed.period = DihedPer[bc-1];
            dihed.phase = DihedPha[bc-1];
            //dihed.SCEE_SCALE = SCEE_SCALE_V[bc-1];
            dihed.ele14scale = 1.0/SCEE_SCALE_V[bc-1];
            //dihed.SCNB_SCALE = SCNB_SCALE_V[bc-1];
            dihed.vdw14scale = 1.0/SCNB_SCALE_V[bc-1];
            //std::cout << "DIHED: " << dihed.atom1  << " " ;
            //std::cout              << dihed.atom2  << " " ; 
            //std::cout              << dihed.atom3  << " " ; 
            //std::cout              << dihed.atom4  << std::endl; 
            // https://ambermd.org/FileFormats.php  
            // https://docs.mdanalysis.org/2.7.0/documentation_pages/topology/TOPParser.html
            // 1) The atom numbers in the following arrays that describe bonds, angles, 
            //    and dihedrals are coordinate array indexes for runtime speed. 
            //    The true atom number equals the absolute value of the number divided by three, 
            //    plus one.
            // 2) If the fourth atom in a dihedral entry is given a negative value, 
            //    this indicates that it is an improper. 
            // 3) If the third atom in a dihedral entry is given a negative value, 
            //    this indicates that it 1-4 NB interactions are ignored for this dihedrals. 
            //    This could be due to the dihedral within a ring, or if it is part of a 
            //    multi-term dihedral definition or if it is an improper.
            //
            //
            // We should ignore impropers in non-bonded calc 
            if (dihed.atom4 < 0) { 
                 //std::cout << "\n improper :: M_bonded = ";
                 //std::cout <<  M_bonded[a1/3][abs(a4)/3] << std::endl;
                 //std::cout << "im dih i = "<< i << " ele14scale = " << dihed.ele14scale << std::endl;
                 //std::cout << "im dih i = "<< i << " vdw14scale = " << dihed.vdw14scale << std::endl;
            } 
            else{ // if it is a standard dihedral:  
                 if (dihed.atom3 < 0) { 
                 //if (dihed.atom3 <= 0) { 
                     //std::cout << " ignore 1-4  \n";
                     if (M_bonded[a1/3][abs(a4)/3] == 0) { // only do this if it is not been assigned a number. 
                                                           // this is for not double conting or ignoring a group. 
                                                           // if the group has already been given a positive value then leave it
                                                           // if it hasn't then we sould flag to be ignored.
                       M_bonded[a1/3][abs(a4)/3] = -4; // though about using 5
                       M_bonded[abs(a4)/3][a1/3] = -4; // though about using 5
                       //std::cout << "not included dih i = "<< i << " ele14scale = " << dihed.ele14scale << std::endl;
                       //std::cout << "not included dih i = "<< i << " vdw14scale = " << dihed.vdw14scale << std::endl;
                     }
                 } else { // do not ignore
                     M_bonded[a1/3][abs(a4)/3] = 4;
                     M_bonded[abs(a4)/3][a1/3] = 4;
                     //std::cout << "dih i = "<< i << " ele14scale = " << dihed.ele14scale << std::endl;
                     //std::cout << "dih i = "<< i << " vdw14scale = " << dihed.vdw14scale << std::endl;
                 }
            }
            //std::cout              << dihed.forceC << " " ; 
            //std::cout              << dihed.period  << " " ; 
            //std::cout              << dihed.phase  << std::endl ; 
   
            //tdiheds.push_back(dihed);
            dihedrals.push_back(dihed);
            count_d = 0;
         }
    }


    //exit(0);
    // Build RESIDUE_ARRAY mapping atoms to residues
    std::vector<std::string> RESIDUE_ARRAY(ATOM_NAME.size(), "");

    for (size_t i = 0; i + 1 < RESIDUE_POINTER.size(); i++) {
        int start = RESIDUE_POINTER[i];
        int stop  = RESIDUE_POINTER[i + 1];
        for (int j = start; j < stop; j++) {
            // j-1 for 0-based index
            if (j - 1 >= 0 && j - 1 < (int)RESIDUE_ARRAY.size()) {
                RESIDUE_ARRAY[j - 1] = RESIDUE_LABEL[i];
            }
        }
    }
    // last residue
    if (!RESIDUE_POINTER.empty() && !RESIDUE_LABEL.empty()) {
        int last_start = RESIDUE_POINTER.back() - 1;
        for (int j = last_start; j < (int)ATOM_NAME.size(); j++) {
            RESIDUE_ARRAY[j] = RESIDUE_LABEL.back();
        }
    }

    //std::cout << "ATOM_NAME = " << ATOM_NAME.size() << "\n";
    //std::cout << "CHARGE = " << CHARGE.size() << "\n";
    //std::cout << "ATOM_TYPE_INDEX = " << ATOM_TYPE_INDEX.size() << "\n";

    int max_atom_type_index = 0;
    if (!ATOM_TYPE_INDEX.empty()) {
        max_atom_type_index = *std::max_element(ATOM_TYPE_INDEX.begin(), ATOM_TYPE_INDEX.end());
    }

    //std::cout << "max(ATOM_TYPE_INDEX) = " << max_atom_type_index << "\n";
    //std::cout << "max(ATOM_TYPE_INDEX)^2 = " << max_atom_type_index * max_atom_type_index << "\n";
    //std::cout << "NONBONDED_PARM_INDEX = " << NONBONDED_PARM_INDEX.size() << "\n";

    int max_nonbonded = 0;
    if (!NONBONDED_PARM_INDEX.empty()) {
        max_nonbonded = *std::max_element(NONBONDED_PARM_INDEX.begin(), NONBONDED_PARM_INDEX.end());
    }
    //std::cout << "max(NONBONDED_PARM_INDEX) = " << max_nonbonded << "\n";
    //std::cout << "LENNARD_JONES_ACOEF = " << LENNARD_JONES_ACOEF.size() << "\n";
    //std::cout << "LENNARD_JONES_BCOEF = " << LENNARD_JONES_BCOEF.size() << "\n";

    // build atom_type_uniq (for debug printing if desired)
    std::vector<std::string> atom_type_uniq;
    for (int AtomNum = 1; AtomNum <= max_atom_type_index; AtomNum++) {
        int count = 0;
        for (size_t i = 0; i < ATOM_TYPE_INDEX.size(); i++) {
            if (AtomNum == ATOM_TYPE_INDEX[i]) {
                if (count == 0) {
                    atom_type_uniq.push_back(AMBER_ATOM_TYPE[i]);
                }
                count++;
            }
        }
        //std::cout << "ATOM_TYPE_INDEX == " << AtomNum
        //          << " has N = " << count << " atoms of this type\n";
    }

    //std::cout << "\n\n LJ matrixes\n";

    // make matrices
    std::vector<std::vector<int>> M_index;
    std::vector<std::vector<double>> M_LJA;
    std::vector<std::vector<double>> M_LJB;

    M_index.assign(max_atom_type_index, std::vector<int>(max_atom_type_index, 0));
    M_LJA.assign(max_atom_type_index, std::vector<double>(max_atom_type_index, 0.0));
    M_LJB.assign(max_atom_type_index, std::vector<double>(max_atom_type_index, 0.0));

    // Pointer meaning: POINTERS[1] is NTYPES in AMBER prmtop
    int NTYPES = 0;
    if (POINTERS.size() > 1) {
        NTYPES = POINTERS[1];
    }

    for (int i = 0; i < NTYPES; i++) {
        for (int j = 0; j < NTYPES; j++) {
            int idx = NONBONDED_PARM_INDEX[NTYPES * i + j];
            M_index[i][j] = idx;
            M_LJA[i][j]   = LENNARD_JONES_ACOEF[idx];
            M_LJB[i][j]   = LENNARD_JONES_BCOEF[idx];
        }
    }

    Parm parm_stuff;
    parm_stuff.RESIDUE_POINTER = RESIDUE_POINTER;
    parm_stuff.RESIDUE_ARRAY   = RESIDUE_ARRAY;
    parm_stuff.ATOM_NAME       = ATOM_NAME;
    parm_stuff.AMBER_ATOM_TYPE = AMBER_ATOM_TYPE;
    parm_stuff.ATOM_TYPE_INDEX = ATOM_TYPE_INDEX;
    parm_stuff.CHARGE          = CHARGE;
    parm_stuff.MASS            = MASS;
    parm_stuff.M_LJA           = M_LJA;
    parm_stuff.M_LJB           = M_LJB;
    parm_stuff.bonds           = bonds;
    parm_stuff.angles          = angles;
    parm_stuff.diheds          = dihedrals;
    parm_stuff.M_bonded        = M_bonded;

    return parm_stuff;
}

// coord_reader: one frame worth of coordinates, plus remainder handling
bool coord_reader(
    int &line_count,
    std::ifstream &fh,
    Frame &frame1,
    const std::string &filename,
    int size,
    std::vector<std::string> &remainder
) {
    bool more_cord_flag = false;
    bool flag_break = false;
    std::cout << "IN coord_reader\n";

    // vals = copy of remainder
    std::vector<std::string> vals = remainder;
    remainder.clear();

    int ii = (int)vals.size();

    std::string line;
    while (std::getline(fh, line)) {
        more_cord_flag = true;
        auto data = split_whitespace(line);

        if (line_count == 0) {
            if (line.find("Restart") != std::string::npos ||
                line.find("default_name") != std::string::npos ||
                line.find("output") != std::string::npos ) {
                std::cout << "file " << filename << " is a restart file.\n";
                // Do NOT increment line_count, skip to next line
                continue;
            }
            std::cout << "line at count == 0 :: " << line << std::endl;
        }

        
        if (line_count > 0) {
            for (size_t i = 0; i < data.size(); i++) {
                if (ii > 3 * size - 1) {
                    // store remainder
                    for (size_t j = i; j < data.size(); j++) {
                        remainder.push_back(data[j]);
                    }
                    flag_break = true;
                    break;
                }
                vals.push_back(data[i]);
                ii++;
            }
            if (flag_break) {
                break;
            }
        }
        line_count++;
    }

    std::cout << "read in coord file\n";
    if (vals.size() % 3 != 0) {
        std::cerr << "error len(vals) mod 3 = " << (vals.size() % 3) << "\n";
        std::exit(1);
    }

    std::vector<Cord> cords;
    cords.reserve(vals.size() / 3);

    for (size_t i = 0; i < vals.size(); i += 3) {
        double x = std::atof(vals[i].c_str());
        double y = std::atof(vals[i + 1].c_str());
        double z = std::atof(vals[i + 2].c_str());
        Cord c { x, y, z };
        cords.push_back(c);
    }

    frame1.cords = cords;
    return more_cord_flag;
}

bool coord_writter(
    const std::string &filename,
    const Frame &frameX
){
    //std::ofstream outfileh((filename).c_str());
/*
  default_name
      27
   -19.2029201 -35.6845165   6.8076401 -19.4252840 -35.4411130   7.9804169
   -20.5258775 -35.3495088   8.4944800 -18.2134171 -35.2081008   8.8786104
*/
    std::ofstream outfileh(filename);

    outfileh << "default_name" << std::endl;
    int start1 = 0;
    int stop1 = frameX.cords.size();

    std::string s;
    char sb[ 7 ];  // You had better have room for what you are sprintf()ing!
    sprintf( sb, "%6d", stop1 );
    s = sb;
    
    //outfileh << stop1 << std::endl;
    outfileh << s << std::endl;


    for (int i = start1; i < stop1; i=i+2) {
        //outfileh << std::setw(12) << std::setprecision(10) << frameX.cords[i].x   << " "; 
        //outfileh << std::setw(12) << std::setprecision(10) << frameX.cords[i].y   << " "; 
        char sb1[ 13 ];  // You had better have room for what you are sprintf()ing!
        sprintf( sb1, "%12.7f", frameX.cords[i].x );
        s = sb1;
        outfileh << s; 
        sprintf( sb1, "%12.7f", frameX.cords[i].y );
        s = sb1;
        outfileh << s; 
        if (i+1 < stop1 ) {
           //outfileh << std::setw(12) << std::setprecision(10) << frameX.cords[i].z   << " "; 
           //outfileh << std::setw(12) << std::setprecision(10) << frameX.cords[i+1].x << " "; 
           //outfileh << std::setw(12) << std::setprecision(10) << frameX.cords[i+1].y << " "; 
           //outfileh << std::setw(12) << std::setprecision(10) << frameX.cords[i+1].z; 
           sprintf( sb1, "%12.7f", frameX.cords[i].z );
           s = sb1;
           outfileh << s; 
           sprintf( sb1, "%12.7f", frameX.cords[i+1].x );
           s = sb1;
           outfileh << s; 
           sprintf( sb1, "%12.7f", frameX.cords[i+1].y );
           s = sb1;
           outfileh << s; 
           sprintf( sb1, "%12.7f", frameX.cords[i+1].z );
           s = sb1;
           outfileh << s; 
        } else {
           //outfileh << std::setw(12) << std::setprecision(10) << frameX.cords[i].z; 
           sprintf( sb1, "%12.7f", frameX.cords[i].z );
           s = sb1;
           outfileh << s; 
        }
        outfileh << std::endl;
    }

    outfileh.close();
    return true;
}

// Distance between two coordinate points
double distance(const Cord &c1, const Cord &c2) {
    double dx = c1.x - c2.x;
    double dy = c1.y - c2.y;
    double dz = c1.z - c2.z;
    return std::sqrt(dx*dx + dy*dy + dz*dz);
}


double lenth_vec ( double x, double y, double z ){
     return std::sqrt(x*x + y*y + z*z);
}

double dot_vecs ( double x1, double y1, double z1, double x2, double y2, double z2 ){
     return (x1*x2 + y1*y2 + z1*z2);
}

double dist_vecs ( double x1, double y1, double z1, double x2, double y2, double z2 ){
     return std::sqrt(pow((x1-x2),2.0) + pow((y1-y2),2.0) + pow((z1-z2),2.0));
}

struct vec {
     double x;
     double y;
     double z;
}; 

vec cross_vecs ( double x1, double y1, double z1, double x2, double y2, double z2 ){

     vec v;
     v.x = y1*z2-z1*y2; //s1 = a2b3-a3b2 = y1*z2-z1*y2  1->x,2->y,3->z, a->1,b-2
     v.y = z1*x2-x1*z2; //s2 = a3b1-a1b3 = z1*x2-x1*z2  
     v.z = x1*y2-y1*x2; //s3 = a1b2-a2b1 = x1*y2-y1*x2  

     return v;
}


// Angle between three coordinate points
// returns an angle 
double cal_angle(const Cord &c1, const Cord &c2, const Cord &c3) {

    double v1x = c2.x - c1.x;
    double v1y = c2.y - c1.y;
    double v1z = c2.z - c1.z;

    double v2x = c2.x - c3.x;
    double v2y = c2.y - c3.y;
    double v2z = c2.z - c3.z;
    
    double lenv1 = lenth_vec(v1x,v1y,v1z);
    double lenv2 = lenth_vec(v2x,v2y,v2z);
    double dot   = dot_vecs(v1x,v1y,v1z,v2x,v2y,v2z);

    //std::cout << c1.x << " "<< c1.y << " " << c1.z << std::endl;
    //std::cout << c3.x << " "<< c3.y << " " << c3.z << std::endl;
    //std::cout << "dot = " << dot << "; lenv1 = " << lenv1 <<  "; lenv2 = "  << lenv2 << "; dot/(lenv1 lenv2) = " << dot/(lenv1*lenv2) << std::endl;


    if (lenv1 < 0.0001) { 
        lenv1 = 0.0001;
    }
    if (lenv2 < 0.0001) { 
        lenv2 = 0.0001;
    }

    if(dot<0.0001 and dot>-0.0001){
       dot = 0.0;
    }   
    
    double val = dot/(lenv1*lenv2);

    if (std::isnan(val)){
        std::cout << v1x << " " << v1y << " " << v1z << std::endl;
        std::cout << v2x << " " << v2y << " " << v2z << std::endl;
        std::cout << "in angle :: dot = " << dot << "; lenv1 = " << lenv1 <<  "; lenv2 = "  << lenv2 << "; dot/(lenv1 lenv2) = " << val << std::endl;
        val = 1;
        exit(0);
    }

    if (val > 1.0){
        val = 1.0;
    }
    if (val < -1.0){
        val = -1.0;
    }
    //double PI = 3.14159265359;

    //return std::acos(dot/(lenv1*lenv2)) * 180.0 / PI;
    //return std::acos(dot/(lenv1*lenv2));
    return std::acos(val);
}


// Dihedral between four coordinate points
// returns an angle in degrees
double cal_dihedral(const Cord &c1, const Cord &c2, const Cord &c3, const Cord &c4) {
    double u1x = c2.x - c1.x;
    double u1y = c2.y - c1.y;
    double u1z = c2.z - c1.z;

    double u2x = c3.x - c2.x;
    double u2y = c3.y - c2.y;
    double u2z = c3.z - c2.z;

    double u3x = c4.x - c3.x;
    double u3y = c4.y - c3.y;
    double u3z = c4.z - c3.z;

    vec u1xu2,u2xu3;
    u1xu2 = cross_vecs(u1x,u1y,u1z,u2x,u2y,u2z); // (u1 x u2)
    u2xu3 = cross_vecs(u2x,u2y,u2z,u3x,u3y,u3z); // (u2 x u3)
    
    double dot =   dot_vecs (u1xu2.x,u1xu2.y,u1xu2.z,u2xu3.x,u2xu3.y,u2xu3.z);
    double lenv1 = lenth_vec(u1xu2.x,u1xu2.y,u1xu2.z);
    double lenv2 = lenth_vec(u2xu3.x,u2xu3.y,u2xu3.z);

    
    //std::cout << "dot = " << dot << "; lenv1 = " << lenv1 <<  "; lenv2 = "  << lenv2 << "; dot/(lenv1 lenv2) = " << val << std::endl;
/*
*/
    if (lenv1 < 0.0001) { 
        lenv1 = 0.0001;
    }
    if (lenv2 < 0.0001) { 
        lenv2 = 0.0001;
    }

    //if(dot<0.0001){
    if(dot<0.0001 and dot>-0.0001){
       dot = 0.0;
    }   

    double val = dot/(lenv1*lenv2);

/*
    if (dot < 0.00001){
        val = 0.0;
        //exit(0);
    }
*/

    if (std::isnan(val)){
        std::cout << u1xu2.x << " " << u1xu2.y << " " << u1xu2.z << std::endl;
        std::cout << u2xu3.x << " " << u2xu3.y << " " << u2xu3.z << std::endl;
        std::cout << "in dihed:: dot = " << dot << "; lenv1 = " << lenv1 <<  "; lenv2 = "  << lenv2 << "; dot/(lenv1 lenv2) = " << val << std::endl;
        val = 1;
        exit(0);
    }

/*
    if ((val-1.0) < 0.0001){
    //if ((dot/(lenv1*lenv2)-1.0) < 0.0001){
       //std::cout << u1xu2.x << " " << u1xu2.y << " " << u1xu2.z << " " << u2xu3.x << " " << u2xu3.y << " " << u2xu3.z << std::endl;
       double dist = dist_vecs(u1xu2.x,u1xu2.y,u1xu2.z,u2xu3.x,u2xu3.y,u2xu3.z); 
       //std::cout << "dist = " << dist << std::endl;
       if (dist < 0.0001){
           return double(0.0);
       }
    }

        
    //if (lenv1 > 10000000.0 or lenv2 > 10000000.0) {
    //    std::cout<< "warning vec are large." << std::endl;
    //    return acos(0);
    //} 
*/
    if (val > 1.0){
        //std::cout<< " val = " << val << "should be between on [-1, 1]" << std::endl;
        //std::cout<< " dot = " << dot;
        //std::cout<< " lenv1 = " << lenv1;
        //std::cout<< " lenv2 = " << lenv2;
        //std::cout<<  std::endl;
        val = 1.0;
    }
    if (val < -1.0){
        //std::cout<< " val = " << val << "should be between on [-1, 1]" << std::endl;
        //std::cout<< " dot = " << dot;
        //std::cout<< " lenv1 = " << lenv1;
        //std::cout<< " lenv2 = " << lenv2;
        //std::cout<<  std::endl;
        val = -1.0;
    }

    //double ang = std::acos(dot/(lenv1*lenv2));
    double ang = std::acos(val);
/*    
    if (std::isnan(ang)){
        std::cout<< "ang = " << ang << std::endl; 
        std::cout<< " dot = " << dot;
        std::cout<< " lenv1 = " << lenv1;
        std::cout<< " lenv2 = " << lenv2;
        std::cout<<  std::endl;
    } 
*/
    return ang;
    //return std::acos(dot/(lenv1*lenv2));
}

// Improper Dihedral between four coordinate points
// returns an angle in degrees
double cal_improper(const Cord &c1, const Cord &c2, const Cord &c3, const Cord &c4) {
/*
    double u1x = c2.x - c1.x;
    double u1y = c2.y - c1.y;
    double u1z = c2.z - c1.z;

    double u2x = c3.x - c2.x;
    double u2y = c3.y - c2.y;
    double u2z = c3.z - c2.z;

    double u3x = c4.x - c2.x;
    double u3y = c4.y - c2.y;
    double u3z = c4.z - c2.z;

    double u4x = u2x + u1x;
    double u4y = u2y + u1y;
    double u4z = u2z + u1z;

    double dot =   dot_vecs (u3x,u3y,u3z,u4x,u4y,u4z);
    double lenv1 = lenth_vec(u3x,u3y,u3z);
    double lenv2 = lenth_vec(u4x,u4y,u4z);

    if (dot/(lenv1*lenv2)-1.0 < 0.0001){
       double dist = dist_vecs(u3x,u3y,u3z,u4x,u4y,u4z); 
       std::cout << "dist = " << dist << std::endl;
       if (dist < 0.0001){
           return double(0.0);
       }
    }

    if (lenv1 < 0.0001) { 
        lenv1 = 0.0001;
    }
    if (lenv2 < 0.0001) { 
        lenv2 = 0.0001;
    }

    return std::acos(dot/(lenv1*lenv2));
*/

    return cal_dihedral(c1, c2, c3, c4);

}


double teb_func(double b, double N, double M, double r){
               //printf("I am here in teb_func\n");
               //printf("%f,%f,%f,%f\n",b,N,M,r);
               //double b = 0.13,N=5.0,M=0.3;
               // x^2M = (x^2)^M
               //double sqrtPI = 1.77245385091;
               //double val  = ( N/(b*sqrtPI))*exp(-1.0*pow(pow((r/b),2.0),M));
               if (r < 0.0){
                   r = 0.0;
               }
               double val  =  N*exp(-1.0*pow(pow((r/b),2.0),M));
               //double val  = ( N/(b*sqrtPI))*exp(-1.0*pow((r/b),2.0*M));
               //cout << "val = " << val << endl;
               //printf("r=%f ,   val = %f\n",r,val);
               return val;
}



double vdw_energy_function(double A, double B, double r, int method) {
    if (method == 1){
        return A / std::pow(r, 12.0) - B / std::pow(r, 6.0);
    } else if (method == 2){
                         // b,        N,        M,                    // b,        N,        M,
        return A * teb_func(1.151669, 1.322028, 1.330330,r) - B * teb_func(0.906882, 5.863632, 4.429459,r);
    } else if (method == 3){ // just repultion
                         // b,        N,        M,           
        return A * teb_func(1.151669, 1.322028, 1.330330,r) ;
        //return A * teb_func(0.5, 10000.0, 1,r) ;
    } else if (method == 4){ // just bonded
        return 0.0 ;
    }
}
  

double es_energy_function(double q1, double q2, double r, int method) {
    if (method == 1){ // standard 
        return q1 * q2 / r;
    } else if (method == 2){
                               // b,        N,        M,
        return q1 * q2 * teb_func(0.879128, 4.733930, 0.336965,r);
    } else if (method == 3){
        return 0.0;
    } else if (method == 4){ // just bonded
        return 0.0 ;
    }
}

double energy_function(double A, double B, double q1, double q2, double r, int method) {
    //return A / std::pow(r, 12.0) - B / std::pow(r, 6.0) + q1 * q2 / r;
    return vdw_energy_function(A,B,r,method) + es_energy_function(q1,q2,r,method);
}

struct EnergyTriple {
    double Eint;
    double Evdw;
    double Ees;
};

struct EnergyBonded {
    double Ebond;  // bond
    double Eangle; // angle
    double Edihed; // dihedral
    //double Eimpro; // improper dyhedral
};




EnergyBonded bonded_Energy(
    const Parm &parm_stuff,
    const Frame &frameX
) {

   //std::cout << "number of atoms:" << frameX.cords.size() << std::endl;
   //std::cout << "number of bonds:" << parm_stuff.bonds.size() << std::endl;
   //std::cout << "number of angles:" << parm_stuff.angles.size() << std::endl;
   //std::cout << "number of dihedrals:" << parm_stuff.diheds.size() << std::endl;

   double Ebond = 0.0;
   for (size_t i = 0; i < parm_stuff.bonds.size(); i++){
        int a1 = parm_stuff.bonds[i].atom1/3 + 1;
        int a2 = parm_stuff.bonds[i].atom2/3 + 1;
        
        //double 
        double fC = parm_stuff.bonds[i].forceC;
        double id = parm_stuff.bonds[i].ideal;

        double d = distance(frameX.cords[a1-1], frameX.cords[a2-1]); 
        //double d = distance(frameX.cords[a1], frameX.cords[a2]); 
        if (std::isnan(d)){
            d = 0.0;
        }
        double E = fC*std::pow((d-id),2.0);
        //std::cout << "E = " << E << std::endl;
        Ebond = Ebond + E;
   }
   //std::cout << "Ebond = " << Ebond << std::endl;

   double Eangle = 0.0;
   for (size_t i = 0; i < parm_stuff.angles.size(); i++){
        //int a1 = std::abs(parm_stuff.angles[i].atom1)/3 + 1;
        int a1 = parm_stuff.angles[i].atom1/3 + 1;
        int a2 = parm_stuff.angles[i].atom2/3 + 1;
        int a3 = parm_stuff.angles[i].atom3/3 + 1;

        //double
        double fC = parm_stuff.angles[i].forceC;
        double id = parm_stuff.angles[i].ideal;

        //std::cout << a1 << " ";
        //std::cout << a2 << " ";
        //std::cout << a3 << std::endl;
        double a = cal_angle(frameX.cords[a1-1], frameX.cords[a2-1], frameX.cords[a3-1]);
        //double a = cal_angle(frameX.cords[a1], frameX.cords[a2],frameX.cords[a3]);
        //std::cout << "angle = " << a << std::endl;
        //std::cout << "id angle = " << id << std::endl;
        double E = fC*std::pow((a-id),2.0);
        //std::cout << "E = " << E << std::endl;
        Eangle = Eangle + E;
   }
   //std::cout << "Eangle = " << Eangle << std::endl;

   double Edihedral = 0.0;
   for (size_t i = 0; i < parm_stuff.diheds.size(); i++){
        int a1 = parm_stuff.diheds[i].atom1/3 + 1;
        int a2 = parm_stuff.diheds[i].atom2/3 + 1;
        int a3 = std::abs(parm_stuff.diheds[i].atom3)/3 + 1;
        int a4 = std::abs(parm_stuff.diheds[i].atom4)/3 + 1;

        //double
        double fC = parm_stuff.diheds[i].forceC;
        double period = parm_stuff.diheds[i].period;
        double phase = parm_stuff.diheds[i].phase;

        double dih;
        if (parm_stuff.diheds[i].atom4 >= 0){
           dih = cal_dihedral(frameX.cords[a1-1], frameX.cords[a2-1], frameX.cords[a3-1],frameX.cords[a4-1]);
        } else { // atom4  is negative so is an improper
           //std::cout << "...improper..." << std::endl;
           dih = cal_improper(frameX.cords[a1-1], frameX.cords[a2-1], frameX.cords[a3-1],frameX.cords[a4-1]); 
        }
        //double E = 0.5*fC*(1.0+std::cos(period*dih+phase));
        double E = fC*(1.0+std::cos(period*dih+phase));
        if (std::isnan(E)){
           std::cout << a1 << " " << a2 << " " << a3 << " " << a4 << std::endl;
           std::cout << "dihed = "  << dih << "; E = " << E << std::endl;
           std::cout << "E = " << E << std::endl;
           E = 0.0;
        }
        Edihedral = Edihedral + E;
   }
   //std::cout << "Edihedral = " << Edihedral << std::endl;

   //exit(0);
   //EnergyBonded val;
   //val.Ebond = Ebond;
   //val.Eangle = Eangle;
   //val.Edihed = Edihedral;
   //return val;

   EnergyBonded out { Ebond, Eangle, Edihedral };
   return out;
}

EnergyTriple intermolecular_Energy(
    const Parm &parm_stuff,
    const Frame &frameX,
    int method
) {
    double Eint = 0.0;
    double Evdw = 0.0;
    double Ees  = 0.0;

    int start1 = 1;
    int stop1 = parm_stuff.CHARGE.size()+1;
    int start2 = 1;
    int stop2 = parm_stuff.CHARGE.size()+1;

    if (stop1 > (int)parm_stuff.CHARGE.size() + 1) {
        std::cout << "WARNING. stop1 > (len(parm_stuff.CHARGE)+1)\n";
    }
    if (stop2 > (int)parm_stuff.CHARGE.size() + 1) {
        std::cout << "WARNING. stop2 > (len(parm_stuff.CHARGE)+1)\n";
    }

    for (int i = start1; i < stop1; i++) {
        start2 = i+1;
        for (int j = start2; j < stop2; j++) {
            //std::cout << "i,j = " << i <<","<<j<<std::endl;
            if (i == j) {
                std::cout << "i==j. skip\n";
                continue;
            }
            double q1 = parm_stuff.CHARGE[i - 1];
            double q2 = parm_stuff.CHARGE[j - 1];
            int idx_i = parm_stuff.ATOM_TYPE_INDEX[i - 1] - 1;
            int idx_j = parm_stuff.ATOM_TYPE_INDEX[j - 1] - 1;

            double A  = parm_stuff.M_LJA[idx_i][idx_j];
            double B  = parm_stuff.M_LJB[idx_i][idx_j];
            double r  = distance(frameX.cords[i - 1], frameX.cords[j - 1]);

            double e = energy_function(A, B, q1, q2, r, method);
            Eint += e;
            Evdw += vdw_energy_function(A, B, r, method);
            Ees  += es_energy_function(q1, q2, r, method);
        }
    }

    EnergyTriple out { Eint, Evdw, Ees };
    return out;
}

struct pair {
      int one;
      int two;
};


bool generate_pairlist(
    const Parm &parm_stuff,
    const Frame &frameX,
    std::vector<pair> &list,
    std::vector<pair> &list14
) {
    list.clear();
    list14.clear();
    //double cutoff = 10.0; // I should make this a user speciffied value.
    //double cutoff = 20.0; // I should make this a user speciffied value.
    //double cutoff = 100000.0; // I should make this a user speciffied value.
    double cutoff = 20.0; // I should make this a user speciffied value.
    int start1 = 1;
    int stop1 = parm_stuff.CHARGE.size()+1;
    int start2 = 1;
    int stop2 = parm_stuff.CHARGE.size()+1;

    if (stop1 > (int)parm_stuff.CHARGE.size() + 1) {
        std::cout << "WARNING. stop1 > (len(parm_stuff.CHARGE)+1)\n";
    }
    if (stop2 > (int)parm_stuff.CHARGE.size() + 1) {
        std::cout << "WARNING. stop2 > (len(parm_stuff.CHARGE)+1)\n";
    }

    for (int i = start1; i < stop1; i++) {
        start2 = i+1;
        for (int j = start2; j < stop2; j++) {
            //std::cout << "i,j = " << i <<","<<j<<std::endl;
            if (i == j) {
                std::cout << "i==j. skip\n";
                continue;
            }
            pair tp;
            int b_int  = parm_stuff.M_bonded[i-1][j-1]; // if atom i is bonded, non-zerro 
            double r  = distance(frameX.cords[i - 1], frameX.cords[j - 1]);
            if (r > cutoff){ // only add to the pair list if they are within the cutoff distance. 
                continue;
            }
            if (b_int == 0){
                // if (r < 2.0){
                //    std::cout << " M_bonded[i-1][j-1] = " << parm_stuff.M_bonded[i-1][j-1] << std::endl;
                //    std::cout << " i = " << i << " j = " << j << " r = " << r << std::endl;
                // }
                tp.one = i;
                tp.two = j;
                list.push_back(tp);
            } else if(b_int == 4) { // 1-4, 2,3,-4 is ignored
            //} else if(b_int == 4 or b_int == -4) { // 1-4, 2,3 is ignored
                //std::cout << " i = " << i << " j = " << j << " r = " << r << std::endl;
                tp.one = i;
                tp.two = j;
                list14.push_back(tp);
            }

        }
    }

    std::cout << "size of pairlist = " << list.size() << std::endl;
    std::cout << "size of 1-4 pairlist = " << list14.size() << std::endl;
    
    return true;
}

EnergyTriple intermolecular_Energy_pairlist(
    const Parm &parm_stuff,
    const Frame &frameX,
    const std::vector <pair> &pairlist,
    const std::vector <pair> &pairlist14,
    int atom, // if atom is -1, do everything in the pair list if atom is positive integer skip all pair without that atom
              // this is useful in the minimizer. only those pair the inclue the atom of interest will need to be calculated
              // all others are not changing.  
    int method
) {
    double Eint = 0.0;
    double Evdw = 0.0;
    double Ees  = 0.0;


    for (size_t ii = 0; ii < pairlist.size(); ii++) {
            int i = pairlist[ii].one;
            int j = pairlist[ii].two;
        
            if (i == j) {
                std::cout << "i==j. skip\n";
                continue;
            }
            if (atom != -1){
              if (atom != i and atom !=j){ 
                continue;
              }
            }
            double q1 = parm_stuff.CHARGE[i - 1];
            double q2 = parm_stuff.CHARGE[j - 1];
            int idx_i = parm_stuff.ATOM_TYPE_INDEX[i - 1] - 1;
            int idx_j = parm_stuff.ATOM_TYPE_INDEX[j - 1] - 1;

            double A  = parm_stuff.M_LJA[idx_i][idx_j];
            double B  = parm_stuff.M_LJB[idx_i][idx_j];
            double r  = distance(frameX.cords[i - 1], frameX.cords[j - 1]);

            double e = energy_function(A, B, q1, q2, r, method);
            Eint += e;
            Evdw += vdw_energy_function(A, B, r, method);
            Ees  += es_energy_function(q1, q2, r, method);
            //std::cout << " i = " << i << " j = " << j << " q1 = " << q1 << " q2 = " << q2 << " r = " << r << std::endl;
            //exit(0);
    }
    //std::cout << "; VDW (no 1-4): " << Evdw  << "; ES (no 1-4): " << Ees << std::endl;
    // 1/2 for vdw
    // 1/1.2 for es
    double escale = 1.0/1.2;
    double vscale = 1.0/2.0;
    double Evdw14 = 0.0;
    double Ees14  = 0.0;
    for (int ii = 0; ii < pairlist14.size(); ii++) {
            int i = pairlist14[ii].one;
            int j = pairlist14[ii].two;

            if (i == j) {
                std::cout << "i==j. skip\n";
                continue;
            }
            if (atom != -1){
              if (atom != i and atom !=j){ 
                  continue;
              }
            }
            double q1 = parm_stuff.CHARGE[i - 1];
            double q2 = parm_stuff.CHARGE[j - 1];
            int idx_i = parm_stuff.ATOM_TYPE_INDEX[i - 1] - 1;
            int idx_j = parm_stuff.ATOM_TYPE_INDEX[j - 1] - 1;

            double A  = parm_stuff.M_LJA[idx_i][idx_j];
            double B  = parm_stuff.M_LJB[idx_i][idx_j];
            double r  = distance(frameX.cords[i - 1], frameX.cords[j - 1]);

            //double e = energy_function(A, B, q1, q2, r);
            //Eint += e;
            //Evdw += vdw_energy_function(A, B, r);
            //Ees  += es_energy_function(q1, q2, r);
            double ev = vscale * vdw_energy_function(A, B, r, method);
            double ee = escale * es_energy_function(q1, q2, r, method);
            Evdw14 += ev;
            Ees14 += ee;
            Eint += ev+ee;
            //if (r < 2.0) {
            //if (ee > 100.0 ) {
            //   std::cout << " i = " << i << " j = " << j << " q1 = " << q1 << " q2 = " << q2 << " r = " << r << std::endl;
            //   std::cout << " ee = " << ee << "; ev = " << ev << std::endl;
            //}
            //exit(0);
    }

    //std::cout << "; VDW (1-4): " << Evdw14  << "; ES (1-4): " << Ees14 << std::endl;

    Evdw += Evdw14;
    Ees  += Ees14;

    EnergyTriple out { Eint, Evdw, Ees };
    return out;
}

bool jiggle_atoms(
    Frame &frameX, // 
    const std::vector <int> &atomlist,
    double scale
){
    //double scale = 0.5;
    int random_value_int;
    double random_value;
    std::srand(std::time({})); // use current time as seed for random generator
    for (size_t a = 0; a < atomlist.size(); a++){
        int i = atomlist[a];
        random_value_int = std::rand();
        random_value = scale * (double(random_value_int)/double(RAND_MAX)- 0.5 );
        frameX.cords[i].x = frameX.cords[i].x +random_value;
        random_value_int = std::rand();
        random_value = scale * (double(random_value_int)/double(RAND_MAX)- 0.5 );
        frameX.cords[i].y = frameX.cords[i].y +random_value;
        random_value_int = std::rand();
        random_value = scale * (double(random_value_int)/double(RAND_MAX)- 0.5 );
        frameX.cords[i].z = frameX.cords[i].z +random_value;
    }
    return true;
}
// give a list of atoms to minimize on. 
// all atoms not in the list will not move (they will be held rigid. 
//
bool Energy_min_pairlist(
    const Parm &parm_stuff,
    //const Frame &frameX,
    //Frame frameX, // make a copy of the frame.
    Frame & frameX, // mod ori 
    const std::vector <pair> &pairlist,
    const std::vector <pair> &pairlist14,
    const std::vector <int> &atomlist,
    int method,
    int maxint // maxium interations
) {

    if (atomlist.size() == 0){
        std::cout << "exit... atomlist must be non empty" << std::endl;
        exit(0);
    }

    int vsize = 3*parm_stuff.CHARGE.size();
    double step = 0.001;
    //double step = 0.00000000001;

    std::vector<double> dEdx(vsize,0);   // derivitive
    //std::vector<double> dE(vsize,0);   // change in energy
    

    // calculat gradient. 
    EnergyBonded eb; 
    EnergyTriple e; 
    eb = bonded_Energy(parm_stuff, frameX); 
    e = intermolecular_Energy_pairlist(parm_stuff, frameX, pairlist, pairlist14,-1, method);
    double current = eb.Ebond + eb.Eangle +  eb.Edihed + e.Evdw + e.Ees;
    double old = current;
    std::cout << "atomlist.size() = " << atomlist.size() << std::endl;

    //for (size_t ii = 0; ii < 1000000; ii++){
    for (size_t ii = 0; ii < maxint; ii++){
        std::cout << "min::step = " << ii << std::endl;
        for (size_t a = 0; a < atomlist.size(); a++){
            int i = atomlist[a];
            float tot; 
            eb = bonded_Energy(parm_stuff, frameX); 
            e = intermolecular_Energy_pairlist(parm_stuff, frameX, pairlist, pairlist14,i, method);
            float ref = eb.Ebond + eb.Eangle +  eb.Edihed + e.Evdw + e.Ees ;
            //std::cout << " ref = " << ref << std::endl;
            // x cord 
            frameX.cords[i].x = frameX.cords[i].x + step ;
            eb = bonded_Energy(parm_stuff, frameX); 
            e = intermolecular_Energy_pairlist(parm_stuff, frameX, pairlist, pairlist14,i, method);
            tot = eb.Ebond + eb.Eangle +  eb.Edihed + e.Evdw + e.Ees ;
            //std::cout << " tot = " << tot << std::endl;
            dEdx[3*i] = (tot-ref)/step;
            //std::cout << " dEdx[3*i] = " << dEdx[3*i] << std::endl;
            frameX.cords[i].x = frameX.cords[i].x - step ;
            // y cord 
            frameX.cords[i].y = frameX.cords[i].y + step ;
            eb = bonded_Energy(parm_stuff, frameX); 
            e = intermolecular_Energy_pairlist(parm_stuff, frameX, pairlist, pairlist14,i,method);
            tot = eb.Ebond + eb.Eangle +  eb.Edihed + e.Evdw + e.Ees ;
            //std::cout << " tot = " << tot << std::endl;
            dEdx[3*i+1] = (tot-ref)/step;
            frameX.cords[i].y = frameX.cords[i].y - step ;
            // z cord
            frameX.cords[i].z = frameX.cords[i].z + step ;
            eb = bonded_Energy(parm_stuff, frameX); 
            e = intermolecular_Energy_pairlist(parm_stuff, frameX, pairlist, pairlist14,i,method);
            tot = eb.Ebond + eb.Eangle +  eb.Edihed + e.Evdw + e.Ees ;
            //std::cout << " tot = " << tot << std::endl;
            dEdx[3*i+2] = (tot-ref)/step;
            frameX.cords[i].z = frameX.cords[i].z - step ;
        }
        // should I normalize the step?
        // take a step -dE/dx
        // normilize vectory
        double sum2 = 0;
        //double scale = 0.0001;
        double scale = 0.001;
        //double scale = 0.000000001;

        for (size_t i = 0; i < vsize; i++){
             //std::cout << "i = "<< i << " dEdx[3*i] = " << dEdx[3*i] << std::endl;
             if (std::isnan(dEdx[i])){
                  std::cout << " warning energy is not a number ... set to zerro" << std::endl;
                  dEdx[i] = 0.0;
             }else if (dEdx[i] > 100.0) { 
                  dEdx[i] = 100.0;
             }else if (dEdx[i] < -100.0) { 
                  dEdx[i] = -100.0;
             } //else {
             //}
             sum2 = sum2+pow(dEdx[i],2);
        }

        std::cout << " sum2 = " << sum2 << std::endl;
        double norm; 
        //if (sum2 < 0.00000000001){
        if (sum2 == 0.0){
            norm = 1;
        } else{
            if (std::isnan(sum2)){
                norm = 100000000.0;
            } else{
                norm = sqrt(sum2);
            }
        }
        std::cout << " norm = " << norm << std::endl;
        
        for (size_t i = 0; i < vsize; i++){
             dEdx[i] = scale*dEdx[i]/norm;
             if (std::isnan(dEdx[i])){
                  std::cout << " warning energy is not a number ... set to zerro" << std::endl;
                  dEdx[i] = 0.0;
             }
        }
       
        for (size_t a = 0; a < atomlist.size(); a++){
            int i = atomlist[a];
            //std:: cout << dEdx[3*i+0] << std::endl;
            //std:: cout << dEdx[3*i+1] << std::endl;
            //std:: cout << dEdx[3*i+2] << std::endl;
            //frameX.cords[i].x = frameX.cords[i].x + dEdx[3*i+0] ;
            frameX.cords[i].x = frameX.cords[i].x - dEdx[3*i+0] ;
            frameX.cords[i].y = frameX.cords[i].y - dEdx[3*i+1] ;
            frameX.cords[i].z = frameX.cords[i].z - dEdx[3*i+2];
        }
    
        eb = bonded_Energy(parm_stuff, frameX); 
        e = intermolecular_Energy_pairlist(parm_stuff, frameX, pairlist, pairlist14,-1, method);
        old = current;
        current = eb.Ebond + eb.Eangle +  eb.Edihed + e.Evdw + e.Ees;
    
        std:: cout << e.Evdw << "+" << e.Ees <<"+" << eb.Ebond <<"+" << eb.Eangle <<"+" << eb.Edihed << std::endl;
        std:: cout << "Etot = " << current << std::endl;
        //if (fabs(current - old) < 0.0001){
        //if ((current - old) < 0.0001){
        if (( old - current) < 0.0001){
            std::cout << "converge ... " << std::endl;
            std::cout << std::setw(12) << std::setprecision(10) << " current =" << current << ";\n";
            std::cout << std::setw(12) << std::setprecision(10) << " old     = " << old << std::endl;
            std::cout << std::setw(12) << std::setprecision(10) << " diff    =" << (current - old) << std::endl;
            break;
        }

    }
    //std::string filename = "output.rst7";
    //coord_writter(filename, frameX);
    return true;
}

// Parse a string like "1-4,7-10,34-59" into a vector<int>
std::vector<int> find_range(const std::string &list) {
    std::vector<int> int_list;
    std::stringstream ss(list);
    std::string token;

    while (std::getline(ss, token, ',')) {
        if (token.empty()) continue;
        size_t dash_pos = token.find('-');
        if (dash_pos == std::string::npos) {
            // single integer
            int val = std::atoi(token.c_str());
            int_list.push_back(val);
        } else {
            std::string left  = token.substr(0, dash_pos);
            std::string right = token.substr(dash_pos + 1);
            int start = std::atoi(left.c_str());
            int stop  = std::atoi(right.c_str());
            for (int v = start; v <= stop; v++) {
                int_list.push_back(v);
            }
        }
    }

    return int_list;
}

int main(int argc, char *argv[]) {
    if (argc != 8) {
        std::cout << "Input:\n";
        std::cout << "amber prmtop filename\n";
        std::cout << "amber mdcrd filename\n";
        std::cout << "residues list to minimize (all other residue atoms are fixed).\n";
        std::cout << "residues list examples: 1-4,7-10,34-59\n";
        std::cout << "output filename\n";
        std::cout << "method: 1 is for standard energy function, 2 is for the squishy non-bonded energy function, 3 just vdw repulsive + bonded, 4 just bonded\n";
        std::cout << "Jiggle=yes or Jiggle=no\n";
        std::cout << "OneByOneFirst or Allonly  \n";
        return 0;
    }

    std::string parmfile      = argv[1];
    std::string crdfile       = argv[2];
    std::string list1         = argv[3];
    std::string output        = argv[4];
    std::string methodstr     = argv[5];
    std::string Jiggle        = argv[6];
    std::string onebyone      = argv[7];

    //int method = 1;
    //int method = 2;
    int method = std::atoi(methodstr.c_str());
    std::cout << "method = " << method << std::endl; 

    if (methodstr == "1") {
        //oflag = true;
        std::cout << "standard energy function method \n" << std::endl;
    } else if (methodstr == "2") {
        //oflag = false;
        std::cout << "squishy energy function method \n" << std::endl;
    } else if (methodstr == "3") {
        //oflag = false;
        std::cout << "squishy energy function method, just vdw repultion + bonded\n" << std::endl;
    } else if (methodstr == "4") {
        //oflag = false;
        std::cout << " Just bonded energies\n" << std::endl;
    } else {
        std::cout << "method must be 1, 2, 3, or 4\n";
        return 1;
    }

    bool jiggleb = false;
    if (Jiggle == "Jiggle=yes") {
        jiggleb = true;
    } else if (Jiggle == "Jiggle=no") {
        jiggleb = false;
    } else{
        std::cout << "Error: input error: "<< Jiggle << " is not a valid option." << " Options are Jiggle=yes or Jiggle=no" << std::endl;
        exit(0);
    }

    bool onebyoneb = false;
    if (onebyone == "OneByOneFirst") {
        onebyoneb = true;
    } else if (onebyone == "Allonly") {
        onebyoneb = false;
    } else{
        std::cout << "Error: input error: "<< onebyone << " is not a valid option." << " Options are OneByOneFirst or Allonly" << std::endl;
        exit(0);
    }

    std::vector<int> int_list1 = find_range(list1);
    //std::vector<int> int_list2 = find_range(list2);

    Parm parm_stuff = parm_reader(parmfile);
    //exit(0);

    int numatoms = (int)parm_stuff.AMBER_ATOM_TYPE.size();
    std::vector <int> atomlist;
    //for (size_t i = 0; i < parm_stuff.CHARGE.size(); i++){
    // RESIDUE_POINTER
    //for (size_t i = 0; i < parm_stuff.RESIDUE_POINTER.size(); i++){
    for (size_t r = 0; r < int_list1.size(); r++){
         //int i = int_list1[r]-1;
         int i = r;
         int rstop;
         if (i == parm_stuff.RESIDUE_POINTER.size()-1){
               rstop = parm_stuff.CHARGE.size()+1; // all remaining atoms 
         } else {
               rstop =  parm_stuff.RESIDUE_POINTER[int_list1[i]]-1;
         }
         std::cout << "residue i = " <<  int_list1[i] << ": atom start = " << parm_stuff.RESIDUE_POINTER[int_list1[i]-1] << " --- atom stop = " ;
         //std::cout << (parm_stuff.RESIDUE_POINTER[int_list1[i]]-1) << std::endl;
         std::cout << rstop << std::endl;
         //for (size_t ii = parm_stuff.RESIDUE_POINTER[int_list1[i]-1]; ii < (parm_stuff.RESIDUE_POINTER[int_list1[i]]); ii++){
         for (size_t ii = parm_stuff.RESIDUE_POINTER[int_list1[i]-1]; ii < rstop; ii++){
             std::cout << ii << " " ;
             atomlist.push_back(ii-1);
         }
         std::cout << std::endl;
    }

    // Matrices for avg, avg^2, variance
    //size_t n1 = int_list1.size();
    //size_t n2 = int_list2.size();

    //std::vector<std::vector<double>> avg_mat_int(n1, std::vector<double>(n2, 0.0));
    //std::vector<std::vector<double>> avg_mat_vdw(n1, std::vector<double>(n2, 0.0));
    //std::vector<std::vector<double>> avg_mat_ele(n1, std::vector<double>(n2, 0.0));

    //std::vector<std::vector<double>> avg2_mat_int(n1, std::vector<double>(n2, 0.0));
    //std::vector<std::vector<double>> avg2_mat_vdw(n1, std::vector<double>(n2, 0.0));
    //std::vector<std::vector<double>> avg2_mat_ele(n1, std::vector<double>(n2, 0.0));

    //std::vector<std::vector<double>> var_mat_int(n1, std::vector<double>(n2, 0.0));
    //std::vector<std::vector<double>> var_mat_vdw(n1, std::vector<double>(n2, 0.0));
    //std::vector<std::vector<double>> var_mat_ele(n1, std::vector<double>(n2, 0.0));

    std::ifstream fh(crdfile.c_str());
    if (!fh) {
        std::cerr << "Error opening coordinate file: " << crdfile << "\n";
        return 1;
    }

    //std::ofstream vdwfileh_frames;
    //std::ofstream elefileh_frames;
    //std::ofstream intfileh_frames;
    //if (oflag) {
    //    vdwfileh_frames.open(("vdw" + output + ".frames").c_str());
    //    elefileh_frames.open(("ele" + output + ".frames").c_str());
    //    intfileh_frames.open(("tot" + output + ".frames").c_str());
    //    if (!vdwfileh_frames || !elefileh_frames || !intfileh_frames) {
    //        std::cerr << "Error opening timestep output files.\n";
    //        return 1;
    //    }
    //}

    int i = 0;
    int linecount = 0;
    std::vector<std::string> remainder_data;

    while (true) {
        Frame frameX;
        bool more = coord_reader(linecount, fh, frameX, crdfile, numatoms, remainder_data);
        if (!more) break;

        std::cout << "remainder: " << remainder_data.size() << "\n";

        EnergyBonded eb; 
        eb = bonded_Energy(parm_stuff, frameX); 
        //std:: cout << "I AM HERE" << std::endl;

        // calculate pair list 
        // exclude bonded pairs 1-2,1-3,1-4
        // generate a second list of 1-4
        //
        // make a matrix.
        //
        // then loop over bonds -> 1-2
        // then loop over angles -> 1-3
        // then loop over diheds -> 1-4
        //
        // generate a distance based pair list
        // update periodically.  this is when we are runing min and mc. 

        //EnergyTriple e = intermolecular_Energy(parm_stuff, frameX, method);
         
        std::vector <pair> pairlist;
        std::vector <pair> pairlist14;

        //bool flag = 
        generate_pairlist(parm_stuff, frameX, pairlist, pairlist14);
        EnergyTriple e = intermolecular_Energy_pairlist(parm_stuff, frameX, pairlist, pairlist14,-1, method);  // -1 indicates that all pairs will be included in the calculation.

        //std:: cout << "I AM HERE" << std::endl;
        std:: cout << "e.Evdw + e.Ees + eb.Ebond + eb.Eangle + eb.Edihed" << std::endl;
        std:: cout << e.Evdw << "+" << e.Ees <<"+" << eb.Ebond <<"+" << eb.Eangle <<"+" << eb.Edihed << std::endl;

        // minimize atom one frist
        // then atoms one and two, then one, two, and three ... and so on. 

        std::vector <int> tempatomlist;
        if (jiggleb) {
           jiggle_atoms(frameX,atomlist,0.1);
        }
        if (onebyoneb) {
          for (size_t i = 0; i < atomlist.size();i++){
             //jiggle_atoms(frameX,atomlist,0.1);
             std::cout << "minimize atom i = " << i << std::endl;
             int atom = atomlist[i];
             tempatomlist.push_back(atom);
             Energy_min_pairlist(parm_stuff, frameX, pairlist, pairlist14, tempatomlist, method, 100000);
             //exit(0);
          }
        }
        //exit(0);

        if (jiggleb) {
           jiggle_atoms(frameX,atomlist,0.1);
        }

        Energy_min_pairlist(parm_stuff, frameX, pairlist, pairlist14, atomlist, method, 100000);
        std::string filename = "output.rst7";
        coord_writter(filename, frameX);

        exit(0);
    } 

    return 0;
}

