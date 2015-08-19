##################################
###                            ###
###      Joshua G. Mausolf     ###
###    Computation Institute   ###
###    University of Chicago   ###
###                            ###
##################################

import networkx as nx


#____________________________________________________________________#
#                                                                    #
## <---------------       Edge List Utility        ---------------> ##
#____________________________________________________________________#

def edge_list(graphfile, data_option, stat_option, print_write="pass", for_label="no_label", load="graphfile"):
	
	if load == "graphfile":
		#Load multigraph file
		G=nx.read_graphml(str(graphfile))
	elif load == "loaded_Graph":
		G=graphfile
	else:
		print "Invalid load option. Please leave blank and specify a graphfile to read or provide a preloaded graphfile and select the option 'loaded_Graph'."

	data = data_option
	stat = stat_option.lower()
	print_option = print_write.lower()


	#Print edges (with no data labels)
	if data==False:
		if print_write == "pass":
			pass
		else:
			if print_write == "print":
				for line in nx.generate_edgelist(G, data=False):
					print(line)
					pass
			elif print_write == "write":
				try:
					outfile = 'Edge_List__'+graphfile+".csv"
					f=open(outfile, 'a')
					for line in nx.generate_edgelist(G, data=False):
						delimited_line = line.replace(' ', ',')
						f.write(u'%s\n' % (delimited_line))
				finally:
					f.close()
					pass
			else:
				pass

	#Print edges (with data labels)
	elif data ==True:
		if print_write == "pass":
			pass
		else:
			if for_label=="no_label":
				if print_write == "print":
					for line in nx.generate_edgelist(G):
						print(line)
						pass
				elif print_write == "write":
					try:
						outfile = 'Edge_List__'+graphfile+".csv"
						f=open(outfile, 'a')
						for line in nx.generate_edgelist(G):
							delimited_line = line.replace(' ', ',')
							f.write(u'%s\n' % (delimited_line))
					finally:
						f.close()
						pass
				elif print_write == "w2":
					try:
						outfile = 'Edgelist-W2__'+graphfile+".csv"
						f=open(outfile, 'a')
						for line in nx.generate_edgelist(G):
							delimited_line = line.replace('	', ' ').replace(',', ' ')
							f.write(u'%s\n' % (delimited_line))
					finally:
						f.close()
						pass

			elif for_label!="no_label":
				if print_write == "print":
					for line in nx.generate_edgelist(G, data=[str(for_label)]):
						print(line)
						pass
				elif print_write == "write":
					try:
						outfile = 'Edge_List__'+graphfile+".csv"
						f=open(outfile, 'a')
						for line in nx.generate_edgelist(G, data=[str(for_label)]):
							delimited_line = line.replace(' ', ',')
							f.write(u'%s\n' % (delimited_line))
					finally:
						f.close()
						pass
				else:
					pass

	#Print Stat Option
	if stat=="yes":
		print '\n'"MULTIGRAPH STATISTICS"'\n', '_'*20, '\n', "Nodes: ", G.number_of_nodes(), '\n', "Edges: ", G.size(), '\n', '_'*20, '\n'
	elif stat=="e1":
		print "Edges: ", G.size()
	elif stat=="no":
		pass
	else:
		print "Please input a valid option. Would you like to return the number of edges: 'yes' or 'no'?" 


#edge_list("entity_date_multigraph.graphml", True, "Yes", "pass", "date")
#edge_list("loop_allyears_entity_date_multigraph.graphml", True, "Yes", "print")
#edge_list("2008_multigraph.graphml", True, "Yes", "print")
#edge_list("2008_multigraph.graphml", True, "Yes", "pass")
#edge_list("2008_edges_added_multigraph.graphml", True, "Yes", "write")
#edge_list("2008_edges_removed_multigraph.graphml", True, "Yes", "write")
#tedge_list("entity_date_multigraph_fx.graphml", True, "Yes", "print")


#____________________________________________________________________#
#                                                                    #
## <---------------       Graph Manipulation       ---------------> ##
#____________________________________________________________________#

