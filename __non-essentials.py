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

#add_year_edges("1982_multigraph.graphml")
#add_year_edges("1995_multigraph.graphml")
#add_year_edges("2008_multigraph.graphml")
#add_year_edges("allyears_entity_date_multigraph.graphml")


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
	#edge_list(outfile, True, "Yes", "print")
	edge_list(outfile, True, "Yes")

#remove_years_range_edges("2008_edges_added_multigraph.graphml")
#remove_years_range_edges("1982_edges_added_multigraph.graphml")
#remove_years_range_edges("1995_edges_added_multigraph.graphml")
#remove_years_range_edges("1995_edges_removed_multigraph.graphml")
#remove_years_range_edges("allyears_edges_added_multigraph.graphml")



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


#expand_edges_and_remove("1982_multigraph.graphml")
#expand_edges_and_remove("1995_multigraph.graphml")
#expand_edges_and_remove("2008_multigraph.graphml")


def expand_and_contract_loop(subgraph):
	import shutil
	infile = subgraph
	outfile = "loop_"+infile
	shutil.copy2(infile, outfile)

	#Establish base statistics
	edge_list(outfile, True, "Yes")

	remaining_edges = testing_no_year_range(outfile)
	#print remaining_edges2, "number of remaining edges"

	G=nx.read_graphml(outfile)

	#Loop
	loop = 0
	if remaining_edges > 0:

		while remaining_edges > 0:
			loop += 1
			print '\n', "Looping, working on loop number ", loop, "..."
			expand_edges_and_remove(outfile)
			#expand_edges_and_remove_nl(G)
			remaining_edges = testing_no_year_range(outfile)
			test_no_year_range(outfile)
			#print testing_no_year_range(outfile)
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
	#infile = str(subgraph).split('_', 1)[0]
	#G=nx.read_graphml(loaded_Graph)
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


	#outfile = subgraph
	#nx.write_graphml(G, outfile)
	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")
	#edge_list(outfile, True, "Yes")

	print "Number of years-range edges detected = ", years_range_edges
	print "Number of years-range edges removed = ", removed_edges
	print "Number of new expanded edges added = ", expanded_edges
	print "Total number of new edges = ------>", (expanded_edges-removed_edges)

	return (expanded_edges-removed_edges)


def expand_edges_and_remove_nl2(loaded_Graph):
	#infile = str(subgraph).split('_', 1)[0]

	#G=nx.read_graphml(loaded_Graph)
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



	#outfile = subgraph
	#nx.write_graphml(G, outfile)
	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")
	#edge_list(outfile, True, "Yes")

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

	#G=nx.read_graphml(outfile)

	#Establish base statistics
	print '\n', "-"*50, '\n', "BASE GRAPH FILE BEFORE CONVERSION:", '\n', "-"*50
	edge_list(outfile, True, "Yes")
	#edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")
	print "-"*50
	remaining_edges = testing_no_year_range(outfile)
	#remaining_edges = testing_no_year_range_nl(G)
	#print remaining_edges2, "number of remaining edges"

	G=nx.read_graphml(outfile)

	#Loop
	loop = 0
	if remaining_edges > 0:

		while remaining_edges > 0:
			loop += 1
			print '\n', "Looping, working on loop number ", loop, "..."
			#expand_edges_and_remove(outfile)
			expand_edges_and_remove_nl2(G)
			remaining_edges = testing_no_year_range_nl(G)
			test_no_year_range_nl(G)
			print testing_no_year_range_nl(G)
			if remaining_edges <= 0:
				#nx.write_graphml(G, outfile)
				print '\n', "Total number of loops = ", loop, "...complete."
				#expand_edges_and_remove(outfile)
				#test_no_year_range(outfile)
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
	#Establish base statistics
	#edge_list(outfile, True, "Yes")
	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")
	print "-"*50

	#remaining_edges = testing_no_year_range(outfile)
	remaining_edges = testing_no_year_range_nl(G)
	#print remaining_edges2, "number of remaining edges"


	#Loop
	loop = 0
	if remaining_edges > 0:

		while remaining_edges > 0:
			loop += 1
			print '\n', "Looping, working on loop number ", loop, "..."
			#expand_edges_and_remove(outfile)
			expand_edges_and_remove_nl2(G)
			remaining_edges = testing_no_year_range_nl(G)
			test_no_year_range_nl(G)
			print testing_no_year_range_nl(G)
			if remaining_edges <= 0:
				nx.write_graphml(G, outfile)
				print '\n', "Total number of loops = ", loop, "...complete."
				print "Checking for duplicate edges...", '\n'
				#expand_edges_and_remove(outfile)
				#test_no_year_range(outfile)
				#test_no_year_range_nl(G)
				detect_duplicatesEdges(G, 10, "loaded_Graph")
				edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")
				#edge_list(outfile, True, "Yes", "w2")
				print "-"*50
				pass

	elif remaining_edges <= 0:
		print "...No edges need expansion."
		expand_edges_and_remove(outfile)
		testing_no_year_range(outfile)



######################################################################
#____________________________________________________________________#
#                                                                    #
## <-----------        Graph Utility Functions         -----------> ##
#____________________________________________________________________#
######################################################################

def make_filtered_subgraph(graphfile, year, test="no"):
	"""This function creates a subgraph for a given edge year
	Has correct nodes, but they lack attributes."""

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



######################################################################
#____________________________________________________________________#
#                                                                    #
## <-----------         Duplicates Functions           -----------> ##
#____________________________________________________________________#
######################################################################





######################################################################
#____________________________________________________________________#
#                                                                    #
## <-----------         Test Filter Functions          -----------> ##
#____________________________________________________________________#
######################################################################




