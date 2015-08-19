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
	#subgraph(in_file1, "1995")

	#expand_and_contract_loop_2pt("1995_full_multigraph.graphml")
	#Not all graphs need expansion and this fails to add edges in that case
	#But for years that need expansion, this gives the desired result

	years = [1940,	1941,	1942,	1943,	1944,	1945,	1946,	1947,	1948,	1949,	1950,	1951,	1952,	1953,	1954,	1955,	1956,	1957,	1958,	1959,	1960,	1961,	1962,	1963,	1964,	1965,	1966,	1967,	1968,	1969,	1970,	1971,	1972,	1973,	1974,	1975,	1976,	1977,	1978,	1979,	1980,	1981,	1982,	1983,	1984,	1985,	1986,	1987,	1988,	1989,	1990,	1991,	1992,	1993,	1994,	1995,	1996,	1997,	1998,	1999,	2000,	2001,	2002,	2003,	2004,	2005,	2006,	2007,	2008,	2009,	2010,	2011,	2012,	2013,	2014,	2015]


	attention = []

	for year in years:
		try:
			subgraph(in_file1, str(year))
			sub_file = str(year)+"_full_multigraph.graphml"
			result = expand_and_contract_loop_2pt(sub_file)
			if result=="NO_EXPANSION":
				attention.append(year)
		except:
			print "Sorry, "+str(year)+" not found in multigraph dataset."
			pass

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




