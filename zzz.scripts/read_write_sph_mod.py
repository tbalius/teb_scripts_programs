
import sys
import sph_lib

def main():
    if len(sys.argv) != 7: # if no input
       print ("ERORR: there need to be 4 inputs: inputfilename, outputfilename, cluster_number, sphere color, radius_max, radius_min")
       print ("       if cluster number = 'A' all clusters are used.")
       print ("       if color number   = 'A' all colors   are used.")
       print ("       if color number   = 'A' all colors   are used.")
       print ("       if radius_max  = '-1.0' this criteria is not appied.")
       print ("       if radius_min  = '-1.0' this criteria is not appied.")
       return

    fileinput  = sys.argv[1]
    fileoutput = sys.argv[2]
    ccluster   = sys.argv[3]
    color      = sys.argv[4]
    r_max      = float(sys.argv[5])
    r_min      = float(sys.argv[6])

    print ('input =' + fileinput)
    print ('output =' + fileoutput)

    list = sph_lib.read_sph_r(fileinput,ccluster,color,r_max,r_min)
    sph_lib.write_sph(fileoutput,list)

main()
