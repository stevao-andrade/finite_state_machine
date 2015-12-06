#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys



#scripts used to handle operations with fsm, graphs, files and trees
from fsm import *
from graph import *
from util import *
from tree import *




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
	paths = read_fsm(fsm_file)
	

	#Create a list with sequences
	sequences = []
	sequences = read_sequences(sequences_file)

	#Run the sequences in FSM in order to get the outputs of each input
	output_sequences = run_fsm(sequences,paths, 1)


	#build the test tree
	test_tree = build_test_tree(output_sequences)

	#get the size of the tree
	tree_size = test_tree.size()

	#build distinction graph
	distinction_graph = build_distinction_graph(tree_size)

	#use lema 1 to create the edges between the nodes of the graph	
	distinction_graph = update_distinction_graph(test_tree, distinction_graph)




	#close the files at the end of execution
	fsm_file.close()
	sequences_file.close()