
# script written by Trent Balius, 2020

foreach file (`ls cluster_*.txt`)


 echo "$file"
 cat $file | sed 's/..bits//g' | uniq -c | awk '{if ($1 == "2"){print $0}}'
 echo ""

end
