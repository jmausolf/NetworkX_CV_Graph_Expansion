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
		#stats = ['\n'"MULTIGRAPH STATISTICS"'\n', '_'*20, '\n', "Nodes: ", G.number_of_nodes(), '\n', "Edges: ", G.size(), '\n', '_'*20, '\n']
		print '\n'"MULTIGRAPH STATISTICS"'\n', '_'*20, '\n', "Nodes: ", G.number_of_nodes(), '\n', "Edges: ", G.size(), '\n', '_'*20, '\n'
	elif stat=="no":
		pass
	else:
		print "Please input a valid option. Would you like to return the number of edges: 'yes' or 'no'?" 


#edge_list("entity_date_multigraph.graphml", True, "Yes", "pass", "date")
#edge_list("loop_allyears_entity_date_multigraph.graphml", True, "Yes", "print")
#edge_list("2008_multigraph.graphml", True, "Yes", "print")
#edge_list("2008_multigraph.graphml", True, "Yes", "write")
#edge_list("2008_edges_added_multigraph.graphml", True, "Yes", "write")
#edge_list("2008_edges_removed_multigraph.graphml", True, "Yes", "write")



def make_filtered_subgraph(graphfile, year, test="no"):
	"""This function creates a subgraph for a given edge year
	Has correct nodes, but they lack attributes."""

	_graphfile = str(graphfile)
	_year = str(year)

	G=nx.read_graphml(graphfile)
	#SG=nx.MultiGraph( [ (u,v,d) for u,v,d in G.edges(data=True) if _year in d['date'].split(':', 1)[0]])
	SG=nx.MultiGraph( [ (u,v,d) for u,v,d in G.edges(data=True) if _year in d['date'].split(':', 1)[0]])

	outfile = _year+"_multigraph.graphml"
	nx.write_graphml(SG, outfile)

	if test == "no":
		pass
	elif test == "test":
		edge_list(outfile, True, "Yes", "print")



#*****#
#make_filtered_subgraph("entity_date_multigraph.graphml", "1982", "test")
#make_filtered_subgraph("entity_date_multigraph.graphml", "1996", "test")
#make_filtered_subgraph("entity_date_multigraph.graphml", "1995", "test")
#make_filtered_subgraph("entity_date_multigraph.graphml", "1995", "test")
#make_filtered_subgraph("entity_date_multigraph.graphml", "1972", "test")
#make_filtered_subgraph("entity_date_multigraph.graphml", "1977", "test")
#make_filtered_subgraph("entity_date_multigraph.graphml", "1979", "test")
#make_filtered_subgraph("entity_date_multigraph.graphml", "1982", "test")
#make_filtered_subgraph("entity_date_multigraph.graphml", "1989", "test")
#make_filtered_subgraph("entity_date_multigraph.graphml", "2008", "test")
#make_filtered_subgraph("entity_date_multigraph.graphml", "2009", "test")


