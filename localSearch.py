import math
from random import random,sample,randint
from greedy import greedy_algorithm
from data import form_lists,two_point_dist,read_data


def calc_result_distance(route,cords_list):
    res_distance=0
    for i in range(1,len(route)):
        res_distance+=two_point_dist(cords_list[route[i]],cords_list[route[i-1]])
    return res_distance


def two_opt(route,distance):
    for i in range(len(route)):
        for k in range(i,len(route)):
            improved_route = route[:i] + route[i:k][::-1] + route[k:]
            new_distance = calc_result_distance(improved_route,cords_list)
            if new_distance<distance :
                distance=new_distance
                route=improved_route
    return route

def do_pertubation(route):
    new_route = route[:]
    i=randint(0,len(route)-1)//4
    j=i+randint(0,len(route)-1)//4
    k=j+randint(0,len(route)-1)//4
    return route[:i]+route[k:] + route[j:k]+route[i:j]

def local_search(start_route, cords_list):
    res_distance = calc_result_distance(start_route,cords_list)
    return two_opt(start_route,res_distance)

def ILS(id_list,cords_list):
    start_route,dist = greedy_algorithm(cords_list)
    # start_route = sample([x for x in range(len(id_list))],len(id_list))
    # print(start_route,dist)
    
    route = local_search(start_route,cords_list)
    min_distance = calc_result_distance(route,cords_list)
    print("Distance after 2-Opt Approach:",min_distance)
    print(route,len(route))
    for i in range(len(route)):
        new_route = do_pertubation(route)
        new_route=local_search(new_route,cords_list)    
        new_distance=calc_result_distance(new_route,cords_list)
        if(new_distance<min_distance):
            min_distance=new_distance
            route=new_route    
    print("Distance after Iterated 2-Opt Approach:",min_distance)
    print(route)
    return route
        


id_list,cords_list = form_lists(read_data(52))

ILS(id_list,cords_list)

