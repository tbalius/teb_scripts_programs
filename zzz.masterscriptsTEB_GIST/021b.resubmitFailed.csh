

#set type = "_nogist"
#set type = "_gist"
set type = "_min"

if (-e vs$type/dirlist_new) then
   echo "Ooh.  vs$type/dirlist_new exists."
   echo "remove it and try again"
   echo "rm -f vs$type/dirlist_new"
   exit
endif

#  ls -l vs$type/$dir/OUTDOCK
foreach dir ( `cat vs$type/dirlist` )
  if !(-e vs$type/$dir/OUTDOCK) then
     echo "vs$type/$dir/OUTDOCK does not exist"
     echo $dir >> vs$type/dirlist_new
  else if (`grep -c elapsed vs$type/$dir/OUTDOCK` == "0") then
     echo "vs$type/$dir/OUTDOCK is not complete"
     echo $dir >> vs$type/dirlist_new
  endif
end 

if !(-e vs$type/dirlist_ori) then 
    mv vs$type/dirlist vs$type/dirlist_ori
endif

cp vs$type/dirlist_new vs$type/dirlist



# stderr and OUTDOCK can cause trouble -> remove those form the respective dirs first before rerunning the jobs

#check the files
foreach dir ( `cat vs$type/dirlist` )
    ls vs$type/$dir/OUTDOCK vs$type/$dir/stderr vs$type/$dir/test.mol2.gz
    cat vs$type/$dir/stderr
    tail vs$type/$dir/OUTDOCK
end


echo "kill with cntl C if something seems wrong, pausing for a few seconds"
sleep 20


# remove them
foreach dir ( `cat vs$type/dirlist` )
    rm vs$type/$dir/OUTDOCK vs$type/$dir/stderr vs$type/$dir/test.mol2.gz
end

# then resubmit 021c.run.vs.csh

