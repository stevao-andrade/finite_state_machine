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


verbose = False


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
	
	#result represents if there is some alteration in labels.. it's begins as False
	result = False

	#number of nodes
	number_nodes = nx.number_of_nodes(distinction_graph)

	#a list with the elements that already been labeled
	with_label = labels.keys()


	if verbose: print 'Nodes with label: ', with_label


	#generate a list to represent all elements of the graph
	without_label = [i for i in range(number_nodes)]

	#update not_labeled just with the elements that aren't labeled yet
	without_label = list(set(without_label) - set(with_label))


	if verbose: print 'Nodes without label: ', without_label		


	#for each node on graph
	for node in distinction_graph:

		#if node dont have a label..
		if node not in labels.keys():


			#create a list with all possible labels
			possible_labels = []
			for i in range(len(clique)):
				possible_labels.append(i)
		
		
			#get the edges that are connected to the node
			edges = list(distinction_graph.adj[node])
			
			#for each edged_node conected to the node			
			for e in edges:

				#look if the edge_node already have a label
				label_edge = None

				try:
					label_edge = labels[e]
				except:
					pass

				#if it have a label
				if label_edge in possible_labels:

					#remove it's label from the possible labes for node
					possible_labels.remove(label_edge)

			#if the number of possible labels for node is 1, then you found the label of node!
			if len(possible_labels) == 1:			

				#get the element labeled that aren't connected to the node
				element = possible_labels.pop()

				#get the label of the element
				label = element

				#write the node with the same label of the element found
				labels[node] = label

				#update result
				result = True

				if verbose: print 'Node %d is connected to: ' % (node), list( set(set(labels.keys())).intersection(set(edges)))
				if verbose: print 'Node %d label is equals to node %d: ' % (node, element), label

	#returning result will show if there are updates in labels 
	return result,labels




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