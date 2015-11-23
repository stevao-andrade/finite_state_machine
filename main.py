#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from util import *
from fsm import FiniteStateMachine


"""
	Main execution
"""
if __name__ == '__main__':

	#Verify the parameters to execution
	if len(sys.argv) < 2:
		print 'Usage: python main.py fsm.txt sequence.txt'
		#print 'Usage: python scheduler.py  num_workers'
		sys.exit(-1)

	#get the files 
	fsm_file = open(str(sys.argv[1]), 'r')
	sequences_file = open(str(sys.argv[2]), 'r')

	#Create a valid FSM obj
	fsm = FiniteStateMachine()
	fsm = util.read_fsm(fsm_file)

	#Create a list with sequences
	sequences = []
	sequences = util.read_sequences(sequences_file)