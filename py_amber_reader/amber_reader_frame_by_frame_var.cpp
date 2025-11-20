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
 * Conversion notes:
 *   - This file is a direct, line-by-line style translation of the original
 *     Python script into C++ with minimal algorithmic changes, intended to
 *     reproduce the same behavior and output formats.
 *
 *   - Data structures:
 *       * Python classes `parm`, `cord`, and `frame` were converted to
 *         C++ structs `Parm`, `Cord`, and `Frame`.
 *       * Python lists are represented by `std::vector<...>` containers.
 *       * AMBER arrays (e.g., Lennard-Jones A/B coefficients) that were
 *         treated as flat lists in Python are stored as:
 *           - `std::vector<double> LENNARD_JONES_ACOEF`
 *           - `std::vector<double> LENNARD_JONES_BCOEF`
 *         and then mapped into 2D matrices `M_LJA` and `M_LJB` using the
 *         same indexing logic as the Python code.
 *
 *   - Indexing and AMBER conventions:
 *       * The Python code uses 1-based indices for atoms and residues
 *         (consistent with AMBER prmtop and mdcrd conventions), while C++
 *         uses 0-based indexing. Care was taken to preserve the original
 *         1-based logic when accessing atoms/residues:
 *           - Atom i in AMBER (1-based) → index (i - 1) in C++ vectors.
 *           - Residue pointer arrays (`RESIDUE_POINTER`) are used with the
 *             same semantics as the Python version.
 *       * `NONBONDED_PARM_INDEX` is stored as `index - 1`, exactly as done
 *         in the Python script, to align with how Amber flattens the
 *         NTYPES×NTYPES matrix into a 1D array.
 *
 *   - File I/O:
 *       * The `parm_reader` function parses the AMBER prmtop file in the
 *         same way as the Python `parm_reader` function, including:
 *           - FLAG-based sections (e.g., %FLAG ATOM_NAME, %FLAG CHARGE).
 *           - Fixed-width field extraction for integer and real data.
 *       * The `coord_reader` function reads the AMBER mdcrd or restart file
 *         frame-by-frame, handling:
 *           - Optional restart header line(s) containing “Restart” or
 *             “default_name”.
 *           - Partial coordinate lines via a `remainder` buffer so that an
 *             integer number of xyz triples is assembled before forming a
 *             `Frame`.
 *       * Output files:
 *           - When `outputflag` is "timestep", the program writes per-frame
 *             interaction energy matrices:
 *               vdw<output>.frames
 *               ele<output>.frames
 *               tot<output>.frames
 *           - In all cases, average and variance matrices across frames are
 *             written to:
 *               vdw<output>.avg / .var
 *               ele<output>.avg / .var
 *               tot<output>.avg / .var
 *             using the same CSV-like format as the Python code.
 *
 *   - Energy calculations:
 *       * The core energy functions
 *           - distance()
 *           - vdw_energy_function(A, B, r)
 *           - es_energy_function(q1, q2, r)
 *           - energy_function(A, B, q1, q2, r)
 *         are direct numeric translations of the Python versions.
 *       * `intermolecular_Energy` loops over atom indices in residue ranges
 *         `[start1, stop1)` and `[start2, stop2)` taken from the prmtop and
 *         computes:
 *           - total Eint  (vdW + electrostatics)
 *           - Evdw        (Lennard-Jones only)
 *           - Ees         (Coulomb term only)
 *
 *   - Command line interface:
 *       * The C++ `main` preserves the Python `main()` calling convention:
 *
 *           argv[1] = prmtop filename
 *           argv[2] = mdcrd filename
 *           argv[3] = residues list1 for species 1
 *           argv[4] = residues list2 for species 2
 *           argv[5] = output filename prefix
 *           argv[6] = outputflag ("timestep" or "justavg")
 *
 *         Residue lists are parsed by `find_range`, which accepts input
 *         like "1-4,7-10,34-59" and expands to a list of integers.
 *
 *   - Numerical behavior and limitations:
 *       * Double precision (`double`) is used for all real-valued quantities
 *         corresponding to Python `float`.
 *       * No attempt was made to change units, cutoffs, or physical models;
 *         the code assumes the same units and conventions as the original
 *         Python script and the AMBER files.
 *       * Some diagnostic `std::cout` messages from the Python version
 *         (e.g., size checks, warnings) have been kept for debugging and
 *         tracing.
 *
 *   - Portability / compilation:
 *       * Designed to compile with GCC using standard C++ (no compiler-
 *         specific extensions required).
 *       * Typical compile command:
 *
 *             g++ amber_reader_frame_by_frame_var.cpp -O2 -Wall -Wextra -o amber_reader
 *
 *       * The code avoids C++20+ features and should compile on GCC versions
 *         with support roughly comparable to C++14/C++17.
 *
 *   Any scientific interpretation, validation, or further optimization
 *   remains the responsibility of the user. This translation’s goal is to
 *   reproduce the algorithmic behavior of the original Python script in a
 *   statically compiled C++ form.
 */


