#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fsm import FiniteStateMachine


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

	#get the first element of the FSM and remove from the list of transitions
	element = transitions.pop(0)

	#populate the first element into FSM object


	
	#populate the others elements
	for element in transitions:
		pass



	return fsm



"""
	Read the sequences from a file and return into a list to run it into a fsm
"""
def read_sequences(txt):
 	
 	sequence = []

 	#read the file and populate sequence list

 	for line in txt:
 		sequence = line.split()  #each line is a list with one sequence
 		sequences.append(sequence) #append one sequence to the list of sequences

 	return sequences  