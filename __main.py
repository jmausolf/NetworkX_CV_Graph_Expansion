##################################
###                            ###
###      Joshua G. Mausolf     ###
###    Computation Institute   ###
###    University of Chicago   ###
###                            ###
##################################


#------------------------------------#
import networkx as nx
from test_filter import *
from graph_utility import *
from remove_duplicate_edges import *
from filter_first_edge_date import *
#------------------------------------#

if __name__ == "__main__":

	infile = "entity_date_multigraph_fx.graphml"
	in_file1 = "full_"+str(infile)
	in_file2 = "EXPANDED_"+str(in_file1)



	##_____________________##
	# Create clean full graph
	##_____________________##

	#Add and Clean Node Labels
	graph_nodes(infile)

	#Expand the Graph 
	expand_and_contract_loop_2pt(in_file1)

	##_____________________##
	# Create clean sub graphs
	##_____________________##

	#Create Subgraphs
	
	years = [2005, 2006]
	infile_base = "_full_multigraph.graphml"

	for year in years:
		sub_graph_infile = str(year)+infile_base
	

		subgraph(in_file2, str(year)) #Subgraph still not correct
		expand_and_contract_loop_2pt(sub_graph_infile)



