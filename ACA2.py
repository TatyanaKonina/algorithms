import math
import random


# там есть скриншотики в ветке

class ACA():
    def __init__(self,max_iters,ants_num,pheromone_intensity,pheromone_importance,distance_priority,speed_evaporation):
        self.max_iters = max_iters
        self.ants_num = ants_num
        self.pheromone_importance = pheromone_importance #alpha
        self.distance_priority = distance_priority #beta
        self.pheromone_intensity = pheromone_intensity # q
        self.speed_evaporation = speed_evaporation #rho
        
        self.dist_matrix,self.cities_num = self.read_data('./input/mona_1000.txt')
        # matrix where pheromone is 1 / cities_num ** 2
        self.pheromone_matrix = [[1 / (self.cities_num * self.cities_num) for j in range(self.cities_num)] for i in range(self.cities_num)]
        self.ants = []
        # self.curr_index = 0
        
        self.best_dist = math.inf
        self.best_route = []

        self.probabilities = [0 for i in range(self.cities_num)]
        
    def calc_dis(self,city1,city2):
        return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)
    
    def read_data(self,path):
        cities = []
        cost_matrix = []
        with open(path) as f:
            f.readline()
            for line in f.readlines():
                city = line.split(' ')
                cities.append(dict(index=int(city[0]), x=int(city[1]), y=int(city[2])))
        for i in range(len(cities)):
            row = []
            for j in range(len(cities)):
                row.append(self.calc_dis(cities[i],cities[j]))
            cost_matrix.append(row)
        return cost_matrix,len(cities)
    
    def run(self):
        for i in range(self.max_iters):
            # init ants
            self.ants = [Ant(self.cities_num,self.dist_matrix) for i in range(self.ants_num)]
            for ant in self.ants:
                # for each ant
                for _ in range(self.cities_num-1):
                    ind = self.select_next(ant)
                    ant.calc_path_dist(ind)
                ant.path_dist += self.dist_matrix[ant.visited[len(ant.visited) - 1]][ant.visited[0]]
                self.update_best(ant)
                self.update_pheromone_for_ant(ant)
            # update pheromone matrix
            for k in range(self.cities_num):
                for j in range(self.cities_num):
                    self.pheromone_matrix[k][j] *= self.speed_evaporation
                    for ant in self.ants:
                        self.pheromone_matrix[k][j] += ant.pheromone_ant_path[k][j]
            print(' #{}, best cost: {}, path: {}'.format(i, self.best_dist, self.best_route))
    
    def update_pheromone_for_ant(self,ant):
        ant.clear()
        # update pheromone intense for ant
        for i in range(1,len(ant.visited)):
            ant.pheromone_ant_path[ant.visited[i - 1]][ant.visited[i]] = self.pheromone_intensity / self.dist_matrix[ant.visited[i - 1]][ant.visited[i]]

    def update_best(self,ant):
        if ant.path_dist < self.best_dist:
            self.best_dist = ant.path_dist
            self.best_route = [] + ant.visited
            
    def select_next(self,ant):
        # 
        pheromone = 0.0
        for i in ant.not_visited:
            # calc pheromone intense 
            try:
                pheromone += pow(self.pheromone_matrix[ant.curr_city][i],self.pheromone_importance) * pow(1.0 / self.dist_matrix[ant.curr_city][i],self.distance_priority)
            except:
                pheromone +=0
        for i in range(self.cities_num):
            # clear probabilities
            self.probabilities[i] = 0

        for i in range(self.cities_num):
            # fill probabilities based on pheromone
            if (i in ant.not_visited):
                try:
                    self.probabilities[i] = ((pow(self.pheromone_matrix[ant.curr_city][i],self.pheromone_importance) * pow(1.0 / self.dist_matrix[ant.curr_city][i],self.distance_priority) ) / pheromone)
                except:
                    pass
        rand = random.random()
        # random roulette for probabilities 
        for i in range(self.cities_num):
            rand -= self.probabilities[i]
            if rand <=0:
                return i


class Ant():
    # each ant has vitited cities, not visited, and own pheromone path
    def __init__(self,cities_num,dist_matrix):
        self.path_dist = 0.0
        self.cities_num = cities_num
        self.dist_matrix = dist_matrix
        self.not_visited = [ i for i in range(cities_num)]
        self.curr_city = random.randint(0, cities_num - 1)
        self.not_visited.remove(self.curr_city)
        self.visited = []
        self.visited.append(self.curr_city)
        self.pheromone_ant_path = []
    
    def calc_path_dist(self,index):
        # here ant do one step to the index city and we update path dist 
        self.not_visited.remove(index)
        self.visited.append(index)
        self.path_dist += self.dist_matrix[self.curr_city][index]
        self.curr_city = index
    
    def clear(self):

        self.pheromone_ant_path = [[0.0 for j in range(self.cities_num)] for i in range(self.cities_num)]


if __name__ == '__main__':
    aco = ACA(pheromone_importance=1.0,distance_priority=10,max_iters=100,ants_num=10,pheromone_intensity=10,speed_evaporation=0.5)
    aco.run()

