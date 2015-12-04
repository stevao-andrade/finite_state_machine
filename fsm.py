#!/usr/bin/env python
# -*- coding: utf-8 -*-


from treelib import Tree, Node



"""
	This method is used to run some sequences into the FSM in order to retrive some information about the output of each state
"""
def run_fsm(sequences, paths, init_state):

	"""
		Args:
			paths      = a dictionary that represents the FSM. Each element is a entry that maps the FSM states into and it's outputs. Ex:. { state: [ output, destination), (output, destination) ..] }
			sequences  = a list that represents the sequences. Each element of the list is another list with the inputs of the sequence -> [ [x,y,x,y,x,x] ...]
			init_state = represents the initial state of the FSM
	"""

	#will store the output_sequence of each sequence
	output_sequences = []

	#first run each sequence in the list of sequences
	for sequence in sequences:

		next_state = init_state

		#will store each output for one sequence
		output_sequence = []

		#after that evaluate every input of each sequence
		for input_seq in sequence:

			#get the current state of the FSM
			possible_destinations = paths[next_state]

			#verify eache destination in possible destinations
			for destination in possible_destinations:

				#extract the output
				output = destination[0]
				
				#input is inside of output?
				if input_seq in output:

					#if it's true, get the destination and saves the output in output_sequence
					next_state = destination[1]
					output_sequence.append(output)


		#after verify each input of one sequence add it correspondet output_sequence in output_sequences
		output_sequences.append(output_sequence)

	#return output sequences
	return output_sequences