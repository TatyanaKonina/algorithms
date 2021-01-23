import math
from random import random,sample,randint

def read_data(n):
    return [input() for i in range(n)]

def form_lists(data):
    id_list,cords_list = [],[]
    for i in data:
        i = list(map(float,i.strip().split()))
        id_list.append(int(i[0]))
        cords_list.append(i[1:])
    return id_list,cords_list

def two_point_dist(point_one,point_two):
    x,y=0,1
    return pow(pow(point_one[x] - point_two[x],2) + pow(point_one[y] - point_two[y],2),0.5)

def calc_result_distance(route,cords_list):
    res_distance=0
    for i in range(1,len(route)):
        res_distance+=two_point_dist(cords_list[route[i]],cords_list[route[i-1]])
    return res_distance

def swap_two_opt(route,i,k):
    new_route = route[:i]
    new_route += reversed(route[i:k])
    new_route += route[k:]
    return new_route
       
def two_opt(route,distance):
    for i in range(len(route)):
        for k in range(i,len(route)):
            improved_route = swap_two_opt(route[:],i,k)
            new_distance = calc_result_distance(improved_route,cords_list)
            if new_distance<distance :
                distance=new_distance
                route=improved_route
    return route

def local_search(start_route, cords_list):
    res_distance = calc_result_distance(start_route,cords_list)
    return two_opt(start_route,res_distance)

def ILS(id_list,cords_list):
    start_route = sample([x for x in range(len(id_list))],len(id_list))
    route = local_search(start_route,cords_list)
    min_distance = calc_result_distance(route,cords_list)
    print("Distance after 2-Opt Approach:",min_distance)
    print(route)


id_list,cords_list = form_lists(read_data(52))

ILS(id_list,cords_list)

