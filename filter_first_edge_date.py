##################################
###                            ###
###      Joshua G. Mausolf     ###
###    Computation Institute   ###
###    University of Chicago   ###
###                            ###
##################################

import cPickle
import networkx as nx
import itertools

from test_filter import *
from graph_utility import *
from remove_duplicate_edges import *



#____________________________________________________________________#
#                                                                    #
## <------- Functions Used for Edge Expansion and Deletion  ------> ##
#____________________________________________________________________#

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


def year_expand(year_range):
	import sys
	from datetime import date

	#year_range = "1995-00-00:2013-00-00"
	edge_years = year_range.split(":", 1)
	startDate = int(edge_years[0][0:4])
	endDate = int(edge_years[1][0:4])

	#Build Expanded Year List from Input
	year_list = []
	for result in perdelta(startDate, endDate+1, 1):
		years_expansion = str(str(result)+"-00-00")
		year_list.append(years_expansion)

	return year_list

#year_expand("1995-00-00:2013-00-00")
#year_expand("1982-00-00:1994-00-00")
#print year_expand("2008-00-00:2009-00-00")

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

	"""
	for e in ebunch:
		if e in ebunch:
			try:
				self.remove_edge(*e)
			except NetworkXError:
				pass
	"""
#____________________________________________________________________#
#                                                                    #
## <-------    Load Functions (Read from Raw Graph File)    ------> ##
#____________________________________________________________________#


def expand_edges_and_remove_test(subgraph):
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
	edge_list(outfile, True, "Yes", "print")
	#edge_list(outfile, True, "Yes")

	print "Number of years-range edges detected = ", years_range_edges
	print "Number of years-range edges removed = ", removed_edges
	print "Number of new expanded edges added = ", expanded_edges
	print "Total number of new edges = ------>", (expanded_edges-removed_edges)

	return (expanded_edges-removed_edges)


#expand_edges_and_remove_test("1982_multigraph.graphml")
#expand_edges_and_remove_test("1995_multigraph.graphml")
#expand_edges_and_remove_test("2008_multigraph.graphml")

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


def expand_edges_and_remove2(subgraph):
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
		if len(_year) > 10:
			years_range_edges += 1
			year_list = year_expand(str(_year))

			#Expand Year-Range Edge
			#Add a Duplicate Edge for each year in Expanded Range
			for new_year in year_list:
				expanded_edges +=1
				added_edges = set()
				edges = set()
				duplicates = set()
				for line in nx.generate_edgelist(G):
					key = str(line)
					if key not in edges:
						edges.add(key)
						G.add_edge(u, v, date=new_year, entity=str(d['entity']))
					else:
						duplicates.add(key)

				"""
				#key = str(G.add_edge(u, v, date=new_year, entity=str(d['entity'])))
				if detect_duplicatesEdges(G, "loaded_Graph") !="duplicates":
					G.add_edge(u, v, date=new_year, entity=str(d['entity']))
				else:
					print "DUPLICATES FOUND --> PASS"
					print detect_duplicatesEdges(G, "loaded_Graph")
					pass
				"""
			
			G.remove_edge(u, v)
			removed_edges +=1

		else:
			#print _year
			pass

	#print "Number of years-range edges detected = ", years_range_edges
	#print "Number of new expanded edges added = ", expanded_edges


	outfile = subgraph
	nx.write_graphml(G, outfile)
	#edge_list(outfile, True, "Yes", "print")
	#edge_list(outfile, True, "Yes")

	print "Number of years-range edges detected = ", years_range_edges
	print "Number of years-range edges removed = ", removed_edges
	print "Number of new expanded edges added = ", expanded_edges
	print "Total number of new edges = ------>", (expanded_edges-removed_edges)

	return (expanded_edges-removed_edges)


#expand_edges_and_remove2("1982_multigraph.graphml")
#expand_edges_and_remove2("2008_multigraph.graphml")


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


#expand_and_contract_loop("1982_multigraph.graphml")
#expand_and_contract_loop("1989_multigraph.graphml")
#expand_and_contract_loop("1995_multigraph.graphml")
#expand_and_contract_loop("2009_multigraph.graphml")
#expand_and_contract_loop("2008_multigraph.graphml")
#expand_and_contract_loop("allyears_multigraph_fx.graphml")


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


#expand_edges_and_remove_nl("1982_multigraph.graphml")

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


#expand_edges_and_remove_nl2("1982_multigraph.graphml")
#expand_edges_and_remove_nl2("1995_multigraph.graphml")


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



#expand_and_contract_loop_nl("1989_multigraph.graphml")
#expand_and_contract_loop_nl("1995_multigraph.graphml")
#expand_and_contract_loop_nl("2008_multigraph.graphml")
#expand_and_contract_loop_nl("2009_multigraph.graphml")
#expand_and_contract_loop_nl("all_years_entity_date_multigraph.graphml")




def expand_and_contract_loop_nlo(subgraph):
	import shutil
	infile = subgraph
	outfile = "nl_loop_"+infile
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
				print "-"*50
				pass

	elif remaining_edges <= 0:
		print "...No edges need expansion."
		expand_edges_and_remove(outfile)
		testing_no_year_range(outfile)



#expand_and_contract_loop_nlo("1989_multigraph.graphml")
#expand_and_contract_loop_nlo("1995_multigraph.graphml")
expand_and_contract_loop_nlo("2008_multigraph.graphml")
#expand_and_contract_loop_nlo("2009_multigraph.graphml")
#expand_and_contract_loop_nlo("all_years_entity_date_multigraph.graphml")
#expand_and_contract_loop_nlo("allyears_multigraph_fx.graphml")


#test_no_year_range("loop_3_all_years_entity_date_multigraph.graphml")
