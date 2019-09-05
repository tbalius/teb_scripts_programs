

#closest <# to keep> <mask> [noimage] [first | oxygen] [closestout <filename>] [outprefix <parmprefix>] 

set mountdir = `pwd`
set workdir  = $mountdir/strip

cd $workdir


#python ~/zzz.scripts/py_amber_reader/amber_reader.py ../../com.leap.prm7 strip.mdcrd "1-803"    "804-816" "fp.1-803.804-816.txt"
#python ~/zzz.scripts/py_amber_reader/amber_reader.py ../../com.leap.prm7 strip.mdcrd "804-816"  "1-803"   "fp.804-816.1-803.txt"


#foreach res ("804 805 806 807 808 809 810 811 812 813 814 815 816")
foreach res ( \
 "804" \
 "805" \
 "806" \
 "807" \
 "808" \
 "809" \
 "810" \
 "811" \
 "812" \
 "813" \
 "814" \
 "815" \
 "816" \
)
   awk 'BEGIN{flag="F"}{if(flag=="T"){print $0};if($1=="AVG"){flag="T"}}' "fp.1-803.$res.txt" > "fp.1-803.$res.avg.txt"
   awk -F, '{print $2}' "fp.1-803.$res.avg.txt" > "fp.1-803.$res.avg_tot.txt"
   awk -F, '{print $3}' "fp.1-803.$res.avg.txt" > "fp.1-803.$res.avg_vdw.txt"
   awk -F, '{print $4}' "fp.1-803.$res.avg.txt" > "fp.1-803.$res.avg_ele.txt"
end 

paste -d, fp.1-803.???.avg_tot.txt > fp.1-803.804-816.avg_tot.txt
paste -d, fp.1-803.???.avg_vdw.txt > fp.1-803.804-816.avg_vdw.txt
paste -d, fp.1-803.???.avg_ele.txt > fp.1-803.804-816.avg_ele.txt

