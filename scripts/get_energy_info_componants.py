
import os
import sys
import math

#systdir = "2RGP_GIST_0p5/ROC_ligdecoy/"
#systdir = "2RGP_GIST/ROC_ligdecoy/"
systdir = sys.argv[1]
sysname = sys.argv[2]
N = int(sys.argv[3])
flagV = sys.argv[4] # flag for printing more information
flagH = sys.argv[5] # flag for header

if flagV == "noV":
   verbose = False
elif flagV == "yesV":
   verbose = True
else:
   print "error: flagV must be set to 'yesV' or 'noV', %s is not valid"%flagV

if flagH == "noH":
   header = False
elif flagH == "yesH":
   header = True
else:
   print "error: flagH must be set to 'yesH' or 'noH', %s is not valid"%flagV

if verbose:
   print "INFO: extractall path = "+ systdir

fh_extract = open(systdir+"extract_all.sort.uniq.txt",'r')
count = 0
ligsel = 0

sumE       = 0.0
sumG       = 0.0
sumEs      = 0.0
sumVDW     = 0.0
sumLigDesA = 0.0
sumLigDesP = 0.0
sumEnoG    = 0.0
sumR       = 0.0
sumabsR    = 0.0 # the absolute value
sumR2      = 0.0 # the absolute value
sumRnG     = 0.0
sumabsRnG  = 0.0
sumMagTot  = 0.0
sumEsPor   = 0.0 # porsion that is contributed by ES
sumVDWPor  = 0.0 # porsion that is contributed by VDW

minE    = 1000
maxE    = -1000
minG    = 1000
maxG    = -1000
minR    = 1000
maxR    = -1000

for line in fh_extract:
    splitline = line.split()
    name = splitline[2]
    totalE = float(splitline[21])
    ES      = float(splitline[12])
    GIST    = float(splitline[13])
    VDW     = float(splitline[14])
    LigDesA = float(splitline[15])
    LigDesP = float(splitline[16])
    totE_nogist = 0.0
    totE_recal = 0.0
    ratio = 0.0
    ratio_EnoG = 0.0
    mag_tot = 0.0
    for i in range(12,21): 
       totE_recal = totE_recal + float(splitline[i]) 
       if (i != 13):
           totE_nogist = totE_nogist + float(splitline[i]) 
       mag_tot = mag_tot + math.fabs(float(splitline[i]))
    if(totalE == 0 ): 
       print "warning: total E is zerro." 
       #exit()
    else: 
       ratio = GIST/totalE
    if(totE_nogist == 0):
       print "warning: total E_nogist is zerro."
    else:
       ratio_EnoG = GIST/totE_nogist 
    if (verbose):
       print count, totalE, totE_recal, totE_nogist, GIST, ratio, ratio_EnoG

    sumE       = sumE       + totalE 
    sumG       = sumG       + GIST
    sumEs      = sumEs      + ES
    sumVDW     = sumVDW     + VDW
    sumLigDesA = sumLigDesA + LigDesA
    sumLigDesP = sumLigDesP + LigDesP 
    sumEnoG    = sumEnoG    + totE_nogist
    sumR       = sumR       + ratio
    sumabsR    = sumabsR    + math.fabs(ratio)
    sumR2      = sumR2      + ratio**2
    sumRnG     = sumRnG     + ratio_EnoG
    sumabsRnG  = sumabsRnG  + math.fabs(ratio_EnoG)
    sumMagTot  = sumMagTot  + mag_tot
    sumEsPor   = sumEsPor   + (100.0*math.fabs(ES)/mag_tot) 
    sumVDWPor  = sumVDWPor  + (100.0*math.fabs(VDW)/mag_tot)

    if (totalE < minE):
       minE = totalE
    if (totalE > maxE):
       maxE = totalE
    if (GIST < minG):
       minG = GIST
    if (GIST > maxG):
       maxG = GIST
    if (ratio < minR):
       minR = ratio
    if (ratio > maxR):
       maxR = ratio

    if (count >= N): 
        break
    count = count + 1

if (header):
   print "sysname count avgE avgG avgES avgVDW avgLDA avgLDP avgEnoG avgR avgabsR avgR2 avgRnG avgabsRnG minE maxE minG maxG minR maxR totMag ESpor VDWpor" 
print "%s %d %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f"%(sysname, count, sumE/count, sumG/count, sumEs/count, sumVDW/count, sumLigDesA/count, sumLigDesP/count, sumEnoG/count, sumR/count, sumabsR/count, sumR2/count, sumRnG/count, sumabsRnG/count, minE, maxE, minG, maxG, minR, maxR, sumMagTot/count, sumEsPor/count, sumVDWPor/count )

fh_extract.close()



