
## This is writen by Trent Balius in the Shoichet Group.  
## this is Based on the Ultrafast Shape Recognition method discriped by
## Ballester and Richards:
## http://onlinelibrary.wiley.com/doi/10.1002/jcc.20681/full

import sys, mol2, math


## there are other mesures we could consider, euclidian distance 

def cal_normalized_similarity_score(vec1,vec2):
    ## normalized similarity score from Ballester et al
    ## this function will return a value on (0,1] where zerro is bad and one is good. 
    if (len(vec1) != len(vec2)):
        print "vectors are not the same length"
        exit

    # caluculate the manhatan distance
    man_d = 0
    for i in range(len(vec1)):
        man_d = man_d + math.fabs(vec1[i]-vec2[i])

    nss = 1/(1+(man_d/len(vec1))) ## normalized_similarity_score

    return nss

def cal_vec_tanimoto(vec1,vec2):
    ## this function cacluates the tanimoto value between two vectors.

    if (len(vec1) != len(vec2)):
        print "vectors are not the same length"
        exit

    V1dotV2 = 0 # dot product of vec1 and vec2
    V1sqrd  = 0 # dot product of vec1 and vec1 
    V2sqrd  = 0 

    for i in range(len(vec1)):
        V1dotV2 = V1dotV2 + vec1[i]*vec2[i]
        V1sqrd  = V1sqrd  + vec1[i]*vec1[i]
        V2sqrd  = V2sqrd  + vec2[i]*vec2[i]

    Tc = V1dotV2 / (V1sqrd + V2sqrd - V1dotV2)
    #print  Tc, "=", V1dotV2, "/ (", V1sqrd, "+", V2sqrd, "-", V1dotV2, ")"

    return Tc

def cal_pearson_corr(vec1,vec2):
    ## this function calculates pearson correlation.
    if (len(vec1) != len(vec2)):
        print "vectors are not the same length"
        exit

    EX  = 0 # mean of vec1
    EX2 = 0
    EY  = 0 # mean of vec2
    EY2 = 0 
    EXY = 0 # mean of  [vec1[i] * vec2[i]]

    N = len(vec1)    

    for i in range(N):
        EX  = EX  + vec1[i]
        EY  = EY  + vec2[i]
        EX2 = EX2 + vec1[i]**2
        EY2 = EY2 + vec2[i]**2
        EXY = EXY + vec1[i] * vec2[i]

    EX  = EX/N
    EY  = EY/N
    EX2 = EX2/N
    EY2 = EY2/N
    EXY = EXY/N

    corr = (EXY - EX*EY) / math.sqrt((EX2-EX**2)*(EY2-EY**2))
    return corr
   

def populate_hist(hist, dmax, dist):
    # hist is a vector wich contains a count in each bin
    # dmax is the maxium value to be bined in the histogram
    # min is set equal to zero
    if dist < dmax and dist >= 0:
       #hist[math.floor(d1)] = hist[math.floor(d1)] + 1
       index = int(math.floor(dist))
       hist[index] = hist[index] + 1
    elif (dist >= dmax):
       hist[dmax] = hist[dmax] + 1
    else: 
       print "something is wrong"
    return hist 
    

