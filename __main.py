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
	#graph_nodes(infile)

	#Expand the Graph 
	#expand_and_contract_loop_2pt(in_file1)

	##_____________________##
	# Create clean sub graphs
	##_____________________##

	#Create Subgraphs
	#subgraph(in_file1, "1995")

	#expand_and_contract_loop_2pt("1995_full_multigraph.graphml")
	#Not all graphs need expansion and this fails to add edges in that case
	#But for years that need expansion, this gives the desired result


	years = [1995, 1996, 1997, 2001, 2002, 2003, 2004, 2005, 2006, 2008]

	attention = []
	for year in years:
		subgraph(in_file1, str(year))
		sub_file = str(year)+"_full_multigraph.graphml"
		result = expand_and_contract_loop_2pt(sub_file)
		if result=="NO_EXPANSION":
			attention.append(year)

	header = "----------------------------------------------\nYears Needing Manual Attention in Gephi: \n----------------------------------------------\n"

	try:
		print header, attention
		print "Writing results to file --> Gephi_Attention_Years.txt"
		f = open("Gephi_Attention_Years.txt", "w")
		f.write(header.encode('utf-8'))
		f.write(str(attention).encode('utf-8'))
		f.close


	except:
		print header, attention
		pass

	#subgraph(in_file2, "2005")

	#edge_year_filter_2pt(in_file2, "2005")

	#expand_and_contract_loop_2pt("2005_full_multigraph.graphml")

	"""
	Sequence Model

	#subgraph("entity_date_multigraph_fx.graphml", "2005")
	graph_nodes("2005_full_multigraph.graphml")
	"""

	#expand_and_contract_loop_2pt("full_2005_full_multigraph.graphml")

	"""
	years = [2005, 2006]
	infile_base = "_full_multigraph.graphml"

	for year in years:
		sub_graph_infile = str(year)+infile_base
	

		subgraph(in_file2, str(year)) #Subgraph still not correct
		expand_and_contract_loop_2pt(sub_graph_infile)
	"""




