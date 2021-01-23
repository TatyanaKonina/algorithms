def read_data(n):
    return [input() for i in range(n)]

def form_lists(data):
    id_list,cords_list = [],[]
    for i in data:
        i = list(map(float,i.strip().split()))
        id_list.append(int(i[0]))
        cords_list.append((i[1:]))
    return id_list,cords_list

def two_point_dist(point_one,point_two):
    x,y=0,1
    return pow(pow(point_one[x] - point_two[x],2) + pow(point_one[y] - point_two[y],2),0.5)