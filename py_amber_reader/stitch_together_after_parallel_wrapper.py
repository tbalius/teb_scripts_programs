
import os, sys, math

# This script is written by Trent E Balius on 2023/05/26.  
# This will process the output parrallel the matrices for the per-residue energy calculation and stich them together. 

def read_dataM(filename,Mat):
    #Mat = []
    fh = open(filename,'r') 
    rowl = -1
    for line in fh: 
        row = []

        #if rowl == -2: # header
        #   rol1 = -1
        if 'AVG' in line:
            continue
        for ele in line.strip().split(','): 
            row.append(ele) 
        if rowl == -1: # header
            rowl = len(row)
        elif rowl != len(row): 
             print(filename)
             print(rowl,len(row))
             print("Error. rows are not all the same length.")
             exit()
        #print (row)
        Mat.append(row)
    return len(Mat),len(Mat[0])    

def write_matrix(Mat,filename):
    txt = ''
    M = len(Mat)
    for i in range(M):
        N = len(Mat[i])
        for j in range(N):
            txt = txt + str(Mat[i][j])
            if j < N-1:
               txt=txt+','
        txt=txt+'\n'
    fh = open(filename,'w')
    fh.write(txt)
    fh.close()

def main():


    print ("syntax: python script num_subset_rows num_subset_columns type")
    print ("        example input:")
    print ("          num_subset_rows = 7")
    print ("          num_subset_columns = 128")
    print ("          type = vdw, ele, or tot")
    if (len(sys.argv) != 4):
       print ("Error.  Wrong number of inputs.  this script requiers 3 inputs")
       exit()

    M           = int(sys.argv[1])
    N           = int(sys.argv[2])
    type_name   = sys.argv[3]

    print("M     = %d"%M )
    print("N     = %d="%N )
    print("type  = "+type_name)


    #name = "vdwrst_fp_"
    name = type_name+"rst_fp_"
    ext  = "avg" # extention
    #M = 64
    #N = 64
    #M = 7
    #N = 128
    
    #fh = os.popen('ls vdwrst_fp_*.avg')
    #fh = os.popen('ls %s*.%s'%(name,ext))
    #fh = os.popen('ls */*/%s*.%s'%(name,ext))
    fh = os.popen('ls */%s*.%s'%(name,ext))
    
    filelist = []
    filenum = []
    for line in fh:
        print(line)
        linestrip = line.strip()
        filelist.append(linestrip)
        #temp = linestrip.split('.')[0]
        #temp = temp[10:-1]
        #print(temp)
        #filenum.append(int(temp))
    fh.close()
    
    lenlist = len(filelist)
    print(lenlist)
    sqrtlenlist = math.sqrt(lenlist)
    print (sqrtlenlist)
    
    if M*N != lenlist: 
       print("%d*%d != %d"%(M,N,lenlist))
       exit()
    
    # ls does not print the files in the right order.
    filelist_ls = filelist
    filelist = []
    
    # we need to read in the files in the right order. 
    for i in range(M*N):
         #filename = '%s%d.%s'%(name,i,ext)
         filename = 'job_%05d/%s%d.%s'%(i+1,name,i,ext)
         print(filename)
         filelist.append(filename)
    
    #count = 0
    all_mat = []
    all_m = 0
    all_n = 0
    mat_index = [] # this will store i (indicating subset1) j (,subset2), all_m, all_n
    for i in range(M):
        all_n = 0
        for j in range(N):
            k = i*N+j 
            #print(count,k)
            #count=count+1
            temp_mat = []
            mtemp,ntemp = read_dataM(filelist[k],temp_mat)
            #print (mtemp,ntemp)
            mat_index.append([i,j,all_m,all_n,mtemp,ntemp])
            all_mat.append(temp_mat)
            all_n = all_n + ntemp
            #print(mat_index[k])
        all_m = all_m + mtemp
    print(all_m,all_n)
    #exit()
    
    stiched_M = []
    for i in range(all_m): 
        row = []
        for j in range(all_n):
             row.append(0.0)
        stiched_M.append(row)
    
    for k in range(len(mat_index)):
        print("job %d"%k)
        print(filelist[k])
        ss1,ss2,start1,start2,m1,n2 = mat_index[k]
        print (ss1,ss2,start1,start2,m1,n2)
        for i in range(m1):
            printstring = ""
            for j in range(n2):
                i_n = start1 + i 
                j_n = start2 + j 
                print(i_n,j_n)
                printstring =  printstring + " " + str(all_mat[k][i][j])
                stiched_M[i_n][j_n] = all_mat[k][i][j]
            print(printstring)
    write_matrix(stiched_M,type_name+'_stiched.csv')

main()    
