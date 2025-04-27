import networkx as nx
import matplotlib.pyplot as plt
import os

curr_dir = os.getcwd()
names_path = os.path.join(curr_dir, "wiki-topcats-page-names.txt")
nodes_path = os.path.join(curr_dir, "wiki-topcats.txt")

names_file = open(names_path, 'r')
names = names_file.readlines()

nodes_file = open(nodes_path, 'r')
nodes = nodes_file.readlines()

G = nx.DiGraph()

for line in nodes:
    src, dest = map(int, line.split())
    G.add_edge(src, dest)

dic = {}
for line in names:
    split_arr = line.split()
    node = int(split_arr[0])
    name = ' '.join(split_arr[1:])
    dic[node] = name
pos = nx.spring_layout(G)
#print(dic[0])

#print(G)
nx.draw(G, pos, with_labels=False, node_size=1500, node_color='lightblue', arrowsize=20)
nx.draw_networkx_labels(G, pos, labels=dic, font_size=10, font_color='black')
plt.tight_layout() 
plt.show()