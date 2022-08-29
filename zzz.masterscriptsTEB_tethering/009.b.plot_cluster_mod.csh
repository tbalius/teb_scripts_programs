## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017
#set mountdir = `pwd`
set mountdir_ori = `pwd`
set mut = E37C
#set lig = DL2040
#set lig = DL2078 
set lig = DL1314_Protomer1

foreach pose (   \
               1 \
               2 \
               3 \
)
set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
cd $mountdir


#set workdir  = $mountdir/009.clustering/
#set workdir  = $mountdir/009.clustering_2.0/
#set workdir  = $mountdir/009.clustering_2.0_mod/
set workdir  = $mountdir/009.clustering_4.0_mod/
cd $workdir


#python $mountdir/009.plot_cluster.py cnumvtime.dat    cnumvtime        cnumvtime
python ${mountdir_ori}/009.plot_cluster_color.py cnumvtime.dat    cnumvtime2        cnumvtime2
python ${mountdir_ori}/009.plot_cluster_color_mod.py cnumvtime.dat cnum_hist_E cnum_hist_E
python ${mountdir_ori}/009.plot_cluster_color_zoomin2.py cnumvtime.dat    cnumvtime2        cnumvtime2_zoomin2

#exit

echo "top clusters"
echo "cluster_size cluster_name"
#awk '{print $2}' 009.clustering_0/cnumvtime.dat  | sort | uniq -c | sort -rnk1 | head 
echo "top"
#awk '{print $2}' cnumvtime.dat  | sort | uniq -c | sort -rnk1 | head 
cat cnumvtime.dat | grep -v "#Frame" |awk '{print $2}'  | sort | uniq -c | sort -rnk1 | head 
echo "bottom"
#awk '{print $2}' cnumvtime.dat  | sort | uniq -c | sort -rnk1 | tail 
cat cnumvtime.dat | grep -v "#Frame" | awk '{print $2}'  | sort | uniq -c | sort -rnk1 | tail 

echo "cluster_name ratio log delta_E"
#awk '{print $2}' cnumvtime.dat  | sort | uniq -c | sort -rnk1 | head | awk 'BEGIN{Kb=0.001985875;temp=298.15;count=0}{if (count==0){ref=$1;print $2, "NA"}else{val=ref/$1;dE=Kb*temp*log(val);printf"%d %f %f %12.9f\n", $2, val, log(val), dE};count=count+1}'
cat cnumvtime.dat | grep -v "#Frame" | awk '{print $2}'  | sort | uniq -c | sort -rnk1 | head | awk 'BEGIN{Kb=0.001985875;temp=298.15;count=0}{if (count==0){ref=$1;print $2, "NA"}else{val=ref/$1;dE=Kb*temp*log(val);printf"%d %f %f %12.9f\n", $2, val, log(val), dE};count=count+1}'

set N = `cat cnumvtime.dat | grep -v "#Frame" | wc -l`

#cat cnumvtime.dat | awk '{print $2}' cnumvtime.dat  | sort | uniq -c | sort -rnk1 | head | awk 'BEGIN{N='$N';S=0}{p=$1/N;print p;S=S+p*log(p)}END{print S}' 
cat cnumvtime.dat | grep -v "#Frame" | awk '{print $2}'   | sort | uniq -c | sort -rnk1       | awk 'BEGIN{N='$N';S=0}{p=$1/N;S=S+p*log(p)}END{printf"S=%f\n",S}' 
cat cnumvtime.dat | grep -v "#Frame" | awk '{print $2}'   | sort | uniq -c | sort -rnk1 |head | awk 'BEGIN{N='$N';S=0}{p=$1/N;S=S+p*log(p)}END{printf"Stop=%f\n",S}' 
cat cnumvtime.dat | grep -v "#Frame" | awk '{print $2}'   | sort | uniq -c | sort -rnk1 |tail | awk 'BEGIN{N='$N';S=0}{p=$1/N;S=S+p*log(p)}END{printf"Sbot=%f\n",S}' 

#end
end # pose
