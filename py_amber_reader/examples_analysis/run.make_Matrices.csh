

#python ~/zzz.scripts/py_amber_reader/amber_reader_mod.py ../com.leap.prm7 strip/strip.mdcrd "1-201" "202-402" "fp.d1_1-201.d2_202-402"
#python ~/zzz.scripts/py_amber_reader/amber_reader_mod.py ../com.leap.prm7 strip/strip.mdcrd "1-201" "403-601" "fp.d1_1-201.d3_403-601"
python ~/zzz.scripts/py_amber_reader/amber_reader_mod.py ../com.leap.prm7 strip/strip.mdcrd "202-402" "602-803" "fp.d2_202-402.d4_602-803"
#python ~/zzz.scripts/py_amber_reader/amber_reader_mod.py ../com.leap.prm7 strip/strip.mdcrd "1-803" "804-816" "fp.1-803.804-816"

