
 #set seed = 0
 #set seed = 5
  set seed = 50

 #grep -A1 ENERGY 008_mmgbsa/full_no_restaint_0/mmgbsa_cal_lig.out | grep -v ENERGY | grep -v "\-\-" | awk 'BEGIN{max=-1000;min=1000;sum=0.0;count=0}{printf "%f\n", $2; sum=sum+$2; count=count+1;if(max<$2){max=$2};if(min>$2){min=$2}}END{printf "max=%f\nmin=%f\navg=%f\n", max,min,sum/count}'

 #grep -A1 ENERGY 008_mmgbsa/full_no_restaint_0/mmgbsa_cal_rec.out | grep -v ENERGY | grep -v "\-\-" | awk 'BEGIN{max=-1000;min=1000;sum=0.0;count=0}{printf "%f\n", $2; sum=sum+$2; count=count+1;if(max<$2){max=$2};if(min>$2){min=$2}}END{printf "max=%f\nmin=%f\navg=%f\n", max,min,sum/count}'

 #grep -A1 ENERGY 008_mmgbsa/full_no_restaint_0/mmgbsa_cal_com.out | grep -v ENERGY | grep -v "\-\-" | awk 'BEGIN{max=-1000;min=1000;sum=0.0;count=0}{printf "%f\n", $2; sum=sum+$2; count=count+1;if(max<$2){max=$2};if(min>$2){min=$2}}END{printf "max=%f\nmin=%f\navg=%f\n", max,min,sum/count}'

 grep -A1 ENERGY 008_mmgbsa/full_${seed}/mmgbsa_cal_lig.out | grep -v ENERGY | grep -v "\-\-" | awk 'BEGIN{max=-10000;min=10000;sum=0.0;count=0}{sum=sum+$2; count=count+1;if(max<$2){max=$2};if(min>$2){min=$2}}END{printf "max=%f\nmin=%f\navg=%f\n", max,min,sum/count}'

 grep -A1 ENERGY 008_mmgbsa/full_${seed}/mmgbsa_cal_rec.out | grep -v ENERGY | grep -v "\-\-" | awk 'BEGIN{max=-10000;min=10000;sum=0.0;count=0}{sum=sum+$2; count=count+1;if(max<$2){max=$2};if(min>$2){min=$2}}END{printf "max=%f\nmin=%f\navg=%f\n", max,min,sum/count}'

 grep -A1 ENERGY 008_mmgbsa/full_${seed}/mmgbsa_cal_com.out | grep -v ENERGY | grep -v "\-\-" | awk 'BEGIN{max=-10000;min=10000;sum=0.0;count=0}{sum=sum+$2; count=count+1;if(max<$2){max=$2};if(min>$2){min=$2}}END{printf "max=%f\nmin=%f\navg=%f\n", max,min,sum/count}'

