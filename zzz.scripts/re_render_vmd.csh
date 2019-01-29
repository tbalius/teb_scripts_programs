


awk '{if($1 == "Resolution"){printf "%s %d %d\n", $1, $2*4, $3*4  } else {print $0}}' vmdscene.dat > temp.dat

#/mnt/nfs/home/tbalius/zzz.programs/vmd/vmd-1.9.1_clash/lib/tachyon_LINUXAMD64 -aasamples 8 -trans_vmd -mediumshade vmdscene.dat -format BMP -o plot.bmp
/mnt/nfs/home/tbalius/zzz.programs/vmd/vmd-1.9.1_clash/lib/tachyon_LINUXAMD64 -aasamples 8 -trans_vmd -mediumshade temp.dat -format BMP -o plot.bmp

