#! /usr/bin/python2.7

# writen by Trent balius

# remove list from extract all file. 

import sys

def read_outdock_file(infilename,match,conf,match_pose, conf_pose, match_nopose, conf_nopose):

    infile = open(infilename,'r')
    lines = infile.readlines()
    infile.close()

    loc_match = 0
    loc_conf  = 0
    loc_match_pose = 0
    loc_conf_pose  = 0
    loc_match_nopose = 0
    loc_conf_nopose  = 0

    old_molnum = 0

    flag_read = False
    for line in lines:
        #line = line.strip('\n')
        splitline = line.split()

        #print len(splitline)
        #if len(splitline) ==0:
        if len(splitline) < 2 :
            continue

        if "we" == splitline[0]: # we reached the end of the file, docking results.
             flag_read = False

        if "warning:" == splitline[0]: 
             continue
        if "Error." == splitline[0]: 
             continue
#        if ">" == splitline[1]: 
#             continue
        if len(splitline) > 4:
             if "bonds" == splitline[2] and "error" == splitline[4]: 
                 #print line
                 print "bond error"
                 continue
        if "skipping"  == splitline[0]:
             print line
             continue 
#        if "<" == splitline[1]:
#             continue
#       if len(splitline) <= 4: 
#          print line
#          continue

        if flag_read:         

          #if len(splitline) != 21:
          #   print line
          #   continue
          #print line
          if not "ZINC" in splitline[1]:
             print line
             continue

          flag_pose = False # this is a pose produesed
          flag_nopose = False # this is not a pose produses

          if len(splitline) == 21:
            molnum = int(splitline[0])
            zid = splitline[2].split('.')[0]
            temp_match = int(splitline[3])
            temp_conf  = int(splitline[4])
            flag_pose = True # there is a pose
          elif len(splitline) > 4:
            molnum = int(splitline[0])
            zid = splitline[1].split('.')[0]
            temp_match = int(splitline[2])
            temp_conf  = int(splitline[3])
            flag_nopose = True # there is no pose


          if molnum != old_molnum: # only count the same mol# ones, we flex receptor is used each mol# has multiple lines
             #print line
             old_molnum = molnum
             loc_match = loc_match + temp_match
             loc_conf  = loc_conf  + temp_conf 
             if flag_pose:
                loc_match_pose = loc_match_pose + temp_match
                loc_conf_pose  = loc_conf_pose + temp_conf
             elif flag_nopose: 
                loc_match_nopose = loc_match_nopose + temp_match
                loc_conf_nopose  = loc_conf_nopose + temp_conf
             else: 
                print "Error..."
                exit


        if  "mol#" == splitline[0]: # start of docking resutls
             flag_read = True


           
        #if id in zincdict: 
        #   print "excluding " + id
        #   continue
        #outfile.write(line)
    match = match+loc_match
    conf = conf+loc_conf
    match_pose = match_pose + loc_match_pose
    conf_pose  = conf_pose + loc_conf_pose
    match_nopose = match_nopose + loc_match_nopose
    conf_nopose  = conf_nopose + loc_conf_nopose


    print 'file=%s; match=%d ; conf=%d\n\tpose match=%d ; pose conf=%d\n\tno pose match=%d ; no pose conf=%d\n'%(infilename,loc_match, loc_conf, loc_match_pose, loc_conf_pose, loc_match_nopose, loc_conf_nopose)
    return match, conf, match_pose, conf_pose, match_nopose, conf_nopose

def main():
   if len(sys.argv) != 2:
      print "error:  this program takes 1 argument "
      print "(1) dirlist where outdock file are.  "    
      exit()
   
   filename1     = sys.argv[1]
   
   print "(1) dirlist = " + filename1
   fh = open(filename1)  

   match        = 0 # number of orients
   conf         = 0 # number of segments scored, one poses is made up of multiple segments.
   # some have poses.
   match_pose   = 0
   conf_pose    = 0
   # some fail to produce poses.
   match_nopose = 0
   conf_nopose  = 0 
   for line in fh:
       print line
       #splitline = line.split() 
       filename = line.split()[0]+'/OUTDOCK'
       match,conf,match_pose, conf_pose, match_nopose, conf_nopose = read_outdock_file(filename,match,conf,match_pose,conf_pose,match_nopose,conf_nopose)
   print  'total; match=%d ; conf=%d\n'%(match,conf)
   print  'pose total; match=%d ; conf=%d\n'%(match_pose,conf_pose)
   print  'no pose total; match=%d ; conf=%d\n'%(match_nopose,conf_nopose)


main()

