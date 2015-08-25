##################################
###                            ###
###      Joshua G. Mausolf     ###
###    Computation Institute   ###
###    University of Chicago   ###
###                            ###
##################################


import networkx as nx
from graph_utility import *


def testing_no_year_range_nl(loaded_Graph):

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

