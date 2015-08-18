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


def remove_edges_from(self, ebunch):
        """Remove all edges specified in ebunch."""
	
	for e in ebunch:
		try:
			self.remove_edge(*e)
		except NetworkXError:
			pass


#____________________________________________________________________#
#                                                                    #
## <--- No Load Functions 2 Part (Read from Loaded Graph File) ---> ##
#____________________________________________________________________#


def expand_edges_nl2(loaded_Graph):
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

		else:
			G.add_edge(u, v, date=str(d['date']), entity=str(d['entity']), Label=lb, Weight='')
			G.remove_edge(u, v)
			pass


	edge_list(G, True, "Yes", "pass", "no_label", "loaded_Graph")

	print "Number of years-range edges detected = ", years_range_edges
	print "Number of years-range edges removed = ", removed_edges
	print "Number of new expanded edges added = ", expanded_edges
	print "Total number of new edges = ------>", (expanded_edges-removed_edges)

	return (expanded_edges-removed_edges)


def remove_edges_nl2(loaded_Graph):

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


def expand_and_contract_loop_2pt(subgraph):
	import shutil
	infile = subgraph
	outfile = "W_EXPANDED_"+infile
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

	if remaining_edges > 0:

		#Add Expanded Edges
		expand_edges_nl2(G)

		#Loop Over Edge Removal (Until Passes)
		while remaining_edges > 0:
			loop += 1
			print '\n', "Looping, working on loop number ", loop, "..."
			remove_edges_nl2(G)
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

	elif remaining_edges <= 0:
		print "...No edges need expansion."
		expand_edges_and_remove(outfile)
		testing_no_year_range(outfile)


#expand_and_contract_loop_2pt("1995_multigraph.graphml")
#expand_and_contract_loop_2pt("2008_multigraph.graphml")
#expand_and_contract_loop_2pt("allyears_multigraph_fx.graphml")
#expand_and_contract_loop_2pt("entity_date_multigraph_fx.graphml")
#expand_and_contract_loop_2pt("full_entity_date_multigraph_fx.graphml")


if __name__ == "__main__":
	expand_and_contract_loop_2pt("full_entity_date_multigraph_fx.graphml")
