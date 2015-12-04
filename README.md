# Finite State Machine

A simple Python implementation of a final state machine.

Will use some extra libs to handle operations with graphs and trees operations:

#Graphs

networkx: http://networkx.github.io/documentation/development/index.html
installing: sudo apt-get install python-networkx

#Trees

treelib: https://github.com/caesar0301/treelib
instaling: sudo easy_install -U treelib


This implementation have 3 main goals:

- Read finite state machines from files
- Read ste of sequences from files
- Verify if that the sequences (Test set) set is N-complete

This implementation is based in the following paper:

Adenilso Simao, Alexandre Petrenko: Checking Completeness of Tests for Finite State Machines.  IEEE Trans. Computers 59 (8): 1023­1032 (2010)
