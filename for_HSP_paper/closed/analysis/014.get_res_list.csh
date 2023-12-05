
 cat 014.footprint/rec_lig_com_seed_*/snapshot.*heatmap_matrix.*.log | awk '{if ($4=="self" || $4=="non_near" || $4 == "near") {print $1,$2}}' | sort | uniq -c | sort -nk1 > 014.resid_pairs.log

 cat 014.footprint/rec_lig_com_seed_*/snapshot.*heatmap_matrix.*.log | awk '{if ($4=="self" || $4=="non_near" || $4 == "near") {printf"%s\n%s\n",$1,$2}}' | sort | uniq -c | sort -nk1 > 014.resid.log

 #cat 014.resid.log | awk '{print $2}' | cut -c 4-6 | sort -n -u | awk 'BEGIN{old="1"}{if(old==$1){printf"%s ",$1}else if($1!=old+1){printf" %s ;;; %s ",old,$1}else{printf"."};old=$1}END{print""}'
 #cat 014.resid.log | awk '{print $2}' | cut -c 4-6 | sort -n -u | awk 'BEGIN{old="1";open="F"}{if(old==$1){printf"%s ",$1}else if($1!=old+1){if(open="T"){printf" %s ;;; ",old} printf" %s ",$1;open="F"}else{printf".";open="T"};old=$1;printf"%s",open}END{print""}'

 #cat 014.resid.log | awk '{print $2}' | cut -c 4-6 | sort -n -u | awk 'BEGIN{old="1";open="F"}{if(old==$1){printf"%s ",$1}else if($1!=old+1){if(open=="T"){printf" %s , ",old}else{printf","}; printf" %s ",$1;open="F"} else{if(open=="F"){printf"-"};open="T"};old=$1;}END{print""}' | sed -e 's/ //g'
 cat 014.resid.log | awk '{if ($1>68){if(substr($2, 1, 2)=="MG"){print " "$2}else{print $2}}}' | cut -c 4-8 | sort -n -u | awk 'BEGIN{old=-1;open="F"}{if(old==-1){old=$1}if(old==$1){printf"%s ",$1}else if($1!=old+1){if(open=="T"){printf" %s , ",old}else{printf","}; printf" %s ",$1;open="F"} else{if(open=="F"){printf"-"};open="T"};old=$1;}END{if(open=="T"){printf"%s\n",old}else{print "" }}' | sed -e 's/ //g'

 cat 014.resid_pairs.log |  awk '{if ($1>68){if(substr($2, 1, 2)=="MG"){print " "$2}else{print $2}}}' | grep -v "ATP" | grep -v "MG" | cut -c 4-8 | sort -n -u | awk 'BEGIN{old=-1;open="F"}{if(old==-1){old=$1}if(old==$1){printf"%s ",$1}else if($1!=old+1){if(open=="T"){printf" %s , ",old}else{printf","}; printf" %s ",$1;open="F"} else{if(open=="F"){printf"-"};open="T"};old=$1;}END{if(open=="T"){printf"%s\n",old}else{print "" }}' | sed -e 's/ //g'

 cat 014.resid_pairs.log |  awk '{if ($1>68){if(substr($3, 1, 2)=="MG"){print " "$3}else{print $3}}}' | grep -v "ATP" | grep -v "MG" | cut -c 4-8 | sort -n -u | awk 'BEGIN{old=-1;open="F"}{if(old==-1){old=$1}if(old==$1){printf"%s ",$1}else if($1!=old+1){if(open=="T"){printf" %s , ",old}else{printf","}; printf" %s ",$1;open="F"} else{if(open=="F"){printf"-"};open="T"};old=$1;}END{if(open=="T"){printf"%s\n",old}else{print "" }}' | sed -e 's/ //g'