def cal_3D_discriptor_vec(mol):
    ## this function takes as input a molecule and outputs two vectors 
    ## The vectors encode the 3D shape of a molecule.
    ## 4 references points are idenified.  the centroid; 
    ## the closet atom to that centrid; the ferthest atom (f1) from
    ## the centroid; and the furthest atom from f1.
    ## The frist vector contains the 1st, 2nd, and 3rd moments 
    ## of the distances from these points. 
    ## the second vector is a histogram all of the distances are 
    ## bined. 

    N = len(mol.atom_list)
    centroid_X = 0
    centroid_Y = 0
    centroid_Z = 0
    ## calculate the centroid of the molecule
    for i in range(N): 
        centroid_X = centroid_X + mol.atom_list[i].X
        centroid_Y = centroid_Y + mol.atom_list[i].Y
        centroid_Z = centroid_Z + mol.atom_list[i].Z
        #centroid_Q = centroid_Q + mol.atom_list[i].Q
    centroid_Q = 0.0
    # X,Y,Z,Q,type,name,num,resnum,resname
    centroid = mol2.atom(centroid_X/N,centroid_Y/N,centroid_Z/N,centroid_Q,'Du','ctd',0,0,'ctd')

    vec = [0.0,0.0,0.0,  0.0,0.0,0.0,  0.0,0.0,0.0,  0.0,0.0,0.0]

    # hist is a population count 
    ## bin 1 will will contain distances 0-1
    ## bin 2, 1-2
    ## bin 3, 2-3 
    ## . . . 
    ## bin i, i-1,i
    ## . . . 
    ## bin 20, 19-12
    ## bin 21 will contain all distances greater than 20
    ## hist = [ 0, 0, 0, 0, 0,   0, 0, 0, 0, 0,   0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0]
    dmax = 25
    hist = []
    for i in range(0,dmax+1):
        hist.append(int(0))
    print "length of hist = ", len(hist)

    ## vec is has 12 elements; 4 sets of 3. 
     
    ## Calculate first, second and third moments of all distances to the centroid. 
    ## Calculate the closest point and the furthest to the centroid
    ## closest = closest to the centroid; extrema1 = furthest to the centroid;
    d2_min = 1000.0
    d2_max = 0.0
    m1 = 0
    m2 = 0
    m3 = 0
    for i in range(N):
        d2 = mol2.distance2(centroid,mol.atom_list[i])
        d1 = math.sqrt(d2)
        d3 = d1**3
        if (d2 < d2_min): 
            d2_min = d2
            closest = mol.atom_list[i]
        if (d2 > d2_max):
            d2_max = d2
            extrema1 = mol.atom_list[i] 
        m1 = m1 + d1 ## Frist moment.
        m2 = m2 + d2 ## Second moment.
        m3 = m3 + d3 ## Thrid moment.

        ##  populate bins in histogram
        hist = populate_hist(hist, dmax, d1)
    vec[0] = m1/N
    vec[1] = m2/N
    vec[2] = m3/N

    ## Calculate first, second and third moments of all distances to the closest atom to centroid.
    m1 = 0
    m2 = 0
    m3 = 0
    for i in range(N):
        d2 = mol2.distance2(closest,mol.atom_list[i])
        d1 = math.sqrt(d2)
        d3 = d1**3
        m1 = m1 + d1 ## Frist moment.
        m2 = m2 + d2 ## Second moment.
        m3 = m3 + d3 ## Thrid moment.

        ##  populate bins
        hist = populate_hist(hist, dmax, d1)


    vec[3] = m1/N
    vec[4] = m2/N
    vec[5] = m3/N

    ## Calculate first, second and third moments of all distances to the extrema1.
    ## idenify extrema2
    ## extrema2 = the furthest point to the the extrema1  
    d2_max = 0.0
    m1 = 0
    m2 = 0
    m3 = 0
    for i in range(N):
        d2 = mol2.distance2(extrema1,mol.atom_list[i])
        d1 = math.sqrt(d2)
        d3 = d1**3
        if (d2 > d2_max):
            d2_max = d2
            extrema2 = mol.atom_list[i]  
        m1 = m1 + d1 ## Frist moment.
        m2 = m2 + d2 ## Second moment.
        m3 = m3 + d3 ## Thrid moment.

        ##  populate bins
        hist = populate_hist(hist, dmax, d1)

    vec[6] = m1/N
    vec[7] = m2/N
    vec[8] = m3/N

    ## Calculate first, second and third moments of all distances to the extrema2.
    m1 = 0
    m2 = 0
    m3 = 0
    for i in range(N):
        d2 = mol2.distance2(extrema2,mol.atom_list[i])
        d1 = math.sqrt(d2)
        d3 = d1**3
        m1 = m1 + d1 ## Frist moment.
        m2 = m2 + d2 ## Second moment.
        m3 = m3 + d3 ## Thrid moment.

        ##  populate bins
        if d1 < 20 and d1 >= 0:
           hist[int(math.floor(d1))] = hist[int(math.floor(d1))] + 1
        if (d1 >= 20):
           hist[20] = hist[20] + 1

    vec[9]  = m1/N
    vec[10] = m2/N
    vec[11] = m3/N
    
    return vec, hist

def printvec(vec, fileh):
    for ele in vec:
        print ele,
        fileh.write("%f " % ele)
    print ""
    fileh.write("\n")

def main():
  if len(sys.argv) != 2: # if no input
     print "ERORR"
     return
  namemol2 = sys.argv[1]
  vecs = []
  mol_names = [] # this stores the name of the molecule. i.e. ZINC id. 

  print "start reading in "+ namemol2 
  filehandel = open(namemol2,'r')
  lines = filehandel.readlines()
  print "finished reading in "+ namemol2 

  LNUM = len(lines)
  print LNUM 
  linenum = 0

  filehandelvec  = open('vec.txt','w')
  filehandelhist = open('hist.txt','w')
  filehandeldisc = open('disc.txt','w')
  while (linenum < LNUM):
     print linenum
     [flag, mol, linenum]  = mol2.read_Mol2_lines(lines,linenum)
     print linenum

     if (not flag):
        break

     vec, hist = cal_3D_discriptor_vec(mol)
     mol_names.append(mol.name)
      
     vecs.append(vec)
     print "vec", 
     printvec(vec,filehandelvec)
     print "hist", 
     printvec(hist,filehandelhist)

     

  for i in range(0,len(vecs)):
      for j in range(i,len(vecs)):
          s1 = cal_normalized_similarity_score(vecs[i],vecs[j])
          s2 = cal_vec_tanimoto(vecs[i],vecs[j])
          s3 = cal_pearson_corr(vecs[i],vecs[j])
          print mol_names[i],mol_names[j],i,j,s1,s2,s3
          filehandeldisc.write("%d %d %f %f %f\n" % (i,j,s1,s2,s3))

  filehandelvec.close()
  filehandelhist.close()
  filehandeldisc.close()
   
main()




