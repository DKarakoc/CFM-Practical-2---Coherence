#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 11:56:36 2017

@author: danny merkx

adapted and altered by Denis Karakoc on November 17th 2019
"""

import itertools
import numpy as np
import matplotlib.pyplot as plt


def make_graph(nV, conn_prob, neg_prob, D):
    # function to make a random graph of given size, takes a connection probability
    # and a probability that a connection is a negative constraint and the observation
    # set
    # if the special set of observations is not empty we need to add an extra,
    # always activated, node which connects to all elements in D
    if D:
        s = 1
    else:
        s = 0
    # the matrix that will contain all the edges
    E = np.matrix(np.zeros([nV + s, nV + s]))
    # the matrix that will contain all the activation levels
    V = np.matrix(np.zeros([nV + s]))
    V += 0.1
    # if there are special elements in D, we need a special node whose activation
    # will be fixed to 1.
    if D:
        V[0, -1] = 1
    # only accept connected graphs
    while not BFS(E, nV + s):
        # create all the 'normal' positive and negative constraints
        E = np.matrix(np.zeros([nV + s, nV + s]))
        for x in range(0, nV):
            for y in range(x + 1, nV):
                if np.random.rand() <= conn_prob:
                    if np.random.rand() >= neg_prob:
                        E[x, y] = 0.4
                    else:
                        E[x, y] = -0.6
        # If there are special elements in D, connect them to the 'always on'
        # node.
        if D:
            for x in D:
                E[x, nV] = 0.5
        E += np.transpose(E)

    return E, V


def BFS(G, nV):
    # a simple breadth first search to make sure the graph is connected (i.e. all nodes
    # have a path to all other nodes)
    queue = []
    visited_nodes = [0]
    # start at node 0, add it's connections to the queue
    curr_node = 0
    connections = [x for x in range(0, np.size(G[0])) if G[0, x] != 0]
    for x in connections:
        queue.append((curr_node, x))
    while queue:
        # add the current node to the list of visited nodes and choose the next node
        # from the queue in a BFS manner
        curr_node = queue[0][1]
        if not curr_node in visited_nodes:
            visited_nodes.append(curr_node)
        queue.pop(0)
        connections = [x for x in range(0, np.size(G[curr_node])) if G[curr_node, x] != 1]
        for x in connections:
            # prevent travelling back to visited nodes, we only need to know whether
            # each node can be reached from each other node by at least one path
            if not x in visited_nodes:
                queue.append((curr_node, x))
    if np.size(visited_nodes) == nV:
        return True
    else:
        return False


def Harmony(E, V):
    H = 0
    for x in range(np.size(V)):
        for y in range(np.size(V)):
            H += E[x, y] * V[0, x] * V[0, y]
    return H


# number of vertices
nV = 10
# number of epochs
nEpochs = 200
# decay
d = .95
# max and min values of the activation
Amax = 1
Amin = -1
# randomly assign some of the vertices as observations. These MUST be true in foundational
# coherence. In the N-Coh algorithms we couple the observations with a node whose
# activation is fixed to 1 such that the observation receives some baseline of activation
# at each iteration.
p_obs = np.random.rand(nV)
D = []
for x in range(nV):
    # control the observation probability through y
    y = 0.9
    if p_obs[x] > y:
        D.append(x)


# connection probability between any two nodes
conn_prob = 1
# probability of any connection being a negative constraint
neg_prob = 0.4
# matrices for the edges and vertices
E, V = make_graph(nV, conn_prob, neg_prob, D)

# keep track of the harmony
H = []
# create a generator which yields all possible instances
for epoch in range(nEpochs):
    # apply the activation update
    V = V * E
    # apply decay
    V *= d
    # the special node is also updated and decayed so set it back to 1
    if D:
        V[0,-1] = 1  #fix this only for F_Coh (next two lines)
        #for index in D:
         #   V[0, index] = 1
    # clip the matrix to the max and min values
    V = np.clip(V, Amin, Amax)
    H.append(Harmony(E, V))

# plt.plot(H)

def create_instance(nV):
    # this function creates a generator that generates all instances (possible truth
    # assignments) to our graph. Basically we generate all possible subsets of nodes, and
    # treat the nodes that are in this subset as being assigned 'True' and all the other nodes as
    # being false.
    for v in range(0,nV+1):
        for ex in itertools.combinations(range(nV), v):
            yield ex

# weight for the observation in discriminating coherence
w_d = 1

# trim the extra node for the observations D for exhaustive Search
if len(D)>0:
        E_trimmed = np.delete(E, nV , 0)
        E_trimmed = np.delete(E_trimmed, nV, 1)
else:
    E_trimmed = E

################# Discriminating Coherence Exhaustive Search ##########################
max_d_coh=0
# create a generator which yields all possible instances
for inst in create_instance(nV):
    coh = 0
    # calculate the coherence
    for x in range(nV):
        for y in range(x+1,nV):
        # check if the contraint is positive and if it is satisfied
            if E_trimmed[x,y] > 0 and ((x in inst and y in inst )or (not x in inst and not y in inst)) :
                coh += E_trimmed[x,y]
            # check if the contraint is negative and if it is satisfied
            elif E_trimmed[x,y] < 0 and ((x in inst and not y in inst) or (not x in inst and y in inst)):
                coh += abs(E_trimmed[x,y])
    # next check for each node in D if it is accepted and if so add the weight w_d to the coherence value
    for x in D:
        if x in inst:
            coh += w_d
    # update the max coherence
    if coh > max_d_coh:
        max_d_coh = coh
        best_d_inst = inst

print('Observations = ', D, '\n', 'D_coh:', max_d_coh, ' ', best_d_inst)

print(V)
print(best_d_inst)

approximation = []
exhaustive = []

# Convert the network's activation outputs into booleans
for index in range(nV):
    if V[0, index] > 0:
        approximation.append(True)
    else:
        approximation.append(False)

print(approximation)


# Convert the exhaustive search's output into booleans
for each in range(nV):
    exhaustive.append(False)

for index in best_d_inst:
    exhaustive[index] = True

print(exhaustive)

# Compare the two outputs
mismatches = 0
for index in range(nV):
    if exhaustive[index] != approximation[index]:
        mismatches += 1

print("Mismatches: " + str(mismatches))