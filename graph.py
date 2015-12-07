#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

#verification to avoid executions without the lib properly instaled
try:
	import networkx as nx

except:
	print 'Please, verify README.md file and follow the instructions'
	sys.exit(-1)


#to draw the graph
import matplotlib.pyplot as plt


verbose = True


"""
	Take the size of the tree and build a graph using networkx lib
"""
def build_distinction_graph(tree_size):
	
	"""
		Args:
			tree_size = just the size of the test tree
	"""
	
	#creat a graph object
	G = nx.Graph()

	#build a graph with the same number of node of test tree 
	for index in range(tree_size):

		#create nodes without edges
		G.add_node(index)


	#return the graph
	return G




"""
	Find all N size cliques on graph
"""
def find_cliques(n, distinction_graph):

	"""
		Args:
			n = number of states of a FSM
			distinction_graph = graph that will be used to search for the cliques
	"""

	#generate all possibles cliques
	all_cliques = list(nx.find_cliques(distinction_graph))

	#cliques with N size
	max_cliques = []

	#check the size of with clique
	for clique in all_cliques:

		if len(clique) == n:

			#if it's N size, add to max_cliques list
			max_cliques.append(sorted(clique)) #just sort the list to be more redable

	return max_cliques




"""
	Find labels using inference on distinction_graph. LEMMA 2 
"""
def graph_inference(labels, clique, distinction_graph):
	
	"""
		Args:
			labels - a disctionary to store the information about the label of each node
			clique - a n-size clique of distinction_graph
			distinction_graph - a networkx graph. Must apply lemma 1 first to obtain the edges between the nodes
	"""

	if verbose: print '\n########## LEMMA 2 ##########\n'
	
	#for each node on graph
	for node in distinction_graph:

		#if the node is on clique ignore it
		if node in clique:

			continue

		else:

			#get the edges that are connected to the node
			edges = distinction_graph.adj[node]
			
			#check if n-1 elements of the clique are conected to node
			if len(set(clique) - set(edges)) == 1:

				#get the element of the clique that arent connected to the node
				element = (set(clique) - set(edges)).pop()

				#get the label of the element
				label = labels[element]

				#write the node with the same label of the element found
				labels[node] = label

				if verbose: print 'Element of the clique: ', clique
				if verbose: print 'Node %d is connected to: ' % (node), list( set(set(clique)).intersection(set(edges)))
				if verbose: print 'Node %d label is equals to node %d: ' % (node, element), label

	return labels




"""
	Draw a graph
"""
def draw_graph(G):
	
	"""
		Args:
			G = a networkx graph
	"""

	# draw graph
	pos = nx.shell_layout(G)
	nx.draw(G, pos)

	# show graph
	plt.show()