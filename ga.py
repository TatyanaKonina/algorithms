
import numpy as np
import pandas as pd
import random
import math




# я написала сначала генетический, но он как то не очень хорошо работал, 
# поэтому я решила попробовать ant colony
class GA (object):
    def __init__(self, gen_num,population_size,mutate_rate):
        self.gen_num = gen_num
        self.population_size = population_size
        self.mutate_rate = mutate_rate

        self.data_cities = pd.read_table('./input/mona_1000.txt',sep=" ", header=None,skiprows = 1,names = [ 'city', 'x', 'y' ],)
        self.cities_num = self.data_cities.shape[0]
        self.cities = self.data_cities[['x', 'y']].values
        
        self.city_dict = { city: index for index, city in enumerate(self.data_cities['city']) }
        self.generation_history = []

    
    def greedy_init(self,cities):
        x, y = 0, 1
        visited = [False]*len(cities)
        i = 0
        dist = 0
        route = [i]

        while(sum(visited) < len(cities)):
            visited[i] = True
            min_distance = math.inf
            for j in range(len(cities)):
                if(visited[j] == False):

                    d = self.calc_two_pont_dist(cities[j], cities[i],cities)
                    if(d < min_distance):
                        min_distance = d
                        k = j
            i = k
            route.append(k)
            dist += min_distance
            visited[k] = True
        return np.array(route),dist


    def calc_two_pont_dist(self,index1,index2,cities):
        # calc dist for greedy init
        city1, city2 = self.cities[self.city_dict[index1]], self.cities[self.city_dict[ index2 ] ]
        distance = np.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) 
        return distance
    
    def create_initial_pop2(self,cities):
        # greedy init(onlu first tour,another are random)
        population = []
        tour,dist = self.greedy_init(cities.values.copy())
        population.append([dist,tour])
        start_index = 0
        tours = []
    
        for i in range(1, self.population_size):
            tour = cities.values.copy()
            np.random.shuffle(tour)
            tours.append(tour) 
        for tour in tours:
            population.append([self.calc_dis(tour), tour])
        population.sort(key=lambda x:x[0])
        return population

    def calc_dis(self,tour):
        # calc dist of the whole tour
        distance = 0.0
        for index, city_index in enumerate(tour):
            city1, city2 = self.cities[self.city_dict[city_index]], self.cities[self.city_dict[ tour[(index + 1) % len(tour)] ]]
            cost = 1
            distance += np.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) * cost
        return distance

    def run(self):
        # greedy init(onlu first tour,another are random)
        population = self.create_initial_pop2(cities = self.data_cities['city'])
        # only random
        # population = self.generate_population(cities = self.data_cities['city'])
        for _ in range(self.gen_num):
            population.sort(key=lambda x:x[0])
            parents = [ p[1] for p in population ]
            children = self.make_children(parents)
            population_children = []
            for child in children:
                population_children.append([self.calc_dis(child), child])
            population.extend(population_children)
            # population is list of [dist,[tour]],
            # so i sort population for dist and make new children only with best
            population.sort(key=lambda x:x[0])
            # slice population
            population = population[:self.population_size]
            # in sorted population last variant on the first place
            generation_best = population[0]
        print(generation_best)
        self.generation_history.append(generation_best)
        return self.generation_history[self.gen_num - 1]


    def generate_population(self, cities):
        #only random tours
        start_index = 0
        tours = []
        population = []
        for i in range(self.population_size):
            tour = cities.values.copy()
            np.random.shuffle(tour)
            tours.append(tour) 
        for tour in tours:
            population.append([self.calc_dis(tour), tour])
        population.sort(key=lambda x:x[0])
        return population



    def make_children(self,parents):
        children = []
        for i in range(0,len(parents),2):
            child = self.cross2(parents[i],parents[i+1])
            child = self.mutate(child)
            children.append(child)
        return children


    def cross(self,parent1,parent2):
        # first attempt to detect repeated cities
        pos=random.randrange(1,self.cities_num-1)
        child = np.r_[parent1[:pos] , parent2[pos:]]
        copy_child = child.tolist()
        count1=0
        for gen in copy_child[:pos]:
            if copy_child.count(gen) > 1:# repeated gen
                for i in range(len(parent2[:pos])):
                    if parent2[i] not in copy_child:
                        copy_child[count1] = parent2[i]
                        break
            count1+=1            		
        return child
    
    def mutate(self,child):
        # random mutation
        if self.mutate_rate > random.random():
            swap1, swap2 = random.sample( range(self.cities_num), k = 2)
            child[swap1], child[swap2] = child[swap2], child[swap1]
        return child

    def cross2(self,parent1,parent2):
        # random cross,choose two random parents
        start, end = random.sample( range(self.cities_num), k = 2 )
        if start > end:
            start, end = end, start
        sl = slice( start, end )
        # special func in numpy wich detect not unique cities fix it
        boolean = np.in1d( parent2, parent1[sl], invert = True )
        not_in_parent = parent2[boolean]
        # repeated cities fix it
        child = np.r_[ not_in_parent[:start], parent1[sl],  not_in_parent[start:] ]		
        return child


if __name__ == '__main__':
    test = GA(500,250,0.3)
    test.run()
