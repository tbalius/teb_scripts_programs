
## This script was written in 2020 by Trent Balius at FNLCR

ifh = open("tc_compare_two.txt",'r')

cluster = {}
is_it_in_a_cluster = {} # 
group_clusters = {} 

#cluster_count = 1
cluster_count = 0

cluster_threshold = 0.3

for line in ifh:
    #print (line)
    #splitline = line.replace('-',',').split(',')
    splitline = line.split(',')
    files = splitline[0].split('-')
    file1 = files[0]
    file2 = files[1]
    tc = float(splitline[1])

    if (1-tc)>cluster_threshold: 
        if not (file1 in is_it_in_a_cluster):
           is_it_in_a_cluster[file1] = 0
        if not (file2 in is_it_in_a_cluster):
           is_it_in_a_cluster[file2] = 0
        #print(line)
        continue
    #elif cluster_count == 111: 
    #     print (line)

    if not (file2 in cluster) and not (file1 in cluster):
       #if cluster_count == 111:
       #   print (group_clusters[cluster_count])
       cluster_count = cluster_count + 1
       print("start cluster %d"%cluster_count) 
       cluster[file1] = cluster_count
       cluster[file2] = cluster_count
       group_clusters[cluster_count] = []
       group_clusters[cluster_count].append(file1)
       group_clusters[cluster_count].append(file2)
       is_it_in_a_cluster[file1] = 1
       is_it_in_a_cluster[file2] = 1
       if cluster_count == 111:
          print("I am here 0", file1, file2, cluster[file1], cluster[file2],line)

    elif (file1 in cluster) and not (file2 in cluster): 
       if cluster_count == 111:
          print("I am here 1", file2, file1, cluster[file1])
       cluster[file2] = cluster[file1]
       num = cluster[file1]
       group_clusters[num].append(file2)
       is_it_in_a_cluster[file2] = 1
    elif (file2 in cluster) and not (file1 in cluster): 
       if cluster_count == 111:
          print("I am here 2", file1, file2, cluster[file2])
       cluster[file1] = cluster[file2]
       num = cluster[file1]
       group_clusters[num].append(file1)
       is_it_in_a_cluster[file1] = 1

    # else both are already assigned and skip

print(cluster_count)

fileprex = "cluster"

for key in group_clusters.keys():
    print(key, len(group_clusters[key]))
    filename = "%s_%d.txt"%(fileprex,key)
    ofh = open(filename,'w')
    for name in group_clusters[key]:
        ofh.write("%s\n"%name)
    ofh.close()

exit()

for key in cluster.keys():
    if cluster[key] == 1:
       print(key, cluster[key])
#exit()
for key in is_it_in_a_cluster.keys():
    if is_it_in_a_cluster[key] == 0: 
       print (key, is_it_in_a_cluster[key])