def make_filtered_subgraph_dev(graphfile, year, test="no"):
	"""This function creates a subgraph for a given edge year
	Gets the nodes attributes added but has nodes without edges in subgraph
	"""
	
	_graphfile = str(graphfile)
	_year = str(year)

	G=nx.read_graphml(graphfile)
	for u, d in G.nodes(data=True):


		#Creating Name Labels
		try:
			name0 = str(d['name']).split('-')[1]
		except: 
			name0 = str(d['name']).split('_', 1)[1].split('_', 1)[0]
			if len(name0) <=4:
				name0 = str(d['name']).split('_', 1)[1].split('_', 1)[1]
			elif len(name0) > 4:
				name0 = str(d['name']).split('_', 1)[1]


		"""
		#Trying to resolve the messed up name deliters
		#Check to see if Bowen's script is fixed.

		try:
			nm = str(d['name']).split('-')
			if len(nm) > 2:
				_name0 = str(d['name']).replace('-', '_')
				print _name0
				try:
					name0 = str(d['name']).split('_', 1)[1].split('_', 1)[0]
					if len(name0) <=4:
						name0 = str(d['name']).split('_', 1)[1].split('_', 1)[1]
					elif len(name0) > 4:
						name0 = str(d['name']).split('_', 1)[1]

			else:
				try:
					name0 = str(d['name']).split('-')[1]
				except: 
					name0 = str(d['name']).split('_', 1)[1].split('_', 1)[0]
					if len(name0) <=4:
						name0 = str(d['name']).split('_', 1)[1].split('_', 1)[1]
					elif len(name0) > 4:
						name0 = str(d['name']).split('_', 1)[1]

		except:
				try:
					name0 = str(d['name']).split('-')[1]
				except: 
					name0 = str(d['name']).split('_', 1)[1].split('_', 1)[0]
					if len(name0) <=4:
						name0 = str(d['name']).split('_', 1)[1].split('_', 1)[1]
					elif len(name0) > 4:
						name0 = str(d['name']).split('_', 1)[1]
		"""

		name = name0.split('.')[0].replace('_', ' ')

		#Creating Department Labels and Groups
		try: 
			dept0 = str(d['name']).split('-')[0]
			dept1 = dept0.replace('_', ' ')
			dept_group = str(d['name']).split('-')[0].split('_', 1)[0]
			#print dept0
			#test = str(d['name']).split('-')[0].split('_', 1)[1]
			#print dept0

			#test = str(d['name']).split('_', 1)[1].split('_', 1)[0]
			#print test
			#test = dept0.split('_', 1)[0]
			#print test
			test = ''
			if len(test) <=4:
				dept = str(d['name']).split('_', 1)[0]
				#print dept
			elif len(test) > 4:
				name0 = str(d['name']).split('_', 1)[1]


			if len(test) <=4:
				test = str(d['name']).split('_', 1)[1].split('_', 1)[1]
				#print test
			elif len(name0) > 4:
				test = str(d['name']).split('_', 1)[1]
			#print dept
		except:
			pass

		#Creating Department Group
		dept1 = str(d['name']).split('-')[0].split('_')[0:1]
		
		for D in dept1:

			#Group Religion Labels in Single Department
			if "THEO" in D or "JWSC" in D or "HREL" in D or "HCHR" in D or "ISLM" in D or "HIJD" in D or "RETH" in D or "BIBL" in D or "DVPR" in D:
				dept_group = "THEO"
				#print dept_group

			#Every Other Department
			else:
				dept_group = str(d['name']).split('-')[0].split('_', 1)[0]
				#print dept_group
		

		#dept_group = str(d['name']).split('-')[0].split('_', 1)[0]

		G.add_node(u, name=str(d['name']), Label=name, Department_Group=dept_group)
		#G.remove_node(u)


	#Create Subgraph with Edges for Specified Year
	SG=nx.MultiGraph( [ (u,v,d) for u,v,d in G.edges(data=True) if _year in d['date'].split(':', 1)[0]])
	
	#Copy All Nodes and Node Data to Subgraph
	SG.add_nodes_from(G.nodes(data=True))
	
	#Remove Nodes without Edges from Subgraph
	SG.remove_nodes_from((n for n,d in SG.degree_iter() if d==0))

	outfile = _year+"_multigraph.graphml"
	nx.write_graphml(SG, outfile)

	#Print Options
	if test == "no":
		edge_list(outfile, True, "Yes")
		pass
	elif test == "test":
		edge_list(outfile, True, "Yes", "print")



#*****#
#make_filtered_subgraph_dev("entity_date_multigraph.graphml", "1996", "test")
#make_filtered_subgraph_dev("entity_date_multigraph.graphml", "1996")
#make_filtered_subgraph_dev("entity_date_multigraph.graphml", "1997")
#make_filtered_subgraph_dev("entity_date_multigraph.graphml", "1998")
