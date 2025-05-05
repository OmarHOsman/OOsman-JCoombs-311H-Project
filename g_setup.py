import networkx as nx
import matplotlib.pyplot as plt
import os

# Number of nodes in subgraph
n = 1000

def get_deg(pair):
    return pair[1] #return the degree
def lis_maker(lis, n=500):
    return [node for node, deg in lis][:n]

def setup():
    curr_dir = os.getcwd()
    names_path = os.path.join(curr_dir, "wiki-topcats-page-names.txt")
    nodes_path = os.path.join(curr_dir, "wiki-topcats.txt")

    names_file = open(names_path, 'r')
    names = names_file.readlines()

    nodes_file = open(nodes_path, 'r')
    nodes = nodes_file.readlines()

    G = nx.DiGraph() #overall graph

    dic = {}
    for line in names:
        split_arr = line.split()
        node = int(split_arr[0])
        name = ' '.join(split_arr[1:])
        dic[node] = name

    for line in nodes:
        src, dest = map(int, line.split())
        if (src == dest or (dic[src] is None or dic[dest] is None)):
            continue #filter self referencing or inelgible pages
        G.add_edge(src, dest)
    #print(dic[0])
    #print(G)

    in_degrees = list(G.in_degree())
    out_degrees = list(G.out_degree())
    sorted_in_degrees = sorted(in_degrees, key=get_deg, reverse=True)
    sorted_out_degrees = sorted(out_degrees, key=get_deg, reverse=True)

    top_in_degrees = lis_maker(sorted_in_degrees, n)
    top_out_degrees = lis_maker(sorted_out_degrees, n)
    combined_in_out_degrees = top_in_degrees+top_out_degrees

    in_deg_G = G.subgraph(top_in_degrees).copy()#top n popular nodes
    out_deg_G = G.subgraph(top_out_degrees).copy()#top n influential nodes
    combined_deg_G = G.subgraph(combined_in_out_degrees).copy()#combined

    return G, in_deg_G, out_deg_G, combined_deg_G, dic

if __name__ == "__main__":
    G, in_deg_G, out_deg_G, combined_deg_G, dic = setup()

    pos = nx.spring_layout(in_deg_G)
    #print(in_deg_G)
    nx.draw(in_deg_G, pos, with_labels=False, node_size=50, node_color='lightblue', arrowsize=10)
    nx.draw_networkx_labels(in_deg_G, pos, labels={n:dic[n] for n in in_deg_G.nodes}, font_size=10, font_color='black')
    #plt.tight_layout() 
    plt.show()