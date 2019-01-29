import sys, struct

## Writen by Trent Balius in the Shoichet Group
## converts a phi grid to dx. 

def read_phi_write_dx(pfilename,dfilename):
    #outdx = open(dfilename,'w')
    inphi = open(pfilename,"rb")
    #text = inphi.read(104)
    #print text
    #text = inphi.read(4)
    #print text
    text = inphi.read(4)
    print text
    #exit()
    text = inphi.read(96)
    print text
    #for line in inphi
    count = 0
    flag = True
    oldmid = [0.0, 0.0, 0.0]
    while flag: 
       text = ''
       #val = inphi.read(8)
       #print val
       if (count < 63**3):
        text = struct.unpack('f', inphi.read(4))
       else:
        #c = inphi.read(1)
        #print c 
        #if c == '':
        #   flag = False
        #else:
        #   text = struct.unpack('1s',c)
       #print text
       #count = count +1

         botlabel = struct.unpack('16s', inphi.read(16))
         #print "botlabel:", self.botlabel
         junk = struct.unpack('8s', inphi.read(8))
         (scale, oldmid[0], oldmid[1], oldmid[2],) = \
             struct.unpack('>ffff', inphi.read(16))
         #print "scale, oldmid:", self.scale, self.oldmid
         junk = struct.unpack('4s', inphi.read(4))
         c = inphi.read(1)
         if c == '':
           flag = False
       print text
       count = count +1
        
    inphi.close()
    #outdx.close()
    return

def main():
  if len(sys.argv) != 3: # if no input
     print "ERORR"
     return
  namephi = sys.argv[1]
  namedx = sys.argv[2]
  read_phi_write_dx(namephi,namedx)
main()


