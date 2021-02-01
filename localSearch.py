import math

from data import form_lists,two_point_dist,read_data
from nearest_neighour import nearest_neighbour
import copy

def calc_result_distance(route,cords_list):
    res_distance=0
    for i in range(1,len(route)):
        res_distance+=two_point_dist(cords_list[route[i]],cords_list[route[i-1]])
    res_distance += two_point_dist(cords_list[route[0]],cords_list[route[len(route) -1]])
    return res_distance
def two_opt(route,distance,max_attempts):
    for i in range(max_attempts):
        for k in range(i + 1,max_attempts):
            improved_route = route[:i] + route[i:k][::-1] + route[k:]
            new_distance = calc_result_distance(improved_route,cords_list)
            if new_distance<distance :
                distance=new_distance
                route=improved_route
    return route,new_distance

def do_pertubation(route):
    new_route = route[:]
    i=randint(0,len(route)-1)//4
    j=i+randint(0,len(route)-1)//4
    k=j+randint(0,len(route)-1)//4
    return route[:i]+route[k:] + route[j:k]+route[i:j]

def local_search(start_route, cords_list,max_attempts):
    res_distance = calc_result_distance(start_route,cords_list)
    return two_opt(start_route,res_distance,max_attempts)

def ILS(id_list,cords_list,max_attempts,max_itter):
    start_route,dist = nearest_neighbour(cords_list,lines)
    route,min_distance = local_search(start_route,cords_list,max_attempts)
    for i in range(max_itter):
        new_route = do_pertubation(route)
        new_route,new_distance=local_search(new_route,cords_list,max_attempts)    
        if(new_distance<min_distance):
            min_distance=new_distance
            route=new_route    
    return route
        
lines = 703
max_attempts = 703
max_itter = 10
id_list,cords_list = form_lists(read_data(lines)) 
route = ILS(id_list,cords_list,max_attempts,max_itter)




