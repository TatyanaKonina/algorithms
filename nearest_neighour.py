from data import two_point_dist

def nearest_neighbour(cords_list,lines):
    x, y = 0, 1

    visited = [False]*len(cords_list)
    i = 1
    dist = 0
    route = [i]

    while(sum(visited) < lines):
        visited[i] = True
        min_distance = math.inf
        for j in range(len(cords_list)):
            if(visited[j] == False):
                d = two_point_dist(cords_list[j], cords_list[i])
                if(d < min_distance):
                    min_distance = d
                    k = j
        i = k
        route.append(k)
        dist += min_distance
        visited[k] = True
    return route, dist
