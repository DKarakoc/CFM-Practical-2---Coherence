# -*- coding: utf-8 -*-
"""
This is example code for an implementation of an exhaustive
search for the Foundational and discriminating coherence problem. 
You are free to use this if you get stuck somewhere in the assignment, 
however you will still need to upload your own code with the assignment.
This script is not guaranteed to be a perfect implementation. 
Any mistakes you copy will be judged as your own mistakes for the grading. 
"""
import itertools
import numpy as np

def create_instance(nV):
    # this function creates a generator that generates all instances (possible truth
    # assignments) to our graph. Basically we generate all possible subsets of nodes, and
    # treat the nodes that are in this subset as being assigned 'True' and all the other nodes as
    # being false.
    for v in range(0,nV+1):
        for ex in itertools.combinations(range(nV), v):
            yield ex

def make_graph(nV, conn_prob, neg_prob):
# function to make a random graph of given size, takes a connection probability
# and a probability that a connection is a negative constraint
    G = np.matrix(np.zeros([nV, nV]))
    # only accept connected graphs
    while not BFS (G, nV):
        G = np.matrix(np.zeros([nV, nV]))
        for x in range (0,nV):
            for y in range (x+1,nV):
                if np.random.rand() <= conn_prob:
                    if np.random.rand() >=neg_prob:
                        G[x,y] = np.random.rand()
                    else:
                        G[x,y] = np.random.rand()-1
        G += np.transpose(G)
    return G
def BFS(G, nV):
# a simple breadth first search to make sure the graph is connected (i.e. all nodes
# have a path to all other nodes)
    queue = []
    visited_nodes = [0]
    # start at node 0, add it's connections to the queue
    curr_node = 0
    connections = [x for x in range (0,np.size(G[0])) if G[0,x] != 0]
    for x in connections:
        queue.append((curr_node,x))
    while queue:
        # add the current node to the list of visited nodes and choose the next node
        # from the queue in a BFS manner        
        curr_node = queue[0][1]
        if not curr_node in visited_nodes:
            visited_nodes.append(curr_node)
        queue.pop(0)
        connections = [x for x in range (0,np.size(G[curr_node])) if G[curr_node,x] != 1]
        for x in connections:
            # prevent travelling back to visited nodes, we only need to know whether
            # each node can be reached from each other node by at least one path
            if not x in visited_nodes:
                queue.append((curr_node,x))
    if np.size(visited_nodes) == nV:
        return True
    else: 
        return False
    
# number of vertices
nV = 10
# observations (in Foundational coherence these MUST be true, in Discriminating
# coherence these have a weight i.e. the instance gets a bonus if these are true)
# randomly assign a small amount of vertices as observations
p_obs = np.random.rand(nV)
D = []
# weight for the observation in discriminating coherence
w_d = 1
for x in range(nV):
    # control the observation probability through y
    y = 0.8
    if p_obs[x] > y:
        D.append(x)
D = set(D)
# connection probability (applied to all possible connection of the fully connected graph)
conn_prob = 0.5
# probability of any connection being a negative constraint
neg_prob = 0.5
# matrix to hold the graph structure
G = make_graph(nV, conn_prob, neg_prob)

################ Foundational Coherence ##########################
# keep track of the maximum coherence
max_f_coh=0
# create a generator which yields all possible instances
for inst in create_instance(nV):
    # first check if the instance is valid, that is, the observations in D are True
    if D.issubset(set(inst)):
        coh = 0
        # calculate the coherence
        for x in range(nV):
            for y in range(x+1,nV):
                if G[x,y] > 0 and ((x in inst and y in inst ) or (not x in inst and not y in inst)) :
                    coh += G[x,y]
                elif G[x,y] < 0 and ((x in inst and not y in inst) or (not x in inst and y in inst)):
                    coh += abs(G[x,y])
        # update the max coherence
        if coh > max_f_coh:
            max_f_coh = coh
            best_f_inst = inst
            
################# Discriminating Coherence ##########################
max_d_coh=0            
# create a generator which yields all possible instances
for inst in create_instance(nV):
    coh = 0
    # calculate the coherence
    for x in range(nV):
        for y in range(x+1,nV):
        # check if the contraint is positive and if it is satisfied
            if G[x,y] > 0 and ((x in inst and y in inst )or (not x in inst and not y in inst)) :
                coh += G[x,y]
            # check if the contraint is negative and if it is satisfied
            elif G[x,y] < 0 and ((x in inst and not y in inst) or (not x in inst and y in inst)):
                coh += abs(G[x,y])
    # next check for each node in D if it is accepted and if so add the weight w_d to the coherence value
    for x in D:
        if x in inst:
            coh += w_d
    # update the max coherence
    if coh > max_d_coh:
        max_d_coh = coh
        best_d_inst = inst
print('D = ', D, '\n', 'F_coh:' , max_f_coh , ' ' , best_f_inst, '\n', 'D_coh:', max_d_coh, ' ', best_d_inst)

