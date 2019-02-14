import sys,  gzip

## Writen by Trent Balius in Shoichet Lab modified frem a script from while Trent was in the Rizzo Group 
## converts a eel to pdb. 


def lookUpEle(num_str):
#   1        888.79        24.81    sp2 and sp C
#   2       1586.37        35.05    CH3 (united atom)
#   3       1128.12        27.96    CH2 (united atom)
#   4        769.72        21.49    CH (united atom)
#   5        533.20        16.16    sp3 C
#   6          0.00         0.00    H on polar atom
#   7         85.37         4.13    H on C
#   8        735.31        24.25    sp2 and sp N
#   9        725.70        20.26    quaternary sp3 N
#  10        888.79        24.81    sp3 N
#  11        480.19        20.72    sp2 O
#  12        500.18        19.68    sp3 O
#  13       2454.77        46.86    P
#  14       1831.79        40.48    S
#  15        251.02        11.92    F
#  16       2194.13        46.37    Cl
#  17       3885.92        66.31    Br
#  18       6817.37        92.86    I
#  19        235.24        10.15    Na+ (unhydrated), K+
#  20         51.92         5.73    Mg++, Li+, Al+++, M++ (except Ca++)
#  21        339.55        14.65    Ca++
#  22       1971.47        37.63    Cl- (unhydrated)
#  23        762.07        24.38    Lennard-Jones water particle
#  24       3885.92        66.31    Si (same numbers as Br)
#  25          0.00         0.00    Du/LP (same numbers as H on polar atom)
   num_str = num_str.strip(' ')
   ele = ''
   if (num_str == '1') or (num_str == '2') or (num_str == '3') or (num_str == '4') or (num_str == '5'):
        ele = 'C '
   elif (num_str == '6') or (num_str == '7'):
        ele = 'H '
   elif (num_str == '8') or (num_str == '9') or (num_str == '10'):
        ele = 'N '
   elif (num_str == '11') or (num_str == '12'):
        ele = 'O '
   elif (num_str == '13'):
        ele = 'P '
   elif (num_str == '14'):
        ele = 'S '
   elif (num_str == '15'):
        ele = 'F '
   elif (num_str == '16'):
        ele = 'Cl'
   elif (num_str == '17'):
        ele = 'Br'
   elif (num_str == '18'):
        ele = 'I '
   elif (num_str == '19'):
        ele = 'Na'
   elif (num_str == '20'):
        ele = 'Mg'
   elif (num_str == '21'):
        ele = 'Ca'
   elif (num_str == '22'):
        ele = 'Cl'
   elif (num_str == '23'):
        ele = 'O ' # Lennard-Jones water particle
   elif (num_str == '25'):
        ele = 'Si'
   elif (num_str == '26'):
        ele = 'Du'
   return ele


def convert(eel_file,pdb_file):

    file1 = gzip.open(eel_file,'r')
    lines = file1.readlines()
    file1.close()
  
    file2 = open(pdb_file,'w')

#ATOM     26  N   ASN A 676      47.124   0.267  65.767  1.00 44.01           N
#ATOM     27  CA  ASN A 676      45.735  -0.094  65.484  1.00 40.28           C
#ATOM     28  C   ASN A 676      45.670  -1.611  65.311  1.00 48.80           C
#ATOM     29  O   ASN A 676      45.949  -2.152  64.242  1.00 55.33           O
#ATOM     30  CB  ASN A 676      45.253   0.656  64.234  1.00 20.42           C

    for line in lines:
         linesplit = line.split() #split on white space  
         if linesplit[0] == "REMARK":
             file2.write(line)
         elif linesplit[0] == "ATOM":
             ele = lookUpEle(line[71:73])
             #print line[71:73] +" " + ele
             file2.write(line[0:54]+'  1.00  0.00           '+ ele +'\n')
         elif linesplit[0] == "TER":
             file2.write('END\n')
         #elif linesplit[0] == "END":
         #    file2.write('END\n')
    file2.close()
    return

def main():
  if len(sys.argv) != 3: # if no input
     print "ERORR"
     return
  name_eel = sys.argv[1]
  name_pdb = sys.argv[2]
  convert(name_eel,name_pdb)
main()


