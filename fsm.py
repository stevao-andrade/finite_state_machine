#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
	This class will represent a FiniteStateMachine
"""
class FiniteStateMachine(self):

	"""docstring for FiniteStateMachine"""
	

	#Contructor
	def __init__(self):
		
		self.init_state  = None   #initial state
		self.pool_states = {}	  #a hash table with all states


	#define the initial state
	def set_init_state(self, state):
		
		"""
			Args:

				state = state that represents the begin of the finite state machine
		"""

		#Will set all states in uppercase to avoid typos  
		self.init_state = state.upper()

	