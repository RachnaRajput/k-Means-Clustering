import sys
import json
import math
from numpy.matrixlib.defmatrix import matrix
from itertools import *
from collections import defaultdict


def kmeans_algo(json_data, number_of_cluster):
 list_array = json_data
 if len(list_array)==1:  #if the length of the json data is 1. then print the tuple of the point and cluster will be 0.
        print tuple(list_array)
        print 0
        sys.exit()
 else:       #if length of the json array is greater than 1. apply the complete kmean algorithm.
    euclidean_matrix = distance_formula(list_array)      #saving the distance between each and evry 2 point in the matrix.
    first_max =  find_first_centroid(list_array,number_of_cluster, euclidean_matrix)
    index_list = []
    index_list.append(first_max[0])
    centroid_row = []
    centroid_row = first_max[1]
    other_max = find_other_centroids(euclidean_matrix,index_list,number_of_cluster,list_array)
    cluster_points = []
    for i in range(len(index_list)):
        cluster_points.append(i+1)
    centroid_value = []
    for i in range (len(list_array)):
        for j in range(len(index_list)):
            if i == index_list[j]:
                centroid_value.append(list_array[i])
    duplicate_list = []
    final_cluster_iteration = iteration_function(euclidean_matrix, centroid_value,duplicate_list, cluster_points,list_array)
    cluster = finding_cluster(final_cluster_iteration,list_array)
    return cluster

distance_list = []
def distance_formula(list_array): #-------------------------> find the distance between the points.
    columns = [i for i in list_array]
    rows = [j for j in list_array]
    A =  [[0.00 for x in range(len(columns))] for x in range(len(rows))]
    for k in range (len(list_array)):
       for i in range (k+1,len(list_array)):
        distance = [pow((point1-point2),2) for (point1,point2) in zip(list_array[k],list_array[i])]
        final_distance =  math.sqrt(sum(distance))
        A[k][i] = final_distance
        A[i][k] = final_distance
    # print A
    return A

def find_first_centroid(list_array,number_of_cluster, euclidean_matrix):   #------------> finding the first centroid which is list_array[0]
    centroid = list_array[0]
    for centroid_index in range(len(list_array)):
        if centroid == list_array[centroid_index]:
            # max_distance = max(euclidean_matrix[centroid_index])
            return centroid_index,euclidean_matrix[centroid_index]

def find_other_centroids( euclidean_matrix,index_list,number_of_cluster,list_array):  #---------------> finding the other centroids.
    index_list1 =[]
    if len(index_list)<number_of_cluster:
        centroid_row1 = []
        for item1 in index_list:
            centroid_row1.append(euclidean_matrix[item1])
        max_of_min_list = []
        for item in izip_longest(*centroid_row1):
            min_item = min(item)
            max_of_min_list.append(min_item)
        max_item = max(max_of_min_list)
        for i in range(len(max_of_min_list)):
            if max_item == max_of_min_list[i]:
                index_list.append(i)
        find_other_centroids(euclidean_matrix,index_list,number_of_cluster,list_array)

def iteration_function(euclidean_matrix, centroid_value, duplicate_list,cluster_points,list_array): #---------------> iteration for finding the clusters.
    col = len(centroid_value)
    row = len(list_array)
    Distance_matrix = matrix( [[None for x in range(col)] for x in range(row)])
    final_distance_list = []
    for k in range (len(list_array)):
       for i in range (len(centroid_value)):
        distance = [pow((point1-point2),2) for (point1,point2) in zip(list_array[k],centroid_value[i])]   # finding the distance between the center and other points.
        final_distance = math.sqrt(sum(distance))
        Distance_matrix[k,i] = final_distance
        final_distance_list.append(final_distance)
    # min_val =  Distance_matrix.min(1)
    cluster_number_list = []
    for i in range(row):
        mini = float("inf")
        for j in range(col):
            if Distance_matrix[i,j]<= mini:
                mini = Distance_matrix[i,j]
                variable = j+1
        cluster_number_list.append(variable)   # finding the cluster number for each point where point should fall.

    dict = {}
    for length in range(len(list_array)):
        dict[length] = list_array[length]


    mylist = []
    for length2 in range(len(centroid_value)):
        newllist = []
        for length1 in range(len(cluster_number_list)):
                 if cluster_number_list[length1]== length2+1:
                     newllist.append(length1)
        mylist.append(newllist)
    finalmean = []
    for item in (mylist):
        combine_list = []
        for item1 in range(len(item)):
            for key,value in dict.iteritems():
                if key == item[item1]:
                    combine_list.append(value)
        mymean=[]
        for i in izip_longest(*combine_list):
            sum_element = 0.00
            for item in i:
                sum_element = sum_element+item
                mean = float(sum_element)/len(i)   # finding the mean distance for all the points of one cluster.
            mymean.append(mean)
        finalmean.append(mymean)    # forming the list of the new mean distance.
    if duplicate_list != cluster_number_list: #stoping condition of the iteration .i.e cluster number in new list should not match with the previous list.
        return iteration_function(euclidean_matrix, finalmean, cluster_number_list, cluster_points,list_array)   #recursively calling the interation fuction.
    else:
        return cluster_number_list   #when new list of the iteration is equale to the previous list. then that list is the final cluster number list.

def finding_cluster(final_cluster_iteration,list_array):  #------------> finding the clusters.
    dict = {}
    sum_dist = []
    output_list = []
    for size in range(len(final_cluster_iteration)):
        dict[size]=final_cluster_iteration[size]
    new_dict = defaultdict(list)
    for key,value in dict.iteritems():
        new_dict[value].append(key)
    for i in new_dict:
        newly_list = []
        new_dist = []
        cluster_list = []

        for j in new_dict[i]:
            newly_list.append(list_array[j])
            cluster_list.append(tuple(list_array[j]))   #converting the list of the point od each cluster in tuple.
            cluster_list.sort()
        output_list.append(cluster_list)
        for k in range(len(newly_list)):
            for i in range (len(newly_list)):
             dist = [pow((point1-point2),2) for (point1,point2) in zip(newly_list[k],newly_list[i])] # finding the distance between the point in each cluster.
             final_dist =  math.sqrt(sum(dist))
             new_dist.append(final_dist)
        sum_dist.append(max(new_dist)) # finding the max distance (cohesion value) form each cluster.
        cohesion = sum(sum_dist)/len(sum_dist)  # finding the final cohesion by taking the average of the largest diameter of each cluster.
    ordered_list = sorted(output_list,key=len)  #sorting the list for the output.
    return ordered_list,cohesion

def main(var,ksize): #---------------------------------> Runs either kmeans program or findkstar program.
    if var == True:                        #-------------> Runs kmeans program.
        datalist = []
        with open(sys.argv[1]) as json_file: #Accessing the json data.
          for line in json_file:
              datalist.append(json.loads(line))
          datalist = tuple(datalist)
          # print len(datalist),
        ksize = int(sys.argv[2])
        if ksize >len(datalist):
            ksize = len(datalist)
            # print ksize
        answer = kmeans_algo(datalist, ksize)
        for j in answer[0]:
            print j
        print answer[1]
    else:                                #------------> Runs findkstar program.
          datalist = []
          with open(sys.argv[1]) as json_file: #Accessing the json data.
           for line in json_file:
              datalist.append(json.loads(line))
           number_of_cluster= ksize
           cohesion =  kmeans_algo(datalist, number_of_cluster)
           return cohesion[1]




if __name__ == "__main__":main(True,0)

