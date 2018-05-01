import os
import student_utils_sp18 as student 
import networkx as nx
from networkx.algorithms import approximation
import random
import numpy as np
import matplotlib.pyplot as plt
import utils
import tspsolver as tspsolver
import SetCoverPy as setcover

# Main method for algorithm
def run(list_of_kingdom_names, starting_kingdom, adjacency_matrix):

	number_kingdoms = len(list_of_kingdom_names)

	graph = student.adjacency_matrix_to_graph(adjacency_matrix)
	shortest = dict(nx.floyd_warshall(graph))

	s = set()

	dictionary = create_set(graph, number_kingdoms, adjacency_matrix)

	#path = [starting_kingdom]
	conquer = []

	vertex = list_of_kingdom_names.index(starting_kingdom)

	while len(s) != number_kingdoms:

		largest = 0
		next_vertex = None


		for key in dictionary:
			c = efficiency(graph, shortest, vertex, key, adjacency_matrix, s, dictionary, list_of_kingdom_names)

			if(c > largest):
				largest = c
				next_vertex = key


		just_conquer = dictionary.pop(next_vertex)

		s.update({list_of_kingdom_names[next_vertex]})

		for vert in just_conquer:

			s.update({list_of_kingdom_names[vert]})

		conquer.append(list_of_kingdom_names[next_vertex])

		# pathto_vert = nx.shortest_path(graph, vertex, next_vertex)
		# pathto_vert.pop(0)
		
		# for i in range(len(pathto_vert)):
		# 	pathto_vert[i] = list_of_kingdom_names[pathto_vert[i]]


		# path.extend(pathto_vert)

		vertex = next_vertex


	# pathto_start = nx.shortest_path(graph, vertex, list_of_kingdom_names.index(starting_kingdom))

	# for i in range(len(pathto_start)):

	# 	pathto_start[i] = list_of_kingdom_names[pathto_start[i]]

	# pathto_start.pop(0)
	# path.extend(pathto_start)

	conquering = []
	if(starting_kingdom in conquer):
		conquering.extend(conquer)
		conquering.append(starting_kingdom)
	else:
		conquering = [starting_kingdom]
		conquering.extend(conquer)
		conquering.append(starting_kingdom)


	adjacency_matrix_TSP = constructTSPmatrix(conquering, shortest, list_of_kingdom_names)
	TSP = student.adjacency_matrix_to_graph(adjacency_matrix_TSP)
	shortestTSP = dict(nx.floyd_warshall(TSP))

	tsp_path = tspsolver.solve_tsp(adjacency_matrix_TSP,3, tspsolver.pairs_by_dist, (0,len(conquering)-1))

	conquer_tsp_path = [conquering[point] for point in tsp_path]
	#print(conquer_tsp_path)


	new_conquered = run_2opt(tsp_path, adjacency_matrix_TSP, 0)
	conquer_tsp_path = [conquering[point] for point in new_conquered]
	#print(conquer_tsp_path)


	new_path = [starting_kingdom]

	v = list_of_kingdom_names.index(starting_kingdom)
	for i in range(len(conquer_tsp_path)):
		e = list_of_kingdom_names.index(conquer_tsp_path[i])
		p = nx.shortest_path(graph, v, e)

		p.pop(0)
		for j in range(len(p)):
			new_path.append(list_of_kingdom_names[p[j]])

		v = e

	#print(new_path)



	return new_path, conquer





# Creates a set for each node, a set consists of the node and its neighbors and is weighted by efficiency
def create_set(graph, number_kingdoms, adjacency_matrix):

	dictionary = {}

	for i in range(number_kingdoms):

		edges = []
		
		for u,v in graph.edges(i):

			edges.append(v)

		dictionary[i] = edges

	return dictionary

# Calculates a binary relationship matrix as well as cost vertex for use in set cover
def create_set_cover_matrix_cost(graph, number_kingdoms, adjacency_matrix):
	matrix = [[False for x in range(number_kingdoms)] for y in range(number_kingdoms)]
	costs = [adjacency_matrix[i][i] for i in range(number_kingdoms)]
	for i in range(number_kingdoms):
		for u, v in graph.edges(i):
			matrix[v][i] = True
	return [matrix, costs]

# Running SetCoverPy
def runSetCoverPy(inputs):
	a_matrix = inputs[0]
	cost = inputs[1]
	g = setcover.SetCover(a_matrix, cost)
	solution, time_used = g.SolveSCP()
	return [g.s, g.total_cost]

# Calculate the efficiency for use as weight of a set
def efficiency(graph, sp, start, end, adjacency_matrix, s, dictionary, list_of_kingdom_names):

	cost = sp[start][end] + adjacency_matrix[end][end]

	count = 0

	edges = dictionary[end]

	for v in edges:

		if(list_of_kingdom_names[v] not in s):
			count += 1

	return count / float(cost)

# Construct a graph to run TSP on given the results of our set cover decision
def constructTSPmatrix(conquered, shortest,list_of_kingdom_names):
	adjacency_matrix_TSP = [[0 for x in range(len(conquered))] for y in range(len(conquered))]
	for source in range(len(adjacency_matrix_TSP)):
		for destination in range(len(adjacency_matrix_TSP)):
			adjacency_matrix_TSP[source][destination] = shortest[list_of_kingdom_names.index(conquered[source])][list_of_kingdom_names.index(conquered[destination])]
	return adjacency_matrix_TSP

def route_distance(route, shortest, starting_index):

	distance = 0

	vertex = starting_index
	for i in range(len(route)):

		distance += shortest[vertex][route[i]]

	distance += shortest[route[len(route)-1]][starting_index]

	return distance

def swap_2opt(route, i, k):

	assert i >= 0 and i < (len(route) - 1)
	assert k > i and k < len(route)

	new_route = route[0:i]
	new_route.extend(reversed(route[i:k + 1]))
	new_route.extend(route[k+1:])

	assert len(new_route) == len(route)
	return new_route


def run_2opt(route, shortest, starting_index):
	"""
	improves an existing route using the 2-opt swap until no improved route is found
	best path found will differ depending of the start node of the list of nodes
		representing the input tour
	returns the best path found
	route - route to improve
	"""
	improvement = True
	b_route = route
	b_distance = route_distance(route, shortest,starting_index)
	while improvement: 

		improvement = False
		for i in range(len(b_route) - 1):
			for k in range(i+1, len(b_route)):
				new_route = swap_2opt(b_route, i, k)
				new_distance = route_distance(new_route, shortest,starting_index)
				if new_distance < b_distance:
					b_distance = new_distance
					b_route = new_route
					improvement = True
					break #improvement found, return to the top of the while loop
			if improvement:
				break
	assert len(b_route) == len(route)
	return b_route

