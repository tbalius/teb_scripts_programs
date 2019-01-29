# just checks what ran/failed

#set type = "_nogist"
#set type = "_gist"
#set type = "_min"
set type = "_flex__gist"
#set type = "_flex__nogist"


#foreach dir ( `cat vs$type/dirlist_ori` )
foreach dir ( `cat vs$type/dirlist` )
  if !(-e vs$type/$dir/OUTDOCK) then
     echo "vs$type/$dir/OUTDOCK does not exist"
  else if (`grep -c elapsed vs$type/$dir/OUTDOCK` == "0") then
     echo "vs$type/$dir/OUTDOCK is not complete"
  endif
end

 
