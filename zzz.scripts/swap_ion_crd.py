

# Writen by Trent Balius 2023.01.05 at FNLCR
# this function swapt coordenates in a trajectory. 
# I need to exchange two ions.  

import sys


def replace_entry(split_lines_array,line_num_1,line_loc_1, line_num_2, line_loc_2):
   # split_lines_array is an array of arrays of strings, each string is a coordenate.  
   # we will go to the two locations and swap entrys
   print ("swap: line (%d) loc (%d) val=%s <--> line (%d) loc (%d) val=%s"%(line_num_1,line_loc_1,split_lines_array[line_num_1][line_loc_1], line_num_2, line_loc_2,split_lines_array[line_num_2][line_loc_2]))
   temp = split_lines_array[line_num_1][line_loc_1]
   temp2 = split_lines_array[line_num_2][line_loc_2]
   #split_lines_array[line_num_1][line_loc_1] = split_lines_array[line_num_2][line_loc_2]
   split_lines_array[line_num_1][line_loc_1] = temp2
   split_lines_array[line_num_2][line_loc_2] = temp

def write_coord(split_lines_array,fhandel): 
    print (" in write_coord")
    for i in range(len(split_lines_array)):
        line = ''
        for j in range(len(split_lines_array[i])): 
            line = line+split_lines_array[i][j]
        fhandel.write(line+'\n')

def main():

    if (len(sys.argv) != 6): # if no input
        print " (1) mdcrd file name,"
        print " (2) atom num 1,"
        print " (3) atom num 2,  ";
        print " (4) total atoms  ";
        print " (5) output file  ";
        return

    incrdfilename  = sys.argv[1]
    ai1            = int(sys.argv[2])
    ai2            = int(sys.argv[3])
    tot_a          = int(sys.argv[4])
    output         = sys.argv[5]

    print('incrdfilename  = %s'%incrdfilename )
    print('ai1            = %d'%ai1           )
    print('ai2            = %d'%ai2           )
    print('tot_a          = %d'%tot_a         )
    print('output         = %s'%output        )

    filer = open(incrdfilename,'r')
    filew = open(output,'w')
    line_1 = [0, 0, 0]
    line_loc_1 = [0, 0, 0]
    line_2 = [0, 0, 0]
    line_loc_2 = [0, 0, 0]

    # what line is x on
    #line_1[0] = ((ai1-1)*3-2) / 10 + 1
    line_1[0] = ((ai1-1)*3+0) / 10 
    # what line is y on
    #line_1[1] = ((ai1-1)*3-1) / 10 + 1
    line_1[1] = ((ai1-1)*3+1) / 10
    # what line is z on
    #line_1[2] = ((ai1-1)*3-0) / 10 + 1
    line_1[2] = ((ai1-1)*3+2) / 10 

    #line_loc_1[0] = ((ai1-1)*3-2) % 10 
    line_loc_1[0] = ((ai1-1)*3+0) % 10 
    line_loc_1[1] = ((ai1-1)*3+1) % 10  
    line_loc_1[2] = ((ai1-1)*3+2) % 10 

    print ("atom1: location 1 on line (%d) = %d\nlocation 3 on line (%d) = %d\n"%(line_1[0],line_loc_1[0],line_1[2],line_loc_1[2]))

    #line_2[0] = ((ai2-1)*3-2) / 10 + 1
    #line_2[1] = ((ai2-1)*3-1) / 10 + 1
    #line_2[2] = ((ai2-1)*3-0) / 10 + 1
    line_2[0] = ((ai2-1)*3+0) / 10 
    line_2[1] = ((ai2-1)*3+2) / 10 
    line_2[2] = ((ai2-1)*3+3) / 10 

    #line_loc_2[0] = ((ai2-1)*3-2) % 10 
    line_loc_2[0] = ((ai2-1)*3+0) % 10 
    line_loc_2[1] = ((ai2-1)*3+1) % 10 
    line_loc_2[2] = ((ai2-1)*3+2) % 10 

    print ("atom2: location 1 on line (%d) = %d\nlocation 3 on line (%d) = %d\n"%(line_2[0],line_loc_2[0],line_2[2],line_loc_2[2]))

    #if (line_loc_2_1 == 0 ):
       

    #last_line = (tot_a-1) * 3 / 10 + 1
    #last_line = (tot_a-1) * 3 / 10 
    last_line = ((tot_a-1) * 3+2) / 10 # z coord. 
    #last_mod = (tot_a-1) * 3 % 10
    last_mod = ((tot_a-1) * 3+2) % 10
    print ("last line: location 3 on line (%d) = %d\n"%(last_line,last_mod))
    #exit() 

    
    count = 0 
    split_lines = []
    frist_line = True
    #fline = ''
    for line in filer:
        if frist_line: 
            #fline = line
            filew.write(line)
            frist_line = False
            continue
        # break line up into peices of the same lenth, each entry has a lenth of 8. 
        coord_len = 8
        count_c = 0
        splitline = [] 
        #print("line lenth = %d"%int(len(line)))
        #for char in line.strip():
        for char in line:
             if count_c == 0: 
                 temp_str = ''
             if count_c < coord_len:
                 temp_str = temp_str+char # catonate char on string
             count_c = count_c+1
             if count_c >= coord_len: 
                 #print(temp_str)
                 #print("sting len = %d"%int(len(temp_str)))
                 splitline.append(temp_str)
                 count_c = 0
        split_lines.append(splitline)

        if count == last_line: 
           for i in range(3): 
             replace_entry(split_lines,line_1[i],line_loc_1[i],line_2[i],line_loc_2[i])

           write_coord(split_lines,filew)
           split_lines = []
      # for i in range(3): 
      #   if count == line_1[i]: 
      #      print (line)

      # for i in range(3): 
      #   if count == line_2[i]: 
      #      print (line)

        count = count + 1
        if count > last_line: 
           print (line)
           count=0
           #exit()
           #break
          
    filer.close()
    filew.close()

main()