def graph_nodes(graphfile, test="no"):
	
	#infile = str(graphfile).split('_', 1)[0]
	_graphfile = str(graphfile)

	G=nx.read_graphml(graphfile)
	for u, d in G.nodes(data=True):


		#Creating Name Labels
		try:
			name0 = str(d['name']).split('-', 1)[1]
		except:
			print "Exception occurred. Check to see if all names follow DEPT_DEPT-NAME_NAME format. These issues are resolved for file: 'entity_date_multigraph_fx.graphml' in the University of Chicago Network."
			name0 = str(d['name']).split('_', 1)[1].split('_', 1)[0]
			if len(name0) <=4:
				name0 = str(d['name']).split('_', 1)[1].split('_', 1)[1]
			elif len(name0) > 4:
				name0 = str(d['name']).split('_', 1)[1]

		#Full Name - Cleaned
		name = name0.split('.')[0].replace('_', ' ')

		#Creating Department Labels and Groups
		try: 
			dept = str(d['name']).split('-', 1)[0]
			#dept = "("+str(dept0.replace('_', ', '))+")"
			#print dept

		
		except:
			print "Exception occurred. Check to see if all names follow DEPT_DEPT-NAME_NAME format. These issues are resolved for file: 'entity_date_multigraph_fx.graphml' in the University of Chicago Network."

		#Creating Department Group
		dg = str(d['name']).split('-')[0].split('_')[0:1]
		
		for D in dg:

			#Group Religion Labels into Single Department
			if "THEO" in D or "JWSC" in D or "HREL" in D or "HCHR" in D or "ISLM" in D or "HIJD" in D or "RETH" in D or "BIBL" in D or "DVPR" in D:
				dept_group = "THEO"

			#Every Other Department
			else:
				dept_group = str(d['name']).split('-')[0].split('_', 1)[0]


		#dept_group = str(d['name']).split('-')[0].split('_', 1)[0]

		#G.add_node(u, name=str(d['name']), Label=name, Department_Group=dept_group)
		G.add_node(u, name=str(d['name']), Label=str(name+' - '+dept_group), Department_Group=dept_group, Departments=dept)
		#G.remove_node(u)


	outfile = "full_"+_graphfile
	nx.write_graphml(G, outfile)

	#Print Options
	if test == "no":
		edge_list(outfile, True, "Yes")
		pass
	elif test == "test":
		edge_list(outfile, True, "Yes", "print")

#graph_nodes("entity_date_multigraph_fx.graphml")


#____________________________________________________________________#
#                                                                    #
## <---------------       Subgraph Creation        ---------------> ##
#____________________________________________________________________#


def subgraph(graphfile, year, test="no"):
	"""This function creates a subgraph for a given edge year
	Gets the nodes attributes added but has nodes without edges in subgraph
	"""
	
	_graphfile = str(graphfile)
	_year = str(year)

	G=nx.read_graphml(graphfile)
	for u, d in G.nodes(data=True):


		#Creating Name Labels
		try:
			name0 = str(d['name']).split('-', 1)[1]
		except:
			print "Exception occurred. Check to see if all names follow DEPT_DEPT-NAME_NAME format. These issues are resolved for file: 'entity_date_multigraph_fx.graphml' in the University of Chicago Network."
			name0 = str(d['name']).split('_', 1)[1].split('_', 1)[0]
			if len(name0) <=4:
				name0 = str(d['name']).split('_', 1)[1].split('_', 1)[1]
			elif len(name0) > 4:
				name0 = str(d['name']).split('_', 1)[1]

		#Full Name - Cleaned
		name = name0.split('.')[0].replace('_', ' ')

		#Creating Department Labels and Groups
		try: 
			dept = str(d['name']).split('-', 1)[0]
			#dept = "("+str(dept0.replace('_', ', '))+")"
			#print dept

		
		except:
			print "Exception occurred. Check to see if all names follow DEPT_DEPT-NAME_NAME format. These issues are resolved for file: 'entity_date_multigraph_fx.graphml' in the University of Chicago Network."

		#Creating Department Group
		dg = str(d['name']).split('-')[0].split('_')[0:1]
		
		for D in dg:

			#Group Religion Labels into Single Department
			if "THEO" in D or "JWSC" in D or "HREL" in D or "HCHR" in D or "ISLM" in D or "HIJD" in D or "RETH" in D or "BIBL" in D or "DVPR" in D:
				dept_group = "THEO"

			#Every Other Department
			else:
				dept_group = str(d['name']).split('-')[0].split('_', 1)[0]


		#dept_group = str(d['name']).split('-')[0].split('_', 1)[0]

		#G.add_node(u, name=str(d['name']), Label=name, Department_Group=dept_group)
		G.add_node(u, name=str(d['name']), Label=str(name+' - '+dept_group), Department_Group=dept_group, Departments=dept)
		#G.remove_node(u)


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

		SG.add_edge(u, v, date=str(d['date']), entity=str(d['entity']), Label=lb)
		SG.remove_edge(u, v)

	outfile = _year+"_full_multigraph.graphml"
	print "writing subgraph file --> ", outfile
	nx.write_graphml(SG, outfile)

	#Print Options
	if test == "no":
		edge_list(outfile, True, "Yes")
		pass
	elif test == "test":
		edge_list(outfile, True, "Yes", "print")


#subgraph("entity_date_multigraph.graphml", "2003")
#subgraph("entity_date_multigraph_fx.graphml", "2003")
#subgraph("EXPANDED_entity_date_multigraph_fx.graphml", "2004", "test")
#subgraph("EXPANDED_entity_date_multigraph_fx.graphml", "2005")


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

	outfile = _year+"_full_multigraph.graphml"
	nx.write_graphml(SG, outfile)

	#Print Options
	if test == "no":
		edge_list(outfile, True, "Yes")
		pass
	elif test == "test":
		edge_list(outfile, True, "Yes", "print")


