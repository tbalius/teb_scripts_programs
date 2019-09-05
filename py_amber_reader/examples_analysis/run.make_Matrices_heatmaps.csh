
## ls -l *1-803*avg
## -rw-r--r--. 1 tbalius bks  99606 Oct 14 01:14 elefp.1-803.804-816.avg
## -rw-r--r--. 1 tbalius bks  99664 Oct 14 01:14 totfp.1-803.804-816.avg
## -rw-r--r--. 1 tbalius bks 104394 Oct 14 01:14 vdwfp.1-803.804-816.avg

#sed '1d'   vdwfp.1-803.804-816.avg >! vdwfp.1-803.804-816.avg.txt
#tail -n +2 elefp.1-803.804-816.avg >! elefp.1-803.804-816.avg.txt

sed '1d'   vdwfp.804-816.804-816.txt.avg >! vdwfp.804-816.804-816.avg.txt
tail -n +2 elefp.804-816.804-816.txt.avg >! elefp.804-816.804-816.avg.txt


#sed '1d'   vdwfp.d1_1-201.d3_403-601.avg   > vdwfp.d1_1-201.d3_403-601.avg.txt
#tail -n +2 elefp.d1_1-201.d3_403-601.avg   > elefp.d1_1-201.d3_403-601.avg.txt

#sed '1d'   vdwfp.d2_202-402.d4_602-803.avg >! vdwfp.d2_202-402.d4_602-803.avg.txt
#tail -n +2 elefp.d2_202-402.d4_602-803.avg >! elefp.d2_202-402.d4_602-803.avg.txt

#python heatmap_matrix_mod.py vdwfp.d1_1-201.d2_202-402.avg 0.0 -1.0 1.0  '../resnames.1.1.txt' '../resnames.1.2.txt' >  vdwfp.d1_1-201.d2_202-402.avg.log
#python heatmap_matrix_mod.py elefp.d1_1-201.d2_202-402.avg 0.0 -30.0 30.0 '../resnames.1.1.txt' '../resnames.1.2.txt'> elefp.d1_1-201.d2_202-402.avg.log

#python heatmap_matrix_mod.py vdwfp.d1_1-201.d3_403-601.avg 0.0 -1.0 1.0   '../resnames.1.1.txt' '../resnames.1.3.txt'> vdwfp.d1_1-201.d3_403-601.avg.log
#python heatmap_matrix_mod.py elefp.d1_1-201.d3_403-601.avg 0.0 -30.0 30.0 '../resnames.1.1.txt' '../resnames.1.3.txt'> elefp.d1_1-201.d3_403-601.avg.log

#python heatmap_matrix_mod.py  vdwfp.d2_202-402.d4_602-803.avg  0.0 -1.0 1.0   '../resnames.1.2.txt' '../resnames.1.4.txt'> vdwfp.d2_202-402.d4_602-803.avg.log 
#python heatmap_matrix_mod.py  elefp.d2_202-402.d4_602-803.avg  0.0 -30.0 30.0 '../resnames.1.2.txt' '../resnames.1.4.txt'> elefp.d2_202-402.d4_602-803.avg.log 

#python heatmap_matrix_mod.py  vdwfp.1-803.804-816.avg  0.0 -1.0 1.0   '../resnames.1.txt' '../resnames.2.txt'> vdwfp.1-803.804-816.avg.log 
#python heatmap_matrix_mod.py  elefp.1-803.804-816.avg  0.0 -30.0 30.0 '../resnames.1.txt' '../resnames.2.txt'> elefp.1-803.804-816.avg.log 

python heatmap_matrix_mod.py  vdwfp.804-816.804-816.avg  0.0 -1.0 1.0   '../resnames.2.txt' '../resnames.2.txt'> vdwfp.804-816.804-816.avg.log 
python heatmap_matrix_mod.py  elefp.804-816.804-816.avg  0.0 -30.0 30.0 '../resnames.2.txt' '../resnames.2.txt'> elefp.804-816.804-816.avg.log 

#-rw-r--r--. 1 tbalius bks 384802 Oct 12 11:10 totfp.d1_1-201.d2_202-402.avg
#-rw-r--r--. 1 tbalius bks 404015 Oct 12 11:10 vdwfp.d1_1-201.d2_202-402.avg
#-rw-r--r--. 1 tbalius bks 384600 Oct 12 11:10 elefp.d1_1-201.d2_202-402.avg
#-rw-r--r--. 1 tbalius bks  99606 Oct 14 01:14 elefp.1-803.804-816.avg
#-rw-r--r--. 1 tbalius bks 384600 Oct 12 11:10 elefp.d1_1-201.d2_202-402.avg
#-rw-r--r--. 1 tbalius bks 469559 Oct 12 14:48 elefp.d1_1-201.d2_202-402.avg.log
#-rw-r--r--. 1 tbalius bks 753965 Oct 12 14:48 elefp.d1_1-201.d2_202-402.avg.png
#-rw-r--r--. 1 tbalius bks 384593 Oct 12 12:21 elefp.d1_1-201.d2_202-402.avg.txt
#-rw-r--r--. 1 tbalius bks 381033 Oct 13 03:51 elefp.d1_1-201.d3_403-601.avg
#-rw-r--r--. 1 tbalius bks 388527 Oct 13 20:28 elefp.d2_202-402.d4_602-804.avg
#-rw-r--r--. 1 tbalius bks  99664 Oct 14 01:14 totfp.1-803.804-816.avg
#-rw-r--r--. 1 tbalius bks 384802 Oct 12 11:10 totfp.d1_1-201.d2_202-402.avg
#-rw-r--r--. 1 tbalius bks 381154 Oct 13 03:51 totfp.d1_1-201.d3_403-601.avg
#-rw-r--r--. 1 tbalius bks 388653 Oct 13 20:28 totfp.d2_202-402.d4_602-804.avg
#-rw-r--r--. 1 tbalius bks 104394 Oct 14 01:14 vdwfp.1-803.804-816.avg
#-rw-r--r--. 1 tbalius bks 404015 Oct 12 11:10 vdwfp.d1_1-201.d2_202-402.avg
#-rw-r--r--. 1 tbalius bks 490286 Oct 12 14:48 vdwfp.d1_1-201.d2_202-402.avg.log
#-rw-r--r--. 1 tbalius bks 615366 Oct 12 14:48 vdwfp.d1_1-201.d2_202-402.avg.png
#-rw-r--r--. 1 tbalius bks 404008 Oct 12 12:16 vdwfp.d1_1-201.d2_202-402.avg.txt
#-rw-r--r--. 1 tbalius bks 399997 Oct 13 03:51 vdwfp.d1_1-201.d3_403-601.avg
#-rw-r--r--. 1 tbalius bks 408035 Oct 13 20:28 vdwfp.d2_202-402.d4_602-804.avg

