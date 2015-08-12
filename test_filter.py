##################################
###                            ###
###      Joshua G. Mausolf     ###
###    Computation Institute   ###
###    University of Chicago   ###
###                            ###
##################################


import networkx as nx
from graph_utility import *

def edge_check_nl(loaded_Graph, u, v):
	G=nx.read_graphml(loaded_Graph)
	#G = loaded_Graph
	print (nx.shortest_path(G,source=u,target=v))
	#print (nx.has_path(G,source=u,target=v))

#edge_check_nl("2008_multigraph.graphml", "160", "159")


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

#print testing_no_year_range("1995_multigraph.graphml")


def testing_no_year_range_nl(loaded_Graph):
	#G=nx.read_graphml(graph_file)

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

#print testing_no_year_range("1995_multigraph.graphml")

def testing_no_year_range_nl_edge(loaded_Graph, u, v):
	#G=nx.read_graphml(graph_file)

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


def test_no_year_range_nl(loaded_Graph):
	G=loaded_Graph
	print "_"*60, '\n'
	print "...Testing file --> "

	#edge_list(graph_file, True, "Yes")
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
		#print "_"*60, '\n'
		print '\n', "FAILED. Edge test failed: number of failed edges = ", failed_edges
		print "_"*60
	elif failed_edges == 0:
		#print "_"*60, '\n'
		print "PASSED. Edge test passed: number of failed edges = ", failed_edges
		print "_"*60


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
		#print "_"*60, '\n'
		print '\n', "FAILED. Edge test failed: number of failed edges = ", failed_edges
		print "_"*60
	elif failed_edges == 0:
		#print "_"*60, '\n'
		print "PASSED. Edge test passed: number of failed edges = ", failed_edges
		print "_"*60


#test_no_year_range("loop_allyears_entity_date_multigraph.graphml")
#test_no_year_range("allyears_edges_removed_multigraph.graphml")
#test_no_year_range("1982_edges_removed_multigraph.graphml")
#test_no_year_range("1982_edges_removed_multigraph.graphml")
#test_no_year_range("1995_edges_removed_multigraph.graphml")
#test_no_year_range("1989_multigraph.graphml")
#test_no_year_range("1995_multigraph.graphml")
#test_no_year_range("1982_multigraph.graphml")
#test_no_year_range("2008_edges_removed_multigraph.graphml")
