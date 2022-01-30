import networkx as nx
import matplotlib.pyplot as plt

G = nx.complete_graph(10)
nx.draw(G)
plt.show()