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
    nodes = list(G.nodes)
    smallest = [False, math.inf, math.inf]

    for n in nodes:
        master = []
        T = nx.Graph()
        T.add_node(n)

        finder(G, T, [], list(G.neighbors(n)), master, [n], 0, 0, smallest)

    return smallest[0]

def finder(G, T, banned, neighs, master, curr, cost, size, smallest):
    for b in neighs[:]:
        curr_copy = curr.copy()
        curr_copy.append(b)
        curr_copy.sort()
        neighs.remove(b)
        if (curr_copy not in master):
            t2 = T.copy()
            neighs_copy = neighs.copy()
            banned_copy = banned.copy()
            banned_copy.append(b)
            temp = []
            for (u, v, wt) in G.edges.data('weight'):
                if ((u == b) and (v in curr_copy) or (v == b) and (u in curr_copy)):
                    temp.append((u, v, wt))
            temp = min( temp,  key=lambda p: p[2])
            t2.add_edge( temp[0], temp[1], weight = temp[2])

            for x in list(G.neighbors(b)):
                if (x in neighs_copy):
                    neighs_copy.remove(x)
                    banned_copy.append(x)
                elif (x not in banned_copy):
                    neighs_copy.append(x)
            master.append(curr_copy)

            newCost = math.inf
            if is_valid_network(G, t2):
                newCost = average_pairwise_distance_fast(t2)
                if ((smallest[0] == False) or (smallest[1] > cost) or (smallest[1] == cost and smallest[2] > size)):
                    smallest[0] = t2
                    smallest[1] = newCost
                    smallest[2] = size + 1
            finder(G, t2, banned_copy, neighs_copy, master, curr_copy, newCost, size + 1, smallest)
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