#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>
#include <cstdlib>
#include <algorithm>

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
    for (size_t i = 0; i < M.size(); ++i) {
        for (size_t j = 0; j < M[i].size(); ++j) {
            std::printf("%10.1f", M[i][j]);
        }
        std::printf("\n");
    }
}

// Debug-print matrix of ints (not used by main, kept for parity)
static void print_matrix_d(const std::vector<std::vector<int>> &M) {
    for (size_t i = 0; i < M.size(); ++i) {
        for (size_t j = 0; j < M[i].size(); ++j) {
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
    std::vector<double> LENNARD_JONES_ACOEF;
    std::vector<double> LENNARD_JONES_BCOEF;
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
            if (split_line[0] == "%FLAG" && split_line[1] == "DIHEDRALS_FORCE_CONSTANT")
                F_DIHEDRAL_FORCE_CONSTANT = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "DIHEDRAL_PERIODICITY")
                F_DIHEDRAL_PERIODICITY = true;
            if (split_line[0] == "%FLAG" && split_line[1] == "DIHEDRAL_PHASE")
                F_DIHEDRAL_PHASE = true;
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

    // Build RESIDUE_ARRAY mapping atoms to residues
    std::vector<std::string> RESIDUE_ARRAY(ATOM_NAME.size(), "");

    for (size_t i = 0; i + 1 < RESIDUE_POINTER.size(); ++i) {
        int start = RESIDUE_POINTER[i];
        int stop  = RESIDUE_POINTER[i + 1];
        for (int j = start; j < stop; ++j) {
            // j-1 for 0-based index
            if (j - 1 >= 0 && j - 1 < (int)RESIDUE_ARRAY.size()) {
                RESIDUE_ARRAY[j - 1] = RESIDUE_LABEL[i];
            }
        }
    }
    // last residue
    if (!RESIDUE_POINTER.empty() && !RESIDUE_LABEL.empty()) {
        int last_start = RESIDUE_POINTER.back() - 1;
        for (int j = last_start; j < (int)ATOM_NAME.size(); ++j) {
            RESIDUE_ARRAY[j] = RESIDUE_LABEL.back();
        }
    }

    std::cout << "ATOM_NAME = " << ATOM_NAME.size() << "\n";
    std::cout << "CHARGE = " << CHARGE.size() << "\n";
    std::cout << "ATOM_TYPE_INDEX = " << ATOM_TYPE_INDEX.size() << "\n";

    int max_atom_type_index = 0;
    if (!ATOM_TYPE_INDEX.empty()) {
        max_atom_type_index = *std::max_element(ATOM_TYPE_INDEX.begin(), ATOM_TYPE_INDEX.end());
    }

    std::cout << "max(ATOM_TYPE_INDEX) = " << max_atom_type_index << "\n";
    std::cout << "max(ATOM_TYPE_INDEX)^2 = " << max_atom_type_index * max_atom_type_index << "\n";
    std::cout << "NONBONDED_PARM_INDEX = " << NONBONDED_PARM_INDEX.size() << "\n";

    int max_nonbonded = 0;
    if (!NONBONDED_PARM_INDEX.empty()) {
        max_nonbonded = *std::max_element(NONBONDED_PARM_INDEX.begin(), NONBONDED_PARM_INDEX.end());
    }
    std::cout << "max(NONBONDED_PARM_INDEX) = " << max_nonbonded << "\n";
    std::cout << "LENNARD_JONES_ACOEF = " << LENNARD_JONES_ACOEF.size() << "\n";
    std::cout << "LENNARD_JONES_BCOEF = " << LENNARD_JONES_BCOEF.size() << "\n";

    // build atom_type_uniq (for debug printing if desired)
    std::vector<std::string> atom_type_uniq;
    for (int AtomNum = 1; AtomNum <= max_atom_type_index; ++AtomNum) {
        int count = 0;
        for (size_t i = 0; i < ATOM_TYPE_INDEX.size(); ++i) {
            if (AtomNum == ATOM_TYPE_INDEX[i]) {
                if (count == 0) {
                    atom_type_uniq.push_back(AMBER_ATOM_TYPE[i]);
                }
                ++count;
            }
        }
        std::cout << "ATOM_TYPE_INDEX == " << AtomNum
                  << " has N = " << count << " atoms of this type\n";
    }

    std::cout << "\n\n LJ matrixes\n";

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

    for (int i = 0; i < NTYPES; ++i) {
        for (int j = 0; j < NTYPES; ++j) {
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
                line.find("default_name") != std::string::npos) {
                std::cout << "file " << filename << " is a restart file.\n";
                // Do NOT increment line_count, skip to next line
                continue;
            }
        }

        if (line_count > 0) {
            for (size_t i = 0; i < data.size(); ++i) {
                if (ii > 3 * size - 1) {
                    // store remainder
                    for (size_t j = i; j < data.size(); ++j) {
                        remainder.push_back(data[j]);
                    }
                    flag_break = true;
                    break;
                }
                vals.push_back(data[i]);
                ++ii;
            }
            if (flag_break) {
                break;
            }
        }
        ++line_count;
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

// Distance between two coordinate points
double distance(const Cord &c1, const Cord &c2) {
    double dx = c1.x - c2.x;
    double dy = c1.y - c2.y;
    double dz = c1.z - c2.z;
    return std::sqrt(dx*dx + dy*dy + dz*dz);
}

double vdw_energy_function(double A, double B, double r) {
    return A / std::pow(r, 12.0) - B / std::pow(r, 6.0);
}

double es_energy_function(double q1, double q2, double r) {
    return q1 * q2 / r;
}

double energy_function(double A, double B, double q1, double q2, double r) {
    return A / std::pow(r, 12.0) - B / std::pow(r, 6.0) + q1 * q2 / r;
}

struct EnergyTriple {
    double Eint;
    double Evdw;
    double Ees;
};

EnergyTriple intermolecular_Energy(
    const Parm &parm_stuff,
    const Frame &frameX,
    int start1,
    int stop1,
    int start2,
    int stop2
) {
    double Eint = 0.0;
    double Evdw = 0.0;
    double Ees  = 0.0;

    if (stop1 > (int)parm_stuff.CHARGE.size() + 1) {
        std::cout << "WARNING. stop1 > (len(parm_stuff.CHARGE)+1)\n";
    }
    if (stop2 > (int)parm_stuff.CHARGE.size() + 1) {
        std::cout << "WARNING. stop2 > (len(parm_stuff.CHARGE)+1)\n";
    }

    for (int i = start1; i < stop1; ++i) {
        for (int j = start2; j < stop2; ++j) {
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

            double e = energy_function(A, B, q1, q2, r);
            Eint += e;
            Evdw += vdw_energy_function(A, B, r);
            Ees  += es_energy_function(q1, q2, r);
        }
    }

    EnergyTriple out { Eint, Evdw, Ees };
    return out;
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
            for (int v = start; v <= stop; ++v) {
                int_list.push_back(v);
            }
        }
    }

    return int_list;
}

int main(int argc, char *argv[]) {
    if (argc != 7) {
        std::cout << "Input:\n";
        std::cout << "amber prmtop filename\n";
        std::cout << "amber mdcrd filename\n";
        std::cout << "residues list1 for species 1 :  Loop over these residues, continuity not nessicery\n";
        std::cout << "residues list examples: 1-4,7-10,34-59\n";
        std::cout << "residues list2 for species 2 ( if species 2 is more than one residue generates a matrix)\n";
        std::cout << "output filename\n";
        std::cout << "outputflag: timestep (output matrix for every time step in addition to averge) or justavg\n";
        return 0;
    }

    std::string parmfile      = argv[1];
    std::string crdfile       = argv[2];
    std::string list1         = argv[3];
    std::string list2         = argv[4];
    std::string output        = argv[5];
    std::string outputflagstr = argv[6];

    bool oflag = false;
    if (outputflagstr == "timestep") {
        oflag = true;
    } else if (outputflagstr == "justavg") {
        oflag = false;
    } else {
        std::cout << "output_flag must be either timestep or justavg\n";
        return 1;
    }

    std::vector<int> int_list1 = find_range(list1);
    std::vector<int> int_list2 = find_range(list2);

    Parm parm_stuff = parm_reader(parmfile);

    int numatoms = (int)parm_stuff.AMBER_ATOM_TYPE.size();

    // Matrices for avg, avg^2, variance
    size_t n1 = int_list1.size();
    size_t n2 = int_list2.size();

    std::vector<std::vector<double>> avg_mat_int(n1, std::vector<double>(n2, 0.0));
    std::vector<std::vector<double>> avg_mat_vdw(n1, std::vector<double>(n2, 0.0));
    std::vector<std::vector<double>> avg_mat_ele(n1, std::vector<double>(n2, 0.0));

    std::vector<std::vector<double>> avg2_mat_int(n1, std::vector<double>(n2, 0.0));
    std::vector<std::vector<double>> avg2_mat_vdw(n1, std::vector<double>(n2, 0.0));
    std::vector<std::vector<double>> avg2_mat_ele(n1, std::vector<double>(n2, 0.0));

    std::vector<std::vector<double>> var_mat_int(n1, std::vector<double>(n2, 0.0));
    std::vector<std::vector<double>> var_mat_vdw(n1, std::vector<double>(n2, 0.0));
    std::vector<std::vector<double>> var_mat_ele(n1, std::vector<double>(n2, 0.0));

    std::ifstream fh(crdfile.c_str());
    if (!fh) {
        std::cerr << "Error opening coordinate file: " << crdfile << "\n";
        return 1;
    }

    std::ofstream vdwfileh_frames;
    std::ofstream elefileh_frames;
    std::ofstream intfileh_frames;
    if (oflag) {
        vdwfileh_frames.open(("vdw" + output + ".frames").c_str());
        elefileh_frames.open(("ele" + output + ".frames").c_str());
        intfileh_frames.open(("tot" + output + ".frames").c_str());
        if (!vdwfileh_frames || !elefileh_frames || !intfileh_frames) {
            std::cerr << "Error opening timestep output files.\n";
            return 1;
        }
    }

    int i = 0;
    int linecount = 0;
    std::vector<std::string> remainder_data;

    while (true) {
        Frame frameX;
        bool more = coord_reader(linecount, fh, frameX, crdfile, numatoms, remainder_data);
        if (!more) break;

        std::cout << "remainder: " << remainder_data.size() << "\n";

        if (oflag) {
            vdwfileh_frames << "Frame" << i << "\n";
            elefileh_frames << "Frame" << i << "\n";
            intfileh_frames << "Frame" << i << "\n";
        }

        size_t j_idx = 0;
        for (size_t j = 0; j < n1; ++j) {
            int resid1 = int_list1[j];
            int start1, stop1;
            if (resid1 == (int)parm_stuff.RESIDUE_POINTER.size()) {
                start1 = parm_stuff.RESIDUE_POINTER[resid1 - 1];
                stop1 = (int)parm_stuff.ATOM_NAME.size() + 1;
            } else if (resid1 > (int)parm_stuff.RESIDUE_POINTER.size()) {
                std::cerr << "Error: resid1 out of range.\n";
                return 1;
            } else {
                start1 = parm_stuff.RESIDUE_POINTER[resid1 - 1];
                stop1  = parm_stuff.RESIDUE_POINTER[resid1];
            }

            size_t k_idx = 0;
            for (size_t k = 0; k < n2; ++k) {
                int resid2 = int_list2[k];
                int start2, stop2;
                if (resid2 == (int)parm_stuff.RESIDUE_POINTER.size()) {
                    start2 = parm_stuff.RESIDUE_POINTER[resid2 - 1];
                    stop2 = (int)parm_stuff.ATOM_NAME.size() + 1;
                } else if (resid2 > (int)parm_stuff.RESIDUE_POINTER.size()) {
                    std::cerr << "Error: resid2 out of range.\n";
                    return 1;
                } else {
                    start2 = parm_stuff.RESIDUE_POINTER[resid2 - 1];
                    stop2  = parm_stuff.RESIDUE_POINTER[resid2];
                }

                EnergyTriple e = intermolecular_Energy(parm_stuff, frameX, start1, stop1, start2, stop2);

                avg_mat_int[j][k] += e.Eint;
                avg_mat_vdw[j][k] += e.Evdw;
                avg_mat_ele[j][k] += e.Ees;

                avg2_mat_int[j][k] += e.Eint * e.Eint;
                avg2_mat_vdw[j][k] += e.Evdw * e.Evdw;
                avg2_mat_ele[j][k] += e.Ees  * e.Ees;

                if (oflag) {
                    if (k < n2 - 1) {
                        intfileh_frames << e.Eint << ",";
                        vdwfileh_frames << e.Evdw << ",";
                        elefileh_frames << e.Ees  << ",";
                    } else {
                        intfileh_frames << e.Eint;
                        vdwfileh_frames << e.Evdw;
                        elefileh_frames << e.Ees;
                    }
                }

                ++k_idx;
            }
            if (oflag) {
                intfileh_frames << "\n";
                vdwfileh_frames << "\n";
                elefileh_frames << "\n";
            }
            ++j_idx;
        }
        ++i;
        if (!more) break;
    }
    fh.close();
    if (oflag) {
        intfileh_frames.close();
        vdwfileh_frames.close();
        elefileh_frames.close();
    }

    int num_frames = i;

    // Write average and variance matrices
    std::ofstream vdwfileh(("vdw" + output + ".avg").c_str());
    std::ofstream elefileh(("ele" + output + ".avg").c_str());
    std::ofstream intfileh(("tot" + output + ".avg").c_str());

    std::ofstream varvdwfileh(("vdw" + output + ".var").c_str());
    std::ofstream varelefileh(("ele" + output + ".var").c_str());
    std::ofstream varintfileh(("tot" + output + ".var").c_str());

    if (!vdwfileh || !elefileh || !intfileh ||
        !varvdwfileh || !varelefileh || !varintfileh) {
        std::cerr << "Error opening avg/var output files.\n";
        return 1;
    }

    vdwfileh << "AVG fp\n";
    elefileh << "AVG fp\n";
    intfileh << "AVG fp\n";
    varvdwfileh << "VAR fp\n";
    varelefileh << "VAR fp\n";
    varintfileh << "VAR fp\n";

    for (size_t j = 0; j < n1; ++j) {
        for (size_t k = 0; k < n2; ++k) {
            avg_mat_int[j][k] /= num_frames;
            avg_mat_vdw[j][k] /= num_frames;
            avg_mat_ele[j][k] /= num_frames;

            avg2_mat_int[j][k] /= num_frames;
            avg2_mat_vdw[j][k] /= num_frames;
            avg2_mat_ele[j][k] /= num_frames;

            var_mat_int[j][k] = avg2_mat_int[j][k] - avg_mat_int[j][k] * avg_mat_int[j][k];
            // Note: original Python code seems to use avg_mat_int for all 3 variances; mirrored here
            var_mat_vdw[j][k] = avg2_mat_vdw[j][k] - avg_mat_int[j][k] * avg_mat_int[j][k];
            var_mat_ele[j][k] = avg2_mat_ele[j][k] - avg_mat_int[j][k] * avg_mat_int[j][k];

            if (k < n2 - 1) {
                vdwfileh     << avg_mat_vdw[j][k] << ",";
                elefileh     << avg_mat_ele[j][k] << ",";
                intfileh     << avg_mat_int[j][k] << ",";
                varvdwfileh  << var_mat_vdw[j][k] << ",";
                varelefileh  << var_mat_ele[j][k] << ",";
                varintfileh  << var_mat_int[j][k] << ",";
            } else {
                vdwfileh     << avg_mat_vdw[j][k];
                elefileh     << avg_mat_ele[j][k];
                intfileh     << avg_mat_int[j][k];
                varvdwfileh  << var_mat_vdw[j][k];
                varelefileh  << var_mat_ele[j][k];
                varintfileh  << var_mat_int[j][k];
            }
        }
        vdwfileh    << "\n";
        elefileh    << "\n";
        intfileh    << "\n";
        varvdwfileh << "\n";
        varelefileh << "\n";
        varintfileh << "\n";
    }

    vdwfileh.close();
    elefileh.close();
    intfileh.close();
    varvdwfileh.close();
    varelefileh.close();
    varintfileh.close();

    return 0;
}

