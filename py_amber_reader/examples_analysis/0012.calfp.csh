

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
   python ~/zzz.scripts/py_amber_reader/amber_reader.py ../../com.leap.prm7 strip.mdcrd "1-803" "$res"  "fp.1-803.$res.txt"
end 

