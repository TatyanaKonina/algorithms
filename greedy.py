from data import form_lists,two_point_dist,read_data

def greedy_algorithm(cords_list):
	best_route = []
	best_length = float('inf')

	for i_start, start in enumerate(cords_list):
		route = [i_start]
		length = 0

		i_next, next, dist = get_closest(start, cords_list, route)
		length += dist
		route.append(i_next)

		while len(route) < len(cords_list):
			i_next, next, dist = get_closest(next, cords_list, route)
			length += dist
			route.append(i_next)


		if length < best_length:
			best_length = length
			best_route = route
	return best_route, best_length

def get_closest(city, cords_list, visited):
	best_distance = float('inf')

	for i, c in enumerate(cords_list):

		if i not in visited:
			distance = two_point_dist(city, c)

			if distance < best_distance:
				closest_city = c
				i_closest_city = i
				best_distance = distance

	return i_closest_city, closest_city, best_distance



# id_list,cords_list = form_lists(read_data(52))

# best_order,best_len = algorithm(cords_list)
# print(best_order,best_len)