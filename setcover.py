import os
import student_utils_sp18 as student 
import networkx as nx
from networkx.algorithms import approximation
import random
import numpy as np
import matplotlib.pyplot as plt
import utils


def run(list_of_kingdom_names, starting_kingdom, adjacency_matrix):

	number_kingdoms = len(list_of_kingdom_names)

	graph = student.adjacency_matrix_to_graph(adjacency_matrix)
	shortest = dict(nx.floyd_warshall(graph))

	s = set()

	dictionary = create_set(graph, number_kingdoms, adjacency_matrix)

	path = [starting_kingdom]
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

		pathto_vert = nx.shortest_path(graph, vertex, next_vertex)
		pathto_vert.pop(0)
		
		for i in range(len(pathto_vert)):
			pathto_vert[i] = list_of_kingdom_names[pathto_vert[i]]


		path.extend(pathto_vert)

		vertex = next_vertex


	pathto_start = nx.shortest_path(graph, vertex, list_of_kingdom_names.index(starting_kingdom))

	for i in range(len(pathto_start)):

		pathto_start[i] = list_of_kingdom_names[pathto_start[i]]

	pathto_start.pop(0)
	path.extend(pathto_start)	


	return path, conquer



def create_set(graph, number_kingdoms, adjacency_matrix):

	dictionary = {}

	for i in range(number_kingdoms):

		edges = []
		
		for u,v in graph.edges(i):

			edges.append(v)

		dictionary[i] = edges

	return dictionary


def efficiency(graph, sp, start, end, adjacency_matrix, s, dictionary, list_of_kingdom_names):

	cost = sp[start][end] + adjacency_matrix[end][end]

	count = 0

	edges = dictionary[end]

	for v in edges:

		if(list_of_kingdom_names[v] not in s):
			count += 1

	return count / float(cost)




