#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


#scripts used to handle operations with fsm, graphs, files and trees
from fsm import *
from graph import *
from util import *
from tree import *


verbose = True


"""
	Main execution
"""
if __name__ == '__main__':

	#Verify the parameters to execution
	if len(sys.argv) < 2:
		print 'Usage: python main.py fsm.txt sequence.txt'
		#print 'Usage: python scheduler.py  num_workers'
		sys.exit(-1)


	#open the files 
	fsm_file = open(str(sys.argv[1]), 'r')
	sequences_file = open(str(sys.argv[2]), 'r')


	#create a dictionary to simulate the execution of a FSM
	paths = {}
	n_states, paths = read_fsm(fsm_file) #get the number of states and paths
	

	#Create a list with sequences
	sequences = []
	sequences = read_sequences(sequences_file)

	#close the files. will note need they anymore
	fsm_file.close()
	sequences_file.close()

	#Run the sequences in FSM in order to get the outputs of each input
	output_sequences = run_fsm(sequences,paths, 1)

	#build the test tree
	test_tree = build_test_tree(output_sequences)

	#get the size of the tree
	number_elements = test_tree.size()

	#build distinction graph
	distinction_graph = build_distinction_graph(number_elements)

	#use lema 1 to create the edges between the nodes of the graph	
	distinction_graph = update_distinction_graph(test_tree, distinction_graph)

	#find all cliques of N size in distinction graph
	cliques = find_cliques(n_states, distinction_graph)

	#some FSM dont have a cliques
	if cliques:

		#
		for clique in cliques:

			#result starts as true
			result = True

			#a dictionary to store the label of each node of distinction graph/ test_tree.
			labels = {}

			#clique = cliques[0]
			clique = [0, 6, 7, 12]

			#start labeling the elements of the clique
			for i in range(len(clique)):
				labels[clique[i]] = i


			#try apply LEMMA 2 and LEMMA 3 while it's possibile
			while result:

				#apply LEMMA 2.. if there are updates in labels, then lemma2 is True
				lemma2, labels = graph_inference(labels, clique, distinction_graph)
				
				#apply LEMMA 3.. if there are updates in labels, then lemma3 is True
				lemma3, labels = common_suffix_verification(labels, test_tree)

				#update result value.. 
				result = lemma2 or lemma3

				print 'Partial Labels: ', labels
			
			#check theorema 1 or just verify if all nodes of the graph have label
			if len(labels.keys()) == number_elements:
				print 'the set is n-complete!'
				sys.exit(0)

			print 'acabou'

	#if the FSM dont have cliques
	else:

		print 'the set is not n-complete.'
		sys.exit(-1)
