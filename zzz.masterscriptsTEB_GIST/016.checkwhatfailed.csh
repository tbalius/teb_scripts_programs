# just checks what ran/failed

set enrich_dir = "docking/2runEnrich/4NVA"
#docking/2runEnrich/1YES_gist/dockedLigDecoyCombined/dirlist

#set type = "_nogist"
#set type = "_gist"
set type = "_gist_elstat0p9"
#set type = "_min"

foreach dir ( `cat $enrich_dir$type/dockedLigDecoyCombined/dirlist` )
#foreach dir ( `cat vs$type/dirlist_ori` )
  if !(-e $dir/OUTDOCK) then
     echo "$$dir/OUTDOCK does not exist"
  else if (`grep -c elapsed $dir/OUTDOCK` == "0") then
     echo "$dir/OUTDOCK is not complete"
  endif
end

 
