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

def remove_edges_from(self, ebunch):
        """Remove all edges specified in ebunch.

        Parameters
        ----------
        ebunch: list or container of edge tuples
            Each edge given in the list or container will be removed
            from the graph. The edges can be:

                - 2-tuples (u,v) All edges between u and v are removed.
                - 3-tuples (u,v,key) The edge identified by key is removed.

        See Also
        --------
        remove_edge : remove a single edge

        Notes
        -----
        Will fail silently if an edge in ebunch is not in the graph.

        Examples
        --------
        >>> G = nx.MultiGraph() # or MultiDiGraph
        >>> G.add_path([0,1,2,3])
        >>> ebunch=[(1,2),(2,3)]
        >>> G.remove_edges_from(ebunch)

        Removing multiple copies of edges

        >>> G = nx.MultiGraph()
        >>> G.add_edges_from([(1,2),(1,2),(1,2)])
        >>> G.remove_edges_from([(1,2),(1,2)])
        >>> G.edges()
        [(1, 2)]
        >>> G.remove_edges_from([(1,2),(1,2)]) # silently ignore extra copy
        >>> G.edges() # now empty graph
        []
        """

	
	for e in ebunch:
		try:
			self.remove_edge(*e)
		except NetworkXError:
			pass



def detect_duplicatesEdges(graphfile, head=10, load="graphfile"):

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

	#G.remove_edges_from([list(duplicates)])
	#G.read_edgelist(edges)
	#print duplicates, len(duplicates)
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
		#return "no_duplicates"



#remove_duplicatesEdges("loop_allyears_entity_date_multigraph.graphml")
#print detect_duplicatesEdges("loop_2008_multigraph.graphml")
#remove_duplicatesEdges("2008_multigraph.graphml")

#detect_duplicatesEdges("loop_3_allyears_multigraph_fx.graphml", 5)
#detect_duplicatesEdges("nl_loop_2008_multigraph.graphml", 5)
#detect_duplicatesEdges("2008_multigraph.graphml", 5)


def duplicateEdges_test(graphfile):

	G=graphfile

	#infile = str(graphfile).split('_', 1)[0]

	edges = set()
	duplicates = set()
	for line in nx.generate_edgelist(G):
		key = str(line)
		if key not in edges:
			edges.add(key)
		else:
			duplicates.add(key)

	#print len(duplicates), " remaining duplicate values..."
	return len(duplicates)


def remove_duplicatesEdges(graphfile):

	import networkx as nx

	infile = str(graphfile).split('_', 1)[0]
	G=nx.read_graphml(str(graphfile))

	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")

	edges = set()
	duplicates = set()		
	for u,v,d in G.edges(data=True):
		key = str(zip(u, v, d))		
		if key not in edges:
			edges.add(key)
		else:
			duplicates.add(key)


	duplicates = list(duplicates)
	for edge in duplicates:
		G.remove_edges_from([(u,v),(u,v)])
		#G.remove_edges_from([(edge),(edge)])

	print detect_duplicatesEdges(G, 5, "loaded_Graph")

	"""
	duplicates = list(duplicates)
	while detect_duplicatesEdges(G, 2, "loaded_Graph") !="NO DUPLICATES FOUND":
		for edge in duplicates:
			G.remove_edges_from([(u,v),(u,v)])
		edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")	

	print detect_duplicatesEdges(G, 5, "loaded_Graph")
	"""
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
	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")


#remove_duplicatesEdges("loop_allyears_entity_date_multigraph.graphml")
#remove_duplicatesEdges("loop_2008_multigraph.graphml")
#remove_duplicatesEdges("2008_multigraph.graphml")

#remove_duplicatesEdges("loop_3_allyears_multigraph_fx.graphml")
#remove_duplicatesEdges("nl_loop_2008_multigraph.graphml")
#detect_duplicatesEdges("2008_multigraph.graphml", 2)

def rm_dup(graphfile):

	import collections
	import networkx as nx

	G=nx.read_graphml(str(graphfile))
	detect_duplicatesEdges(G, 2, "loaded_Graph")

	ctr = collections.Counter()
	for x in G.edges(data=True):
	#for G in [A, B, C, D]:
		print x
		ctr.update(str(x))
		if str(x) in ctr:
			G.remove_edge(x)
		else:
			print "fail"

	#duplicates = {x for (x,n) in ctr.viewitems() if n > 1}
	#duplicates = {u, v {d} for (u, v, d,n) in ctr.viewitems() if n > 1}
	#print duplicates

	#G.remove_edges_from([str(duplicates)])
	detect_duplicatesEdges(G, 2, "loaded_Graph")	

#rm_dup("nl_loop_2008_multigraph.graphml")


def remove_duplicatesEdges_nl(graphfile, load="graphfile"):
	import networkx as nx

	if load == "graphfile":
		G=nx.read_graphml(str(graphfile))
	elif load == "loaded_Graph":
		G=graphfile
	else:
		print "Invalid load option. Please leave blank and specify a graphfile to read or provide a preloaded graphfile and select the option 'loaded_Graph'."



	#infile = str(graphfile).split('_', 1)[0]
	#G=nx.read_graphml(str(graphfile))

	#edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")

	edges = set()
	duplicates = set()		
	for u,v,d in G.edges(data=True):
		key = str(zip(u, v, d))		
		if key not in edges:
			edges.add(key)
		else:
			duplicates.add(key)

	
	duplicates = list(duplicates)
	for edge in duplicates:
		G.remove_edges_from([(u,v),(u,v)])
	

	edge_list(G, True, "e1", "pass", "no_label", "loaded_Graph")
	return G



def remove_duplicates(graphfile):

	import networkx as nx
	import shutil
	infile = graphfile
	outfile = "rm_loop"+infile
	shutil.copy2(infile, outfile)

	#infile = str(graphfile).split('_', 1)[0]
	G=nx.read_graphml(outfile)

	print '\n', "-"*50, '\n', "EDGES BEFORE DUPLICATE REMOVAL:", '\n', "-"*50
	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")

	"""
	while detect_duplicatesEdges(G, 2, "loaded_Graph") !="NO DUPLICATES FOUND":
		#remove_duplicatesEdges_nl(outfile)
		G = remove_duplicatesEdges_nl(G, "loaded_Graph")
		
		#edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")
	"""

	duplicate_edges = duplicateEdges_test(G)

	while duplicate_edges > 0:
		#G = remove_duplicatesEdges_nl(G, "loaded_Graph")
		#remove_duplicatesEdges_nl(G, "loaded_Graph")
		H = remove_duplicatesEdges_nl(G, "loaded_Graph")
		duplicate_edges = duplicateEdges_test(H)
		#detect_duplicatesEdges(H, 2, "loaded_Graph")

	#print detect_duplicatesEdges(G, 5, "loaded_Graph")

	#return duplicates


	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")



#remove_duplicates("loop_3_allyears_multigraph_fx.graphml")
#remove_duplicates("nl_loop_2008_multigraph.graphml")

#print detect_duplicatesEdges("no_duplicates2008_multigraph.graphml", 5)
