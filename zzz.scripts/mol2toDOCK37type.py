import sys, mol2

## Writen by Trent Balius in the Shoichet Group, 2014
## converts a mol2 to spheres. 

def upper_to_lower(string):
    string_new=''

    for c in string: 
        if c == 'A':
           string_new=string_new+'a'
        if c == 'B':
           string_new=string_new+'b'
        if c == 'C':
           string_new=string_new+'c'
        if c == 'D':
           string_new=string_new+'d'
        if c == 'E':
           string_new=string_new+'e'
        if c == 'F':
           string_new=string_new+'f'
        if c == 'G':
           string_new=string_new+'g'
        if c == 'H':
           string_new=string_new+'h'
        if c == 'I':
           string_new=string_new+'i'
        if c == 'J':
           string_new=string_new+'j'
        if c == 'K':
           string_new=string_new+'k'
        if c == 'L':
           string_new=string_new+'l'
        if c == 'M':
           string_new=string_new+'m'
        if c == 'N':
           string_new=string_new+'n'
        if c == 'O':
           string_new=string_new+'o'
        if c == 'P':
           string_new=string_new+'p'
        if c == 'Q':
           string_new=string_new+'q'
        if c == 'R':
           string_new=string_new+'r'
        if c == 'S':
           string_new=string_new+'s'
        if c == 'T':
           string_new=string_new+'t'
        if c == 'U':
           string_new=string_new+'u'
        if c == 'V':
           string_new=string_new+'v'
        if c == 'W':
           string_new=string_new+'w'
        if c == 'X':
           string_new=string_new+'x'
        if c == 'Y':
           string_new=string_new+'y'
        if c == 'Z':
           string_new=string_new+'z'
    return string_new

def pad_string(string):
    string_new = ''
    if len(string) == 1: 
       string_new = string + '  '
    elif len(string) == 2: 
       string_new = string + ' '
    elif len(string) == 3 or len(string) == 4: # do nothing
       string_new = string
    elif len(string) > 4: 
       print("Warning len(string) > 4")
       string_new = string
    return string_new

def main():
  if len(sys.argv) != 3: # if no input
     print "ERORR"
     return
  namemol2 = sys.argv[1]
  namedocktype = sys.argv[2]
  fh = open(namedocktype,'w')
  fh1 = open(namedocktype+'.amb.crg.oxt','w')
  fh2 = open(namedocktype+'.prot.table.ambcrg.ambH','w')
  mol  = mol2.read_Mol2_file(namemol2)[0]
  dt   = mol2.convert_sybyl_to_dock(mol)
  for i in range(len(mol.atom_list)):
      print i+1, mol.atom_list[i].type, dt[i]
      fh.write('%2d %4s %4s %4s %-6s %2s\n' % (i+1, mol.atom_list[i].name, mol.atom_list[i].resname, upper_to_lower(mol.atom_list[i].resname), mol.atom_list[i].type, dt[i]))
      fh1.write('%-4s %4s       %6.3f\n' % (mol.atom_list[i].name, upper_to_lower(mol.atom_list[i].resname),  mol.atom_list[i].Q))
      fh2.write('%4s  %4s       %6.3f %2s\n' % (  pad_string(mol.atom_list[i].name), mol.atom_list[i].resname, mol.atom_list[i].Q, dt[i]))

  fh.close()
  fh1.close()
  fh2.close()
main()


