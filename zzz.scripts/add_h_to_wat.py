
import pdb_lib
import sys,copy

# Written by Trent E. Balius, B. Shoichet Lab

O  = [ 28.781,  50.284,  29.051]
H1 = [ 29.738,  50.284,  29.051]
H2 = [ 28.541,  51.210,  29.051]

pdb_file = sys.argv[1]

wat_o = pdb_lib.read_pdb(pdb_file)

print len(wat_o)

fh = open(pdb_file+".rst7",'w')

new_wat = []
count = 0
for c in wat_o:
  print c.X
  print c.Y
  print c.Z
  new_wat.append(c)
  #count = count+1
  c1 = copy.copy(c)
  new_wat.append(c1)
  count = count+1
  new_wat[count].atomname = " H1 " #= line[12:16
  new_wat[count].X = new_wat[count].X+H1[0]-O[0] #
  new_wat[count].Y = new_wat[count].Y+H1[1]-O[1] #
  new_wat[count].Z = new_wat[count].Z+H1[2]-O[2] #
  c2 = copy.copy(c)
  new_wat.append(c2)
  count = count+1
  new_wat[count].atomname = " H2 " #= line[12:16
  new_wat[count].X = new_wat[count].X+H2[0]-O[0] #
  new_wat[count].Y = new_wat[count].Y+H2[1]-O[1] #
  new_wat[count].Z = new_wat[count].Z+H2[2]-O[2] #
  fh.write(" %11.7f %11.7f %11.7f %11.7f %11.7f %11.7f\n %11.7f %11.7f %11.7f\n"%(new_wat[0].X,new_wat[0].Y,new_wat[0].Z,new_wat[1].X,new_wat[1].Y,new_wat[1].Z,new_wat[2].X,new_wat[2].Y,new_wat[2].Z))

fh.close()
pdb_lib.output_pdb(new_wat,pdb_file+"_new")

#  len(c)
#  for a in c:
#      print a

