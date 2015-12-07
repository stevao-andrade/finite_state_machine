#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import itertools

#verification to avoid executions without the lib properly instaled
try:
	from treelib import Tree
except:
	print 'Please, verify README.md file and follow instructions'
	sys.exit(-1)





"""
	Take a list with sequences formed by input/output and build the test tree. Will use treelib
"""
def build_test_tree(sequences):
	
	"""
		Args:
			sequences = a list that contanis the set of sequences. Format [[seq1], [seq2], [...]]
	"""

	tree = Tree() #test tree
	
	#add root to the tree
	node = tree.create_node('empty', 0)

	#get the root id to identify some parents nodes bellow
	root_id = node.identifier

	#just a counter to mantain a id to each node in the tree. 
	i = 0

	#sequence is as list with the inputs off each sequence 
	for sequence in sequences:

		#as tree already have one element, begin the counter at 1.
		i = i + 1

		#get the first element of the sequence
		init = sequence.pop(0)

		#add to the tree
		node = tree.create_node(init, i, parent = root_id)

		#parent to the nexts childs
		parent_id = node.identifier

		#now go through every input in the sequence. Every input will be a node into the teste tree
		for s in sequence:

			#increment the ID counter
			i = i + 1

			#add s node to the tree
			node = tree.create_node(s, i, parent = parent_id)

			#update parent for next iteration
			parent_id = node.identifier

	#to vizualize a representation of the tree in terminal uncomment the line bellow
	tree.show()

	return tree



"""
	Generate all possibles distinguishable sequences for a node in the tree
"""
def generate_all_sequences(node, test_tree):

	"""
		Args:
			node = a index of a treelib Node element 
			test_tree = the test_tree
	"""

	in_out = []		
	sequences = []
	
	#define a subtree of test_tree starting in node
	subtree = test_tree.subtree(node)
	
	#(iterator don't work) workaround to see every node in subtree
	for i in range(test_tree.size()):
		
		#workaround
		if i in subtree:

			#generate the sequence
			in_out = in_out + [subtree[i].tag]

			#add to the list of possibles sequences
			sequences.append(in_out)
	
	return sequences



"""
	Generate all possibles distinguishable sequences for a node in the tree
"""
def generate_all_sequences_w_output(node, test_tree):

	"""
		Args:
			node = a index of a treelib Node element 
			test_tree = the test_tree
	"""

	#input/output
	in_out = []	

	#one sequence
	sequence = []

	#all sequences
	sequences = []
	
	#define a subtree of test_tree starting in node
	subtree = test_tree.subtree(node)
	
	#(iterator don't work) workaround to see every node in subtree
	for i in range(test_tree.size()):
		
		#workaround
		if i in subtree:

			#destination node
			node = subtree[i].identifier

			#input/output
			in_out = [subtree[i].tag]

 			#generate the sequence
			sequence = sequence + in_out
 
 			#add to the list of possibles sequences
			sequences.append([sequence, node])
			sequences.append(in_out)
	
	return sequences




"""
	Take to sequences and compare to find a distinction 
"""
def compare_sequences(sequences1, sequences2):
	
	"""
		Args:
			sequence1 = all possible sequences formed by a arbitrary node 
			sequence2 = all possible sequences formed by a arbitrary node
	"""

	for sequence1, sequence2 in zip(sequences1, sequences2):

		for in_out1, in_out2 in zip(sequence1, sequence2):

			input1  = in_out1.split('/')[0] #get just input
			output1 = in_out1.split('/')[1] #get just output

			input2  = in_out2.split('/')[0] #get just input
			output2 = in_out2.split('/')[1] #get just output

			#compare inputs
			if input1 != input2:

				#go check next sequence1
				break

			if (input1 == input2) and (output1 == output2):

				#go check next input/output of sequence1
				continue

			#same input, diferent output (distinguishable)
			else:

				#uncomment to check
				#print '##########################'
				#print sequence1
				#print sequence2
				#print '##########################'

				return True

	#the sequences are indistinguishable
	return False




"""
	Take two nodes of the tree and evaluate if both are T-distinguishable
"""
def t_distinguishable(n1, n2, test_tree):
	
	"""
		Args:
			n1 = a index of a treelib Node element 
			n2 = a index of a treelib Node element
	"""

	tree_size = test_tree.size()

	childs_n1 = test_tree[n1].fpointer
	childs_n2 = test_tree[n2].fpointer

	#will generate all possibles distinguishable sequences for child_n1
	for child_n1 in childs_n1:
		
		sequences_n1 = generate_all_sequences(child_n1, test_tree)

		
		for child_n2 in childs_n2:
			
			sequences_n2 = generate_all_sequences(child_n2, test_tree)

			result = compare_sequences(sequences_n1, sequences_n2)

			if result:

				return True

	return False



"""
	This method is used to detect the edges between the nodes of the graph. The main goal is use the informations of the FSM to find T-distinguishable sequences and create edges between pairs of nodes
"""
def update_distinction_graph(test_tree, distinction_graph):

	"""
		Args:
			test_tree = a tree contructed using a set of sequences and the outputs of the FSM 
			distinction_graph = a empty graph that will be filled
	"""	

	#create a list with test_tree.size() elements
	l = [i for i in range(test_tree.size())] 


	#will look for the distinguishable sequence for each pair 
	for pair in itertools.combinations(l, r=2):

		#get the index of the nodes
		n1 = pair[0]
		n2 = pair[1]

		#see if the two nodes are t distinguishables
		if t_distinguishable(n1, n2, test_tree):

			#add a edge beetwen p1 and p2 in graph
			distinction_graph.add_edge(n1, n2)

	return distinction_graph




"""
	This method use the test tree to try discover new labels of the elements that aren't labeled yet. LEMMA 3 
"""
def common_suffix_verification(labels, test_tree):

	print '################### LEMMA 3 ###################'
	
	#a list with the elements that already been labeled
	labeled = labels.keys()

	#generate a list to represent all elements of the graph
	not_labeled = [i for i in range(test_tree.size())]

	#update not_labeled just with the elements that aren't labeled yet
	not_labeled = list(set(not_labeled) - set(labeled))

	print 'With label: ', labeled
	print 'Without label: ', not_labeled

	#will check every not labeled element
	for element in not_labeled:

		print 'Analysing element: ', element

		#generate all possible sequences for that element
		sequences1 = generate_all_sequences_w_output(element, test_tree)

		#get the first sequence for element		
		sequence1 = sequences1[0]
		destination_node1 = sequence1.pop(1) #get destination node of element and remove from sequence1

		#will check if there is label in before_node1
		before_node1 = destination_node1 - 1

		print 'Using this sequence: ', sequence1

		#for each element that already been confirmed
		for element_labeled in labeled:

			print 'Will compare with labeled element: ', element_labeled

			#generate all possible sequences for that element
			sequences2 = generate_all_sequences_w_output(element_labeled, test_tree)

			#now try find a commum sufix beetween 'element' and 'element_labeled' in order to find the label of the 'element'
			
			#get the first sequence for element_labeled			
			sequence2 = sequences2[0]
			destination_node2 = sequence2.pop(1) #get destination node of element_labeled and remove from sequence2

			#will check if there is label in before_node2
			before_node2 = destination_node2 - 1

			print 'Comparing with this sequence: ', sequence2

			#if the sequences are equals, label of element is the same label of element_labeled
			if (sequence1 == sequence2) and (before_node1 in labels.keys() and (before_node2 in labels.keys())):
				print 'Label of %d: ' % (element), labels[destination_node2]

				break