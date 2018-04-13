import matplotlib.pyplot as plt
import scipy as sp
from networkx import *
import sys

n= 50
e = 580

G=fast_gnp_random_graph(n, 0.4)
# some properties
print("node degree clustering")
for v in nodes(G):
    print('%s %d %f' % (v,degree(G,v),clustering(G,v)))

# print the adjacency list to terminal
try:
    write_adjlist(G,sys.stdout)
except TypeError: # Python 3.x
    write_adjlist(G,sys.stdout.buffer)

A = nx.to_numpy_matrix(G)

for i in range(len(A)):
	print(A[i])

nx.draw(G)
nx.write_gexf(G, "./graphs/50node.gexf")