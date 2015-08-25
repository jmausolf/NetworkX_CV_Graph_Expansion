##################################
###                            ###
###      Joshua G. Mausolf     ###
###    Computation Institute   ###
###    University of Chicago   ###
###                            ###
##################################

"""
These functions were created during the creation of this package.

Although these functions run, the results were suboptimal compared to the final
module design. Depending on your purpose or needs, these may have utility, 
and have been included to that end.

The functions have been organized into sections respective of the original
script they came from. These functions largely draw upon other functions
from the rest of the module.

To run, please import:
------------------------------------
import networkx as nx
from test_filter import *
from graph_utility import *
from remove_duplicate_edges import *
from filter_first_edge_date import *
------------------------------------
"""


######################################################################
#____________________________________________________________________#
#                                                                    #
## <-----------    Filter First Edge Date Functions    -----------> ##
#____________________________________________________________________#
######################################################################


#____________________________________________________________________#
#                                                                    #
## <------- Functions Used for Edge Expansion and Deletion  ------> ##
#____________________________________________________________________#

def add_year_edges(subgraph):
	infile = str(subgraph).split('_', 1)[0]

	G=nx.read_graphml(subgraph)

	years_range_edges = 0
	expanded_edges = 0
	for u,v,d in G.edges(data=True):
		try:
			_year = d['date']
		except:
			print "ERROR: An error has occured in defining edge dates."
			pass
		if len(_year) > 10:
			years_range_edges += 1
			year_list = year_expand(str(_year))

			#Expand Year-Range Edge
			for new_year in year_list:
				expanded_edges +=1
				G.add_edge(u, v, date=new_year, entity=str(d['entity']))

		else:
			pass

	print "Number of years-range edges detected = ", years_range_edges
	print "Number of new expanded edges added = ", expanded_edges


	outfile = infile+"_edges_added"+"_multigraph.graphml"
	nx.write_graphml(G, outfile)
	edge_list(outfile, True, "Yes", "print")

	print "Number of years-range edges detected = ", years_range_edges
	print "Number of new expanded edges added = ", expanded_edges


def remove_years_range_edges(subgraph):
	infile = str(subgraph).split('_', 1)[0]

	G=nx.read_graphml(subgraph)

	years_range_edges = 0
	for u,v,d in G.edges(data=True):
		try:
			_year = d['date']
		except:
			print "ERROR: An error has occured in defining edge dates."
		if len(_year) > 10:
			years_range_edges +=1
			print str(_year)
	
			#Remove Original Year Range e.g. 1982-1994
			G.remove_edge(u, v)

		else:
			pass

	print "Number of years-range edges detected = ", years_range_edges

	outfile = infile+"_edges_removed"+"_multigraph.graphml"
	nx.write_graphml(G, outfile)
	print "writing file "+outfile
	edge_list(outfile, True, "Yes")


#____________________________________________________________________#
#                                                                    #
## <-------    Load Functions (Read from Raw Graph File)    ------> ##
#____________________________________________________________________#


def expand_edges_and_remove(subgraph, edge_print="pass"):
	infile = str(subgraph).split('_', 1)[0]

	G=nx.read_graphml(subgraph)

	years_range_edges = 0
	expanded_edges = 0
	removed_edges = 0
	for u,v,d in G.edges(data=True):
		try:
			_year = d['date']
		except:
			print "ERROR: An error has occured in defining edge dates."

		#Define Label
		lb = str(d['entity']).title().split('|')[1]

		if len(_year) > 10:
			years_range_edges += 1
			year_list = year_expand(str(_year))

			#Expand Year-Range Edge
			for new_year in year_list:
				expanded_edges +=1
				G.add_edge(u, v, date=new_year, entity=str(d['entity']), Label=lb)

			G.remove_edge(u, v)
			removed_edges +=1


		else:
			G.add_edge(u, v, date=str(d['date']), entity=str(d['entity']), Label=lb)
			G.remove_edge(u, v)
			pass


	outfile = subgraph
	nx.write_graphml(G, outfile)
	if edge_print == "print":
		edge_list(outfile, True, "Yes", "print")
	else:
		edge_list(outfile, True, "Yes")

	print "Number of years-range edges detected = ", years_range_edges
	print "Number of years-range edges removed = ", removed_edges
	print "Number of new expanded edges added = ", expanded_edges
	print "Total number of new edges = ------>", (expanded_edges-removed_edges)

	return (expanded_edges-removed_edges)


def expand_and_contract_loop(subgraph):
	import shutil
	infile = subgraph
	outfile = "loop_"+infile
	shutil.copy2(infile, outfile)

	#Establish base statistics
	edge_list(outfile, True, "Yes")

	remaining_edges = testing_no_year_range(outfile)

	G=nx.read_graphml(outfile)

	#Loop
	loop = 0
	if remaining_edges > 0:

		while remaining_edges > 0:
			loop += 1
			print '\n', "Looping, working on loop number ", loop, "..."
			expand_edges_and_remove(outfile)
			remaining_edges = testing_no_year_range(outfile)
			test_no_year_range(outfile)
			if remaining_edges == 0:
				print '\n', "Total number of loops = ", loop, "...complete."
				expand_edges_and_remove(outfile, "print")
				test_no_year_range(outfile)
				pass

	elif remaining_edges == 0:
		print "...No edges need expansion."
		expand_edges_and_remove(outfile)
		testing_no_year_range(outfile)


#____________________________________________________________________#
#                                                                    #
## <------- No Load Functions (Read from Loaded Graph File) ------> ##
#____________________________________________________________________#

def delete_edge_loop(loaded_Graph):

	G = loaded_Graph

	remaining_edges = testing_no_year_range_nl(G)
	print remaining_edges
	while remaining_edges > 0:
		for u,v,d in G.edges(data=True):
			try:
				_year = d['date']
			except:
				_year = 'except'
			G.remove_edge(u, v)
			remaining_edges = testing_no_year_range_nl(G)


def expand_edges_and_remove_nl(loaded_Graph):
	G = loaded_Graph

	years_range_edges = 0
	expanded_edges = 0
	removed_edges = 0
	for u,v,d in G.edges(data=True):
		try:
			_year = d['date']
		except:
			print "ERROR: An error has occured in defining edge dates."

		#Define Label
		lb = str(d['entity']).title().split('|')[1]

		if len(_year) > 10:
			years_range_edges += 1
			year_list = year_expand(str(_year))

			#Expand Year-Range Edge
			for new_year in year_list:
				expanded_edges +=1
				G.add_edge(u, v, date=new_year, entity=str(d['entity']), Label=lb)

			G.remove_edge(u, v)
			removed_edges +=1

		else:
			G.add_edge(u, v, date=str(d['date']), entity=str(d['entity']), Label=lb)
			G.remove_edge(u, v)
			pass

	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")

	print "Number of years-range edges detected = ", years_range_edges
	print "Number of years-range edges removed = ", removed_edges
	print "Number of new expanded edges added = ", expanded_edges
	print "Total number of new edges = ------>", (expanded_edges-removed_edges)

	return (expanded_edges-removed_edges)


def expand_edges_and_remove_nl2(loaded_Graph):

	G = loaded_Graph

	years_range_edges = 0
	expanded_edges = 0
	removed_edges = 0
	for u,v,d in G.edges(data=True):
		try:
			_year = d['date']
		except:
			print "ERROR: An error has occured in defining edge dates."

		#Define Label
		lb = str(d['entity']).title().split('|')[1]

		if len(_year) > 10:
			years_range_edges += 1
			year_list = year_expand(str(_year))

			#Expand Year-Range Edge
			for new_year in year_list:
				expanded_edges +=1
				G.add_edge(u, v, date=new_year, entity=str(d['entity']), Label=lb)

			G.remove_edges_from([(u,v),(u,v)])
			removed_edges +=1


		else:
			G.add_edge(u, v, date=str(d['date']), entity=str(d['entity']), Label=lb)
			G.remove_edge(u, v)
			pass

	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")

	print "Number of years-range edges detected = ", years_range_edges
	print "Number of years-range edges removed = ", removed_edges
	print "Number of new expanded edges added = ", expanded_edges
	print "Total number of new edges = ------>", (expanded_edges-removed_edges)

	return (expanded_edges-removed_edges)


def expand_and_contract_loop_nl(subgraph):
	import shutil
	infile = subgraph
	outfile = "nl2_loop_"+infile
	shutil.copy2(infile, outfile)

	print "loading graph file..."

	#Establish base statistics
	print '\n', "-"*50, '\n', "BASE GRAPH FILE BEFORE CONVERSION:", '\n', "-"*50
	edge_list(outfile, True, "Yes")
	print "-"*50
	remaining_edges = testing_no_year_range(outfile)

	G=nx.read_graphml(outfile)

	#Loop
	loop = 0
	if remaining_edges > 0:

		while remaining_edges > 0:
			loop += 1
			print '\n', "Looping, working on loop number ", loop, "..."
			expand_edges_and_remove_nl2(G)
			remaining_edges = testing_no_year_range_nl(G)
			test_no_year_range_nl(G)
			print testing_no_year_range_nl(G)
			if remaining_edges <= 0:
				print '\n', "Total number of loops = ", loop, "...complete."
				test_no_year_range_nl(G)
				print detect_duplicatesEdges(G, "loaded_Graph")
				pass

	elif remaining_edges <= 0:
		print "...No edges need expansion."
		expand_edges_and_remove(outfile)
		testing_no_year_range(outfile)


def expand_and_contract_loop_nlo(subgraph):
	import shutil
	infile = subgraph
	outfile = "nlo_loop_"+infile
	shutil.copy2(infile, outfile)

	print "loading graph file..."
	G=nx.read_graphml(outfile)

	print '\n', "-"*50, '\n', "BASE GRAPH FILE BEFORE CONVERSION:", '\n', "-"*50
	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")
	print "-"*50

	remaining_edges = testing_no_year_range_nl(G)

	#Loop
	loop = 0
	if remaining_edges > 0:

		while remaining_edges > 0:
			loop += 1
			print '\n', "Looping, working on loop number ", loop, "..."
			expand_edges_and_remove_nl2(G)
			remaining_edges = testing_no_year_range_nl(G)
			test_no_year_range_nl(G)
			print testing_no_year_range_nl(G)
			if remaining_edges <= 0:
				nx.write_graphml(G, outfile)
				print '\n', "Total number of loops = ", loop, "...complete."
				print "Checking for duplicate edges...", '\n'
				detect_duplicatesEdges(G, 10, "loaded_Graph")
				edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")
				print "-"*50
				pass

	elif remaining_edges <= 0:
		print "...No edges need expansion."
		expand_edges_and_remove(outfile)
		testing_no_year_range(outfile)


def edge_year_filter_expand_nl2(loaded_Graph):
	G = loaded_Graph

	years_range_edges = 0
	expanded_edges = 0
	removed_edges = 0
	for u,v,d in G.edges(data=True):
		try:
			_year = d['date']
		except:
			print "ERROR: An error has occured in defining edge dates."

		#Define Label
		lb = str(d['entity']).title().split('|')[1]

		if len(_year) > 10:

			print ">10"
			G.add_edge(u, v, date=str(_year), entity=str(d['entity']), Label=lb)

		else:
			print "else"
			G.add_edge(u, v, date=str(d['date']), entity=str(d['entity']), Label=lb, Weight='')
			G.remove_edge(u, v)
			pass


	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")

	print "Number of years-range edges detected = ", years_range_edges
	print "Number of years-range edges removed = ", removed_edges
	print "Number of new expanded edges added = ", expanded_edges
	print "Total number of new edges = ------>", (expanded_edges-removed_edges)

	return (expanded_edges-removed_edges)


def edge_year_filter_remove_nl2(loaded_Graph):

	G = loaded_Graph

	years_range_edges = 0
	expanded_edges = 0
	removed_edges = 0
	for u,v,d in G.edges(data=True):
		try:
			_year = d['date']
		except:
			print "ERROR: An error has occured in defining edge dates."

		#Define Label
		lb = str(d['entity']).title().split('|')[1]

		if year not in str(_year):

			G.remove_edges_from([(u,v),(u,v)])
			removed_edges +=1

		else:
			pass

	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")

	print "Number of years-range edges detected = ", years_range_edges
	print "Number of years-range edges removed = ", removed_edges
	print "Number of new expanded edges added = ", expanded_edges
	print "Total number of new edges = ------>", (expanded_edges-removed_edges)

	return (expanded_edges-removed_edges)


def edge_year_filter_2pt(subgraph, year):
	import shutil
	infile = subgraph
	outfile = "EXPANDED_"+infile
	shutil.copy2(infile, outfile)

	print "\nLoading graph file..."+str(infile)+"..."
	G=nx.read_graphml(outfile)

	#Establish base statistics
	print '\n', "-"*50, '\n', "BASE GRAPH FILE BEFORE CONVERSION:", '\n', "-"*50
	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")
	print "-"*50

	remaining_edges = testing_no_year_range_nl(G)

	#Loop
	loop = 0

	if remaining_edges <= 0:

		#Add Expanded Edges
		edge_year_filter_expand_nl2(G, year)

		#Loop Over Edge Removal (Until Passes)
		while remaining_edges <= 0:
			loop += 1
			print '\n', "Looping, working on loop number ", loop, "..."
			edge_year_filter_remove_nl2(G, year)
			remaining_edges = testing_no_year_range_nl(G)
			test_no_year_range_nl(G)
			if remaining_edges <= 0:
				print "\nWriting new graph file..."+str(outfile)+"\n", "...Please wait -->"
				nx.write_graphml(G, outfile)
				print '\n', "Total number of loops = ", loop, "...complete."
				print "Checking for duplicate edges...", '\n'
				detect_duplicatesEdges(G, 10, "loaded_Graph")
				edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")
				print "-"*50, '\n'
				pass

	elif remaining_edges > 0:
		pass


######################################################################
#____________________________________________________________________#
#                                                                    #
## <-----------        Graph Utility Functions         -----------> ##
#____________________________________________________________________#
######################################################################

def make_filtered_subgraph(graphfile, year, test="no"):

	_graphfile = str(graphfile)
	_year = str(year)

	G=nx.read_graphml(graphfile)
	SG=nx.MultiGraph( [ (u,v,d) for u,v,d in G.edges(data=True) if _year in d['date'].split(':', 1)[0]])

	outfile = _year+"_multigraph.graphml"
	nx.write_graphml(SG, outfile)

	if test == "no":
		pass
	elif test == "test":
		edge_list(outfile, True, "Yes", "print")


def subgraph_filter(graphfile, year, test="no"):

	_graphfile = str(graphfile)
	_year = str(year)

	G=nx.read_graphml(graphfile)
	
	#Create Subgraph with Edges for Specified Year
	SG=nx.MultiGraph( [ (u,v,d) for u,v,d in G.edges(data=True) if _year in d['date'].split(':', 1)[0]])
	
	#Copy All Nodes and Node Data to Subgraph
	SG.add_nodes_from(G.nodes(data=True))
	
	#Remove Nodes without Edges from Subgraph
	SG.remove_nodes_from((n for n,d in SG.degree_iter() if d==0))


	#Ensure Subgraph Edge Labels Present
	for u,v,d in SG.edges(data=True):

		#Define Label
		lb = str(d['entity']).title().split('|')[1]

		G.add_edge(u, v, date=str(d['date']), entity=str(d['entity']), Label=lb, Weight='')
		G.remove_edge(u, v)

	outfile = "aux_"+_year+"_full_multigraph.graphml"
	nx.write_graphml(SG, outfile)

	#Print Options
	if test == "no":
		edge_list(outfile, True, "Yes")
		pass
	elif test == "test":
		edge_list(outfile, True, "Yes", "print")


######################################################################
#____________________________________________________________________#
#                                                                    #
## <-----------         Duplicates Functions           -----------> ##
#____________________________________________________________________#
######################################################################


def remove_edges_from(self, ebunch):
	
	for e in ebunch:
		try:
			self.remove_edge(*e)
		except NetworkXError:
			pass


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

	print detect_duplicatesEdges(G, 5, "loaded_Graph")


	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")


def remove_duplicatesEdges_nl(graphfile, load="graphfile"):
	import networkx as nx

	if load == "graphfile":
		G=nx.read_graphml(str(graphfile))
	elif load == "loaded_Graph":
		G=graphfile
	else:
		print "Invalid load option. Please leave blank and specify a graphfile to read or provide a preloaded graphfile and select the option 'loaded_Graph'."

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

	G=nx.read_graphml(outfile)

	print '\n', "-"*50, '\n', "EDGES BEFORE DUPLICATE REMOVAL:", '\n', "-"*50
	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")

	duplicate_edges = duplicateEdges_test(G)

	while duplicate_edges > 0:
		H = remove_duplicatesEdges_nl(G, "loaded_Graph")
		duplicate_edges = duplicateEdges_test(H)

	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")


######################################################################
#____________________________________________________________________#
#                                                                    #
## <-----------         Test Filter Functions          -----------> ##
#____________________________________________________________________#
######################################################################


def edge_check_nl(loaded_Graph, u, v):
	G=nx.read_graphml(loaded_Graph)
	print (nx.shortest_path(G,source=u,target=v))


def testing_no_year_range(graph_file):
	G=nx.read_graphml(graph_file)

	failed_edges = 0
	for u,v,d in G.edges(data=True):
		try:
			_year = d['date']
		except:
			pass
		if len(_year) > 10:
			failed_edges +=1
	return failed_edges


def testing_no_year_range_nl_edge(loaded_Graph, u, v):

	G = loaded_Graph

	failed_edges = 0
	for u,v,d in G.edges(data=True):
		try:
			_year = d['date']
		except:
			pass
		if len(_year) > 10:
			failed_edges +=1
	return failed_edges


def test_no_year_range(graph_file):
	G=nx.read_graphml(graph_file)
	print "_"*60, '\n'
	print "...Testing file --> "+str(graph_file)

	edge_list(graph_file, True, "Yes")
	failed_edges = 0
	for u,v,d in G.edges(data=True):
		try:
			_year = d['date']
		except:
			pass
		if len(_year) > 10:
			print u, v, str(_year), d['entity']
			failed_edges +=1

	if failed_edges > 0:
		print '\n', "FAILED. Edge test failed: number of failed edges = ", failed_edges
		print "_"*60
	elif failed_edges == 0:
		print "PASSED. Edge test passed: number of failed edges = ", failed_edges
		print "_"*60


