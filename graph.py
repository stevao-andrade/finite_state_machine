#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

#verification to avoid executions without the lib properly instaled
try:
	import networkx as nx
except:
	print 'Please, verify README.md file and follow the instructions'
	sys.exit(-1)




"""
	Take the size of the tree and build a graph using networkx lib
"""
def build_distinction_graph(tree_size):
	
	"""
		Args:
			fsm_list = a list that contanis the finit state machine. Format [{ 'input': value, 'current_state': value, 'transition_state': value }]
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

"""