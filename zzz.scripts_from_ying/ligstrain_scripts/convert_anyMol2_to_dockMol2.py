from __future__ import print_function
import os,sys

def anyMol2_to_dockMol2(infile, name):

    out_lines = []
    fi = open(infile, "r")
    in_lines = fi.readlines()
    fi.close()

    for i in range(len(in_lines)):
        oneline = in_lines[i]
        if oneline.startswith("@<TRIPOS>MOLECULE"):
            natom = int( in_lines[i+2].split()[0] )
            nbond = int( in_lines[i+2].split()[1] )
            out_lines.append(oneline)
            out_lines.append('%17s      none\n' % name)
            out_lines.append(in_lines[i+2])
            out_lines.append('\n\n\n')
        elif oneline.startswith("@<TRIPOS>ATOM"):
            out_lines.append(oneline)
            for j in range(1, natom+1):
                ele = in_lines[i+j].split()
                line = " %6d %-4s    %10.4f %10.4f %10.4f %-5s %6d  %4s  %7.4f\n" \
                % (int(ele[0]), ele[1], float(ele[2]), float(ele[3]), float(ele[4]), \
                    ele[5], int(ele[6]), ele[7]+'1', float(ele[8]))
                out_lines.append(line)
        elif oneline.startswith("@<TRIPOS>BOND"):
            out_lines.append(oneline)
            for k in range(1, nbond+1):
                ele = in_lines[i+k].split()
                line = "%6d%5d%5d %2s\n" % (int(ele[0]),int(ele[1]),int(ele[2]),ele[3])
                out_lines.append(line)

    return out_lines

in_mol2  = sys.argv[1]
out_mol2 = sys.argv[2]
zincID   = sys.argv[3]

out_lines = anyMol2_to_dockMol2(in_mol2, zincID)

with open(out_mol2, "w") as fo:
    fo.write("##########\n")
    for line in out_lines:
        fo.write(line)



