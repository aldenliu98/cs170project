import student_utils_sp18 as student 
import networkx as nx
from networkx.algorithms import approximation
import random
import numpy as np
import matplotlib.pyplot as plt
import utils

def efficiency_ratio(g, s, e, shortest_path, hashset, list_of_kingdom_names, adjacency_matrix):
	
	cost = shortest_path[s][e] + adjacency_matrix[e][e]

	count = 0

	for a, b in graph.edges(e):

		if(list_of_kingdom_names[b] not in hashset):
			count += 1

	return count / float(cost)



for i in range(1,753):

	input_file_number = "inputs/"+str(i)+".in"
	#f = open(input_file_number, "r")

	try: 
		input_data = utils.read_file(input_file_number)
		number_of_kingdoms, list_of_kingdom_names, starting_kingdom, adjacency_matrix = student.data_parser(input_data)

		try:
			graph = student.adjacency_matrix_to_graph(adjacency_matrix)
			shortest = dict(nx.floyd_warshall(graph))

			s = set()

			final = [starting_kingdom]
			line2 = [starting_kingdom]

			vertex = list_of_kingdom_names.index(starting_kingdom)
			s.update({starting_kingdom})

			for u,v in graph.edges(vertex):
				s.update({list_of_kingdom_names[v]})


			while len(s) != number_of_kingdoms:
				

				mincost = 0
				vertex_to_add = None
				count = 0
				for u, v in graph.edges(vertex):

					if(list_of_kingdom_names[v] not in s):

						count += 1
						c = efficiency_ratio(graph, u, v, shortest, s, list_of_kingdom_names, adjacency_matrix)

						if(c > mincost):
							mincost = c
							vertex_to_add = v



				if count == 0:
					
					for name in s:

						point = list_of_kingdom_names.index(name)

						for u, v in graph.edges(point):

							c = efficiency_ratio(graph, u, v, shortest, s, list_of_kingdom_names, adjacency_matrix)

							if(c > mincost):
								mincost = c
								vertex_to_add = v


				if(count == 0):
					path = nx.shortest_path(graph, vertex, vertex_to_add)
					path.pop(0)

					for i in range(len(path)):
						path[i] = list_of_kingdom_names[path[i]]

					final.extend(path)
				else:

					final.append(list_of_kingdom_names[vertex_to_add])

				s.update({list_of_kingdom_names[vertex_to_add]})
				line2.append(list_of_kingdom_names[vertex_to_add])

				for u, v in graph.edges(vertex_to_add):
					s.update({list_of_kingdom_names[v]})

				
				vertex = vertex_to_add


			path = nx.shortest_path(graph, vertex, 0)
			path.pop(0)
			final.extend(path)

			out_file_number = "outputs/"+str(i)+".out"
			output = open(out_file_number, "w")

			s = ""

			for i in range(len(final)):
				if(i != len(final) - 1):
					s = s + str(final[i]) + " "
				else:
					s = s + str(final[i])
			output.write(s + "\n")
			s = ""
			for i in range(len(line2)):
				if(i != len(line2) - 1):
					s = s + str(line2[i]) + " "
				else:
					s = s + str(line2[i])
			output.write(s + "\n")
			output.close()		
			
		except IndexError:
			print(input_file_number + " index error")
	except ValueError:
		print(input_file_number + " is a retard")
	except FileNotFoundError:
		print(input_file_number + " not found")



