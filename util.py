#!/usr/bin/env python
# -*- coding: utf-8 -*-

#This script will handle the file operations


"""
	Read a fsm from a file and returns a FiniteStateMachine obj
"""
def read_fsm(txt):
	
	fsm = FiniteStateMachine()

	transitions = []

	#read the file and populate fsm object

	for line in txt:

		#replace one of the tokens
		line = line.replace('->','--')

		#split the line into a list with three elements [state, transition, state_destination]
		element = line.split('--')

		#add to the list of transition
		transitions.append(element)

		
	#populate the others elements
	for element in transitions:
		print element



	return fsm



"""
	Read the sequences from a file and return into a list to run it into a fsm
"""
def read_sequences(txt):
 	
 	sequences = []

 	#read the file and populate sequence list

 	for line in txt:

 		#Avoid empyt lines into the file
 		if line.strip():

	 		sequence = list(line)  #convert a line with a sequence into a list. Ex:. xxxy = [x,x,x,y]

	 		#There is a \n at the end of some lines. So remove the 
	 		try:
	 			sequence.remove('\n') #remove the [\n] element
	 		except:
	 			pass #if [\n] do not exists, just pass

	 		#Add one sequence to the list of sequences
	 		sequences.append(sequence) #append one sequence to the list of sequences

	#Testing
 	for s in sequences:
 		print s
 		
 	return sequences  