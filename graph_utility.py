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


#____________________________________________________________________#
#                                                                    #
## <---------------       Graph Manipulation       ---------------> ##
#____________________________________________________________________#

def graph_nodes(graphfile, test="no"):
	
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

		G.add_node(u, name=str(d['name']), Label=str(name+' - '+dept_group), Department_Group=dept_group, Departments=dept)

	outfile = "full_"+_graphfile
	nx.write_graphml(G, outfile)

	#Print Options
	if test == "no":
		edge_list(outfile, True, "Yes")
		pass
	elif test == "test":
		edge_list(outfile, True, "Yes", "print")


#____________________________________________________________________#
#                                                                    #
## <---------------       Subgraph Creation        ---------------> ##
#____________________________________________________________________#


def subgraph(graphfile, year, test="no"):
	
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

		G.add_node(u, name=str(d['name']), Label=str(name+' - '+dept_group), Department_Group=dept_group, Departments=dept)


	#Create Subgraph with Edges for Specified Year
	SG=nx.MultiGraph( [ (u,v,d) for u,v,d in G.edges(data=True) if _year in d['date'].split(':', 1)[0]])
		
	#Copy All Nodes and Node Data to Subgraph
	SG.add_nodes_from(G.nodes(data=True))
		
	#Remove Nodes without Edges from Subgraph
	SG.remove_nodes_from((n for n,d in SG.degree_iter() if d==0))

	#Quality Check to Reject Year Inputs Not Found
	if SG.number_of_nodes() < 2:
		#If Nodes < 2 (i.e. year not found)
		return
	else:
		#Keep all other valid subgraphs
		pass

	#Ensure Subgraph Edge Labels Present
	for u,v,d in SG.edges(data=True):

		#Define Label
		lb = str(d['entity']).title().split('|')[1]

		SG.add_edge(u, v, date=str(d['date']), entity=str(d['entity']), Label=lb)
		SG.remove_edge(u, v)

	outfile = "aux_"+_year+"_full_multigraph.graphml"
	print "writing subgraph file --> ", outfile
	nx.write_graphml(SG, outfile)

	#Print Options
	if test == "no":
		edge_list(outfile, True, "Yes")
		pass
	elif test == "test":
		edge_list(outfile, True, "Yes", "print")


