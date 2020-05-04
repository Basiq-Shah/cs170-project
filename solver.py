import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance_fast
import sys
import math
import scipy.special
import bisect 

def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    
    smallest = [False, math.inf, math.inf, G.number_of_nodes()]

    vals = [0]*101
    for i in range(100):
        vals[i] = scipy.special.comb(i, 2)
    ban = []
    
    #  'm', 'n', 'a', 'b'

    for n in nx.nodes(G):
        G.add_node(n, state='a')

    for n in nx.nodes(G): 
        master = []
        ban.append(n)
        T = G.copy()
        for m in ban:
            T.add_node(m, state='m')
        for a in nx.neighbors(T, n):
            T.add_node(a, state='n')
        curr = [n]
        dom(G, T, [n], master, vals, smallest, curr, 1)

    return smallest[0]

def dom(G, T, claimed, master, vals, smallest, curr, size):
    visit = []
    for n in nx.nodes(T):
        if T.nodes[n]['state'] == 'n':
            visit.append(n)
    for n in visit:
        fam = curr.copy()
        bisect.insort(fam, n)
        if (fam not in master):
            claimed_copy = claimed.copy()
            master.append(fam)
            t2 = T.copy()
            t2.add_node(n, state = 'm')

            temp = []
            for (u, v, wt) in t2.edges.data('weight'):
                if (u == n and v in curr ) or (u in curr and v == n):
                    temp.append([u, v, wt])
            temp = min(temp, key = lambda p: p[2]) 
            t2.add_edge(temp[0], temp[1], weight= temp[2] )
            for a in nx.neighbors(t2, n):
                if t2.nodes[a]['state'] == 'a':
                    t2.add_node(a, state = 'n')
                elif t2.nodes[a]['state'] == 'n':
                    t2.add_node(a, state = 'b')
                if a not in claimed_copy:
                    claimed_copy.append(a)

            if (len(claimed_copy) == smallest[3]):
                cost = average_pairwise_distance_fast(t2)
                if  (cost < smallest[1] or (cost == smallest[1] and t2.number_of_nodes() < smallest[2])):
                    smallest[0] = t2
                    smallest[1] = cost
                    smallest[2] = t2.number_of_nodes()
                dom(G, t2, claimed_copy, master, vals, smallest, fam, size + 1)
                print(fam)
            else:
                dom(G, t2, claimed_copy, master, vals, smallest, fam, size + 1)
                print(fam)

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
