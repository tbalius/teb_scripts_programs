

foreach file (`ls ????/????_*.pdb`)

   set filename = $file:r 
   #echo $filename $file
   grep "^ATOM " ${file} > ${filename}_rec.pdb
   grep " HEM " ${file} | sed 's/HETATM/ATOM  /g' >> ${filename}_rec.pdb

end

