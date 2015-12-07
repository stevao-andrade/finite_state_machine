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


verbose = False


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
	if verbose: tree.show()

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
				if verbose: print 'Find a distinguishable sequence: '
				if verbose: print 'Inputs: ', sequence1, sequence2
				if verbose: print 'Diferent Outputs: ', output1, output2
				

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

	#size of the tree
	tree_size = test_tree.size()

	#childs for n1 and n2
	childs_n1 = test_tree[n1].fpointer
	childs_n2 = test_tree[n2].fpointer

	#will generate all possibles distinguishable sequences for child_n1
	for child_n1 in childs_n1:
		
		#generate all possible sequences for child_n1	
		sequences_n1 = generate_all_sequences(child_n1, test_tree)

		#for each child n2
		for child_n2 in childs_n2:
			
			#generate all possible sequences for child_n2
			sequences_n2 = generate_all_sequences(child_n2, test_tree)

			#compare the sequence of child_n1 and child_n2... if one of the sequences are equal but produces a diferent output then return true
			result = compare_sequences(sequences_n1, sequences_n2)

			#if there is a valid result
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

	if verbose: print '\n########## LEMMA 1 ##########\n'

	#create a list with test_tree.size() elements
	l = [i for i in range(test_tree.size())] 


	#will look for the distinguishable sequence for each pair 
	for pair in itertools.combinations(l, r=2):

		#get the index of the nodes
		n1 = pair[0]
		n2 = pair[1]

		#see if the two nodes are t distinguishables
		if t_distinguishable(n1, n2, test_tree):

			if verbose: print 'The nodes %d and %d are T-Distinguishable. Will create an edge beetwen then.' % (n1, n2)

			#add a edge beetwen p1 and p2 in graph
			distinction_graph.add_edge(n1, n2)

	return distinction_graph



"""
	This method is used to build an index with sequences of common suffix
"""
def build_common_suffix_index(labels, test_tree, with_label):

	#an index with the labels that already have been discovered
	common_suffix = {}

	#build a index to identify the label of one element based in it's parent label and it's transference sequence
	for element in with_label:

		#get parent
		parent = test_tree[element].bpointer

		#if the parent have label to..
		if parent in labels.keys():

			#get all sequences for parent and for the element
			element_sequences = generate_all_sequences(element, test_tree)
			parent_sequences  = generate_all_sequences(parent, test_tree) 

			#will look just for the first sequence of element
			element_sequence = element_sequences[0].pop(0)
			parent_sequence  = parent_sequences[0].pop(0)

			#labels
			element_label = labels[element]
			parent_label  = labels[parent] 

			#build a index with the information already discovered
			key = (parent_label, element_sequence)  #when i'm on label and aply sequence i arrive on element_label
			
			common_suffix[key] = element_label

	return common_suffix




"""
	This method use the test tree to try discover new labels of the elements that aren't labeled yet. LEMMA 3 
"""
def common_suffix_verification(labels, test_tree):

	if verbose: print '\n########## LEMMA 3 ##########\n'

	#result represents if there is some alteration in labels.. it's begins as False
	result = False

	#an index with the labels that already have been discovered
	common_suffix = {}

	#a list with the elements that already been labeled
	with_label = labels.keys()

	if verbose: print 'Nodes with label: ', with_label
	
	#parent of the element that wants to discovery the label
	for parent in with_label:

		#update with_label value
		with_label = labels.keys()

		#generate a list to represent all elements of the graph
		without_label = [i for i in range(test_tree.size())]

		#update not_labeled just with the elements that aren't labeled yet
		without_label = list(set(without_label) - set(with_label))

		if verbose: print 'Nodes without label: ', without_label

		#encapsule inside a method to update the common_suffix for each iteration
		common_suffix = build_common_suffix_index(labels, test_tree, with_label)

		#now will use the created index to discover information about the elements that don't have label yet

		#get the childs.. candidate to be labeled
		childs = test_tree[parent].fpointer

		#for each child
		for child in childs:

			#wants to discovery child label
			if child in without_label:

				#parent label
				parent_label = labels[parent]

				#get the sequences of child
				child_sequences = generate_all_sequences(child, test_tree)
				
				#get just the first one
				child_sequence = child_sequences[0].pop() 

				#build the key to findout the label of child
				key = (parent_label, child_sequence)

				#lookup in the index in order to find a match
				if key in common_suffix.keys():

					if verbose: print 'Index of labels {(parent, element_sequence) : element_label}: ', common_suffix

					#if there is a match, update the label of the child
					labels[child] = common_suffix[key]

					#update result
					result = True

					if verbose: print 'Searching for the label of: ', child
					if verbose: print 'Sequence of %d: ' % (child), child_sequence
					if verbose: print 'Parent information (id, label): ', (parent, parent_label)
					if verbose: print 'Find a match in the index of labels!'
					if verbose: print 'Element %d label: ' % (child), common_suffix[key]

	#returning result will show if there are updates in labels
	return result, labels