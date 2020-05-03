import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance_fast
import sys
import math

def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    master = []
    smallest = [False, math.inf, math.inf]
    
    #  'marked', 'neighbor', 'alone', 'banned'

    for n in nx.nodes(G):
        G.add_node(n, state='alone')

    for n in nx.nodes(G):    
        T = G.copy()
        T.add_node(n, state='marked')
        for a in nx.neighbors(T, n):
            T.add_node(a, state='neighbor')
        curr = [n]
        dom(G, T, master, smallest, curr)

    return smallest[0]

def dom(G, T, master, smallest, curr):
    visit = []
    for n in nx.nodes(T):
        if T.nodes[n]['state'] == 'neighbor':
            visit.append(n)
    for n in visit:
        fam = curr.copy()
        fam.append(n)
        if (fam not in master):
            master.append(fam)
            t2 = T.copy()
            t2.add_node(n, state = 'marked')

            temp = []
            for (u, v, wt) in t2.edges.data('weight'):
                if (u == n and v in curr ) or (u in curr and v == n):
                    temp.append([u, v, wt])
            temp = min(temp, key = lambda p: p[2]) 
            t2.add_edge(temp[0], temp[1], weight= temp[2] )
            for a in nx.neighbors(t2, n):
                if t2.nodes[a]['state'] == 'alone':
                    t2.add_node(a, state = 'neighbor')
                elif t2.nodes[a]['state'] == 'neighbor':
                    t2.add_node(a, state = 'banned')
            cost = average_pairwise_distance_fast(t2)
            if is_valid_network(G, t2) and (cost < smallest[1] or (cost == smallest[1] and t2.number_of_nodes() < smallest[2])):
                smallest[0] = t2
                smallest[1] = cost
                smallest[2] = t2.number_of_nodes()
            dom(G, t2, master, smallest, fam)

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    T = solve(G)
    assert is_valid_network(G, T)
    print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
    write_output_file(T, 'out/test.out')
