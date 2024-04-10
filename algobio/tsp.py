#!/bin/python
import tsplib95
import math
from itertools import permutations
from collections import defaultdict
import argparse
import sys

## takes a tsplib95 instance of a TSP problem and a tour as a set of 
## returns the score of that tour, i.e. the sum of the weights in that tour as a roundtrip
def score_permutation(problem, tour):
    l = len(list(problem.get_nodes()))
    if not len(tour) == l:
        return -1
    
    sum = 0
    for i in range(1, len(tour)):
        if not (i, i+1 % l) in problem.get_edges():
            return -1
        sum = sum + problem.get_weight(i, i+1 % l)

    return sum

## brute forces the optimal solution to a tsplib95 instance
def brute_force(problem):
    minscore = math.inf
    minperm = []

    for perm in permutations(problem.get_nodes()):
        permscore = score_permutation(problem, perm)
        if permscore <= minscore and not permscore == -1:
            minscore = permscore
            minperm = perm

    return minperm

## a generator yielding all euler circuits on a tsplib95 instance
## optimised to terminate in O(e) if an ec does not exist
## otherwise, this method is in EXP
## contract: the graph is connected
def ec_iter(problem, list_vertices=True):
    deg_dict = defaultdict(lambda: 0)
    for e in problem.get_edges():
        deg_dict[e[0]]= deg_dict[e[0]] + 1
    #adj_list = [ filter(lambda l: l[0] == x, problem.get_edges()) for x in problem.get_nodes() ]

    if any(filter(lambda l: l% 2 == 1, deg_dict)):
        return
    
    for perm in permutations(problem.get_edges()):
        for i in range(0, len(perm)):
            if perm[i][1] != perm[i+1 %len(perm)]:
                continue
            if perm[0][0] != perm[-1][1]:
                continue
            
            yield map(lambda x: x[0], perm) if list_vertices else x

## the nearest Neighbour/NN approximation to the TSP
## takes a tsplib95 instance, returns an approximation of the optimal tour
def nearest_neighbour(problem):
    # build adjlist with distance
    adj_dict = defaultdict(lambda: [])
    for e in problem.get_edges():
        adj_dict[e[0]].append( (problem.get_weight(e[0], e[1]), e[1]) ) # e[0] is encoded in the key

    path = []
    
    v = 1 # start at first node
    while len(path) < len(list(problem.get_nodes()))-1:
        path.append(v) # eliminate loop edges
        v = min(filter(lambda x: x[1] not in path, adj_dict[v]))[1]

    path.append(v)
    return (* path,) # return as tuple


## greedy approximation for the TSP
## takes a tsplib95 instance, returns an approximation of the optimal tour
## only works for non-directional graphs
def greedy(problem):

    # initialise the component list to contain each individual component
    conn_comps = list(map(lambda x: [x], problem.get_nodes()))

    # sorted edge list, used in place of a minheap because heapq is weird
    # and does not allow non-standard keys
    edge_heap = sorted(problem.get_edges(), key=lambda x: problem.get_weight(x[0], x[1]))
    #print(edge_heap)

    # store path as dict, reconstruct permutation later
    path_dict = {}
    
    # iterate until the tour covers the entire graph
    while len(conn_comps) > 1:
        edge = edge_heap.pop(0) # heap-pop
        # find the components of the origin/endpoint of that edge
        # both guaranteed to be unique
        orig = list(filter(lambda x: edge[0] in x, conn_comps))[0]
        dest = list(filter(lambda x: edge[1] in x, conn_comps))[0]
        # check if the edge is internal to a component
        # or that node already has a marked edge
        if orig == dest or edge[0] in path_dict.keys():
            continue

        # merge the components
        orig.extend(dest)
        conn_comps.remove(dest)
        # add edge to path
        path_dict[edge[0]] = edge[1]
        
    # reconstruct the path, starting at the first node
    #print(path_dict)
    path = [1]
    j = 1
    l = len(path_dict)
    # find the right order, as long as it matters
    while True:
        j = path_dict.pop(j)
        path.append(j)
        if j not in path_dict.keys():
            break

    path.extend(path_dict.keys()) # add the stragglers
    return (* path,) # return as tuple





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A few TSP solving functions, as well as an EC generator. Uses TSPLIB95")
    parser.add_argument("-i", dest="in_file", help="Input TSPLIB file. Default and - are stdin.", type=argparse.FileType('r'), default='-')

    method = parser.add_mutually_exclusive_group(required=True)
    method.add_argument("-e", "--euler", dest="func", help="prints all euler circuits in the given graph to STDOUT", action="store_const", const= ec_iter)
    method.add_argument("-g", "--greedy", dest="func", help="Uses the greedy TSP heuristic", action="store_const", const= greedy)
    method.add_argument("-n", "--neighbour", dest="func", help="Uses the Nearest Neighbour TSP heuristic", action="store_const", const= nearest_neighbour)
    method.add_argument("-b", "--brute", dest="func", help="Brute-forces the TSP instance.", action="store_const", const= brute_force)

    args = parser.parse_args()
    
    problem = tsplib95.read(args.in_file)
    #print([x for x in problem.get_nodes()])
    #print([(x, problem.get_weight(x[0], x[1])) for x in problem.get_edges()])
    if args.func == ec_iter:
        for i in ec_iter(problem):
            print(i)
        sys.exit(0)

    path = args.func(problem)
    print(args.func(problem), ", score:", score_permutation(problem, path))
