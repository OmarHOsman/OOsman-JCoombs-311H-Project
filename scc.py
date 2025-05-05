import networkx as nx
import matplotlib.pyplot as plt
from g_setup import setup
import os

# Get SCCs, optionally display or save large SCCs to a file
def get_sccs(G, dic, display=False, save=False):
    sccs = list(nx.strongly_connected_components(G))
    if display or save:
        data = ""
        for i, scc in enumerate(sccs):
            if len(scc) > 10:
                data += f"SCC {i}: {len(scc)} nodes\n"
                for node in scc:
                    data += f"  {dic[node]}\n"
        if display:
            print(data)
        if save:
            with open("sccs.txt", "w") as f:
                f.write(data)
    return sccs

# Calculate edge betweenness and node centrality for all edges and nodes in the SCC
def find_betweenness(G, dic, scc, display=False, save=False):
    edge_betweenness = nx.edge_betweenness_centrality(G.subgraph(scc))
    node_betweenness = nx.betweenness_centrality(G.subgraph(scc))
    # Sort by descending order
    edge_betweenness = dict(sorted(edge_betweenness.items(), key=lambda item: item[1], reverse=True))
    node_betweenness = dict(sorted(node_betweenness.items(), key=lambda item: item[1], reverse=True))
    if display or save:
        data = "Nodes:\n"
        for node in node_betweenness.keys():
            data += f"  {dic[node]}: {node_betweenness[node]}\n"
        data += "\n. . .\n\nEdges:\n"
        for edge in edge_betweenness.keys():
            data += f"  {dic[edge[0]]} to {dic[edge[1]]}: {edge_betweenness[edge]}\n"
        if display:
            print(data)
        if save:
            with open(f"betweenness_{num_large_sccs}.txt", "w") as f:
                f.write(data)
    return edge_betweenness, node_betweenness

# Process a passed-in graph to find and calculate betweenness for large SCCs
def process_graph(G, dic, display=False, save=False):
    sccs = get_sccs(G, dic, display, save)
    num_large_sccs = 0
    max_scc_size = max(len(scc) for scc in sccs)
    max_scc_in = 0
    edge_bet = []
    node_bet = []
    for scc in sccs:
        if len(scc) > 10:
            if len(scc) == max_scc_size:
                max_scc_in = num_large_sccs
            e, n = find_betweenness(G, dic, scc, display, save)
            edge_bet.append(e)
            node_bet.append(n)
            num_large_sccs += 1
    return edge_bet, node_bet, max_scc_size, max_scc_in, num_large_sccs

if __name__ == "__main__":
    G, in_deg_G, out_deg_G, combined_deg_G, dic = setup()

    edge_bet, node_bet, max_scc_size, max_scc_in, num_large_sccs = process_graph(combined_deg_G, dic)

    print(f"Number of large SCCs found: {num_large_sccs}")
    print(f"Size of largest SCC: {max_scc_size} nodes")
    print(f"\nTop 10 most central nodes in the largest SCC:")
    for i in range(10):
        print(f"  {dic[list(node_bet[max_scc_in])[i]]}: {node_bet[max_scc_in][list(node_bet[max_scc_in])[i]]}")
    print(f"\nTop 10 most common edges in the largest SCC:")
    for i in range(10):
        print(f"  {dic[list(edge_bet[max_scc_in])[i][0]]} to {dic[list(edge_bet[max_scc_in])[i][1]]}: {edge_bet[max_scc_in][list(edge_bet[max_scc_in])[i]]}")