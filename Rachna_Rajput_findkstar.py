import sys
import json
import Rachna_Rajput_kmeans


def findkstar_algo(dataitem,theta,cohesion_dict,k):
  if k > len(dataitem):       #if k is greater than the size of the json data. then the best k will be the length of the json data.
               print len(dataitem)
               sys.exit()
  else:                      #if k is less than the length of the json data. then we will apply the cohesion formula
   coh = Rachna_Rajput_kmeans.main(False,k)
   cohesion_dict[k]=coh
   key =  k
   formula = (cohesion_dict[key/2]-cohesion_dict[key])/(cohesion_dict[key/2]*(key/2))
   # print "formula_list: ",formula_list   #list 'formula' s containing the calculation of the cohesion formula for different values of the k.
   if formula>theta:                    #comparing the value of the formula with given value of theta.
       formula_list.append(formula)
       findkstar_algo(dataitem,theta,cohesion_dict,k+k)  # Recursively calling findkstar algo to find cohesion of k = 4,8,etc
   else:                                                 # else part will be active when formula value is less than the theta.
       formula_list.append(formula)
       number = k
       focus_point= formula_list[len(formula_list)-2]     # focus point is the cohesion value of the root; root=> from where binary search is going to start.
       v = number/2
       v_by_2 = number/4
       if (len(formula_list))==1:               #when the formula list have only 1 cohesion value. then k is either 1 or 0. so value of cluster is 1.
           print 1
       else:
           Binary_Search(focus_point,v_by_2,v)   #when length of the formula list is greater than 1, then we will call the binary search function.

def Binary_Search(focus_point,v_by_2,v):   #-------------------> Binary search.
       for i in range(len(formula_list)):
               midpoint = (v+v_by_2)/2
               c = Rachna_Rajput_kmeans.main(False,midpoint)
               cohesion_dict[midpoint]= c    #adding the cohesion value of the midpoint in the dictionary.
               if focus_point>theta:        #if focus point is greater than the theta, then search in the right part.
                   formula_for_right_side = (abs(cohesion_dict[midpoint]-cohesion_dict[v]))/(cohesion_dict[midpoint]*(abs(midpoint-v))) #applying calculation formula.
                   if v-midpoint!=1:       #stoping condition for the recusive call of the binary tree.
                       if formula_for_right_side > theta:    # if right side focus value is greater than theta. then go deep in the right side of the tree.
                           Binary_Search(formula_for_right_side,midpoint,v)  # calling the binary function for the right value.
                           break
                   if cohesion_dict[v]<cohesion_dict[midpoint]:  #if latest cohesion value is less than the midpoint's cohesion; then output latest point.
                       print v
                       break
                   else:
                       if midpoint ==0:
                           print 1
                       else:
                           print midpoint


               else:   #searching in the left side of the tree.
                   formula_for_left_side = (abs(cohesion_dict[v_by_2]-cohesion_dict[midpoint]))/(cohesion_dict[v_by_2]*(abs(midpoint-v_by_2)))
                   if midpoint-v_by_2!=1:   #stoping point for the recusive call of the binary search function.
                       if formula_for_left_side < theta:
                           Binary_Search(formula_for_left_side,v_by_2,midpoint)
                   if cohesion_dict[v_by_2]>cohesion_dict[midpoint]:  #if value of v/2 is greater then the mid point cohesion value. then print v/2
                       if v_by_2==0:
                           print 1
                       else:
                           print v_by_2
                   else:
                       print midpoint


if __name__=="__main__":
    dataitem = []
    formula_list = []
    with open(sys.argv[1]) as json_file: #Accessing the json data.
          for line in json_file:
              dataitem.append(json.loads(line))
    theta = float(sys.argv[2])
    coh = Rachna_Rajput_kmeans.main(False,1)
    cohesion_dict = {}
    cohesion_dict[1]= coh
    k=2
    findkstar_algo(dataitem,theta,cohesion_dict,k)

#
# [5.1,3.5,1.4,0.2,1.6]
# [4.9,3.0,1.4,0.2,1.0]
# [4.7,3.2,1.3,0.2,1.0]
# [4.6,3.1,1.5,0.2,1.0]
# [5.0,3.6,1.4,0.2,1.2]
# [7.0,3.2,4.7,1.4,1.0]
# [6.4,3.2,4.5,1.5,1.3]
# [6.9,3.1,4.9,1.5,1.0]
# [5.5,2.3,4.0,1.3,1.0]
# [6.5,2.8,4.6,1.5,1.4]
# [6.3,3.3,6.0,2.5,2.0]
# [5.8,2.7,5.1,1.9,1.0]
# [7.1,3.0,5.9,2.1,1.0]
# [6.5,3.0,5.8,2.2,1.5]
# [7.6,3.0,6.6,2.1,1.0]
# [4.9,2.5,4.5,1.7,1.7]

# [5.1,3.5,1.4,0.2]
# [4.9,3.0,1.4,0.2]
# [4.7,3.2,1.3,0.2]
# [4.6,3.1,1.5,0.2]
# [5.0,3.6,1.4,0.2]
# [7.0,3.2,4.7,1.4]
# [6.4,3.2,4.5,1.5]
# [6.9,3.1,4.9,1.5]
# [5.5,2.3,4.0,1.3]
# [6.5,2.8,4.6,1.5]
# [6.3,3.3,6.0,2.5]
# [5.8,2.7,5.1,1.9]
# [7.1,3.0,5.9,2.1]
# [6.5,3.0,5.8,2.2]
# [7.6,3.0,6.6,2.1]
# [4.9,2.5,4.5,1.7]
#
