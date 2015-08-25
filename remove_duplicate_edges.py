##################################
###                            ###
###      Joshua G. Mausolf     ###
###    Computation Institute   ###
###    University of Chicago   ###
###                            ###
##################################

import networkx as nx
import random
from graph_utility import *


def detect_duplicatesEdges(graphfile, head=10, load="graphfile"):

	if load == "graphfile":
		G=nx.read_graphml(str(graphfile))
	elif load == "loaded_Graph":
		G=graphfile
	else:
		print "Invalid load option. Please leave blank and specify a graphfile to read or provide a preloaded graphfile and select the option 'loaded_Graph'."

	infile = str(graphfile).split('_', 1)[0]

	edges = set()
	duplicates = set()
	for line in nx.generate_edgelist(G):
		#print line
		key = str(line)
		if key not in edges:
			edges.add(key)
		else:
			duplicates.add(key)

	if len(duplicates) > 0:
		duplicates = list(duplicates)
		if head < len(duplicates):
			print "DUPLICATES: ", head, " random duplicate values displayed...", '\n'
			for line in duplicates[0:head]:
				print random.choice(duplicates)
			print '\n', (len(duplicates) - head), " duplicate values not displayed..."
		
		else:
			print "DUPLICATES: ", len(duplicates), " random duplicate values displayed...", '\n'
			for line in duplicates:
				print random.choice(duplicates)

		print '\n', "-"*50, '\n', len(duplicates), "total duplicate values found.",'\n'
		return "DUPLICATES FOUND"
	else:
		print '\n', "-"*50, '\n', "NO DUPLICATES FOUND"
		return "NO DUPLICATES FOUND"


def duplicateEdges_test(graphfile):

	G=graphfile

	edges = set()
	duplicates = set()
	for line in nx.generate_edgelist(G):
		key = str(line)
		if key not in edges:
			edges.add(key)
		else:
			duplicates.add(key)

	return len(duplicates)


