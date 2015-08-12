##################################
###                            ###
###      Joshua G. Mausolf     ###
###    Computation Institute   ###
###    University of Chicago   ###
###                            ###
##################################

import networkx as nx
from graph_utility import *

def remove_duplicatesEdges(graphfile):

	import networkx as nx

	infile = str(graphfile).split('_', 1)[0]
	G=nx.read_graphml(str(graphfile))

	dupl = set()
	def loop():
		edges = set()
		duplicates = set()
		for line in nx.generate_edgelist(G):
			#print line
			key = str(line)
			if key not in edges:
				edges.add(key)
			else:
				duplicates.add(key)

		G.remove_edges_from(duplicates)
		return duplicates

	edges = set()
	duplicates = set()
	for line in nx.generate_edgelist(G):
		#print line
		key = str(line)
		if key not in edges:
			edges.add(key)
		else:
			duplicates.add(key)

	#G.remove_edges_from(duplicates)
	#return duplicates

	#duplicates = loop()
	#G.remove_edges_from([(1,2),(1,2)])
	#print dupl, len(dupl)
	#print duplicates
	#print edges
	#outfile = "no_duplicates"+infile+"_multigraph.graphml"
	#nx.write_graphml(G, outfile)
	#print "removing duplicates in graph file"
	#print "writing new graph file -->", outfile, "..."
	#edge_list(G, True, "Yes", "print", "no_label", "loaded_Graph")

#remove_duplicatesEdges("loop_allyears_entity_date_multigraph.graphml")
#remove_duplicatesEdges("loop_2008_multigraph.graphml")
#remove_duplicatesEdges("2008_multigraph.graphml")


def detect_duplicatesEdges(graphfile, load="graphfile"):

	if load == "graphfile":
		#Load multigraph file
		G=nx.read_graphml(str(graphfile))
	elif load == "loaded_Graph":
		G=graphfile
	else:
		print "Invalid load option. Please leave blank and specify a graphfile to read or provide a preloaded graphfile and select the option 'loaded_Graph'."


	infile = str(graphfile).split('_', 1)[0]
	#G=nx.read_graphml(str(graphfile))


	edges = set()
	duplicates = set()
	for line in nx.generate_edgelist(G):
		#print line
		key = str(line)
		if key not in edges:
			edges.add(key)
		else:
			duplicates.add(key)

	#G.remove_edges_from(duplicates)
	#G.read_edgelist(edges)
	#print duplicates, len(duplicates)
	if len(duplicates) > 0:
		print "DUPLICATES:", '\n'
		pass
	for line in duplicates:
		print line
	if len(duplicates) > 0:
		print '\n', "-"*50, '\n'
		return "DUPLICATES FOUND"

	else:
		print '\n', "-"*50, '\n'
		return "NO DUPLICATES FOUND"
		#return "no_duplicates"



#remove_duplicatesEdges("loop_allyears_entity_date_multigraph.graphml")
#print detect_duplicatesEdges("loop_2008_multigraph.graphml")
#remove_duplicatesEdges("2008_multigraph.graphml")
