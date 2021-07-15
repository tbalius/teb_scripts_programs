
set list = `ls 006.rmsd_*/lig1.dat _min/006.rmsd_*/lig1.dat`

foreach file ($list) 

echo $file

awk 'BEGIN{min=1000;max = 0; sum = 0;count=0}{if(count!=0){sum=sum+$2;if($2>max){max = $2};if($2<min){min=$2}};count=count+1}END{printf"%6.2f %6.2f %6.2f\n", min,max,sum/count}' $file

tail -50001 $file | awk 'BEGIN{min=1000;max = 0; sum = 0;count=0}{if(count!=0){sum=sum+$2;if($2>max){max = $2};if($2<min){min=$2}};count=count+1}END{printf"%6.2f %6.2f %6.2f\n", min,max,sum/count}' 

end
