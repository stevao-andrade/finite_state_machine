#!/usr/bin/env python
# -*- coding: utf-8 -*-



"""
	Read a fsm from a file and returns a dictionary that represents each state transition of the finite state machine
"""
def read_fsm(txt):

	"""
		Args:
			txt = a file that represents the finite state machine
	"""
	
	paths = {}
	n_states = 0

	#read the txt and create a list with each transition information
	for line in txt:

		#avoid empty lines 
		if line.strip():

			#replace one of the tokens
			line = line.replace('->','--')

			#split the line into a list with three elements [state, input/output, state_destination]
			element = line.split('--')

			#just remove the blank spaces of each element of the list	
			element = [e.strip() for e in element]

			#make more readable
			input_output      = element[1] 
			current_state     = int(element[0])
			state_destination = int(element[2])


			#a path is represented by a dict.. key (current state) and value a list where each element is tuple formed by (input_output, state_destination)
			path = [(input_output,state_destination)]

			
			#verify if current state is already in paths 
			if current_state in paths:

				#if its true, update the path to current state
				old_path = paths[current_state]
				new_path = old_path + path

				paths[current_state] = new_path


			#create a entry in dictionary with the path..
			else:

				n_states = n_states + 1
				paths[current_state] = path						

	return n_states, paths





"""
	Read the sequences from a file and return into a list to run it into a fsm
"""
def read_sequences(txt):

	"""
		Args:
			txt = a file that contains the sequences of test case
	"""

	
	sequences = []

	#read the file and populate sequences into a list

	#for each line in file
	for line in txt:

		#convert a line with a sequence into a list. Ex:. xxxy = [x,x,x,y]
		sequence = list(line)  

		#There is a \n at the end of some lines. So remove the 
		try:
			
			sequence.remove('\n') #remove the [\n] element
		
		except:

			pass #if [\n] do not exists, just pass

		#Add one sequence to the list of sequences
		sequences.append(sequence) #append one sequence to the list of sequences

	return sequences  