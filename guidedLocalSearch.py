from data import *
from random import sample
from localSearch import calc_result_distance
import copy
from nearest_neighour import nearest_neighbour

def update_penalty(penalty, city_tour, utilities):
    max_utility = max(utilities)   
    for i in range(0, len(city_tour) - 1):
        c1 = city_tour[i]
        c2 = city_tour[i + 1]                
        if (utilities[i] == max_utility):
            penalty[c1][c2] = penalty[c1][c2] + 1   
    return penalty

def utility (cords_list, city_tour, penalty, limit = 1):
    utilities = [0 for i in city_tour]
    for i in range(0, len(city_tour) - 1):
        c1 = city_tour[i]
        c2 = city_tour[i + 1]                 
        utilities[i] = two_point_dist(cords_list[c1],cords_list[c2]) /(1 + penalty[c1][c2])  
    return utilities

def stochastic_2_opt(cords_list,route,distance,penalty, limit):
    for i in range(max_attempts):
        for k in range(i + 1,max_attempts):
            improved_route = route[:i] + route[i:k][::-1] + route[k:]
            new_distance = augumented_cost(cords_list,improved_route,penalty, limit)
            if new_distance<distance :
                distance=new_distance
                route=improved_route
    return route,new_distance



def augumented_cost(cord_list, city_tour, penalty, limit):
    augmented = 0   
    for i in range(0, len(city_tour) - 1):
        c1 = city_tour[i]
        c2 = city_tour[i + 1]                  
        augmented = augmented + two_point_dist(cords_list[c1],cord_list[c2]) + (limit * penalty[c1][c2])    
    return augmented

def local_search(cords_list,city_tour, penalty, max_attempts = 50, limit= 1):
    count = 0
    ag_cost = augumented_cost(cords_list,city_tour = city_tour, penalty = penalty, limit = limit)
    solution = copy.deepcopy(city_tour) 
    while (count < max_attempts):
        candidate,candidate_augmented = stochastic_2_opt(cords_list,solution,ag_cost,penalty, limit)
        if candidate_augmented < ag_cost:
            solution  = copy.deepcopy(candidate)
            ag_cost = augumented_cost(cords_list, city_tour = solution, penalty = penalty, limit = limit)
            count = 0
        else:
            count = count + 1                             
    return solution

def guided_search(cords_list,city_tour,alpha = 0.3, local_search_optima = 1000, max_attempts = 20, iterations = 500):
    count = 0
    limit = alpha * (local_search_optima / len(city_tour))  
    penalty = [[0 for i in city_tour] for j in city_tour]
    solution = copy.deepcopy(city_tour)
    best_solution = []
    while (count < iterations):
        solution = local_search(cords_list,city_tour = solution, penalty = penalty, max_attempts = max_attempts, limit = limit)
        utilities = utility(cords_list, city_tour = solution, penalty = penalty, limit = limit)
        penalty = update_penalty(penalty = penalty, city_tour = solution, utilities = utilities)
        if (calc_result_distance(solution,cords_list) < calc_result_distance( best_solution,cords_list) or  not(best_solution)):
            best_solution = copy.deepcopy(solution) 
        count = count + 1
        print("Iteration = ", count, " Distance ", calc_result_distance( best_solution,cords_list))
    return best_solution


id_list,cords_list = form_lists(read_data(703))
start_route,dist = nearest_neighbour(cords_list,1000)


route = guided_search(cords_list,city_tour = start_route, alpha = 0.1, local_search_optima = 1000, max_attempts = 10, iterations = 1000)
lis1 = [ x+ 1 for x in route]
print(" ".join(map(str, lis1)))