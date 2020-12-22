
# script written by Trent Balius, 2020


#set listpdb = `grep "interface" symestry.txt | cut -c 9-13`
#set list1 = `grep "interface" symestry.txt | cut -c 9-13,44`
#set list2 = `grep "interface" symestry.txt | cut -c 9-13,52`

mkdir copy_interfaces

set pwd = `pwd`

foreach line (`grep "interface" symestry.txt | awk '{print $2}'`)

    set dir = `echo $line | cut -c 1-29`
    set pdb = `echo $line | cut -c 1-4`
    set file1 = `echo $line | cut -c 1-4,35-36`
    set file2 = `echo $line | cut -c 1-4,43-44`
    #echo ${dir} ${file1} ${file2}
    ls -l ${dir}/${pdb}_chains/${file1}.pdb
    ls -l ${dir}/${pdb}_chains/${file2}.pdb

    cat ${dir}/${pdb}_chains/${file1}.pdb ${dir}/${pdb}_chains/${file2}.pdb > $pwd/copy_interfaces/${file1}_${file2}_interface.pdb

end


