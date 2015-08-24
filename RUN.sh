##################################
###                            ###
###      Joshua G. Mausolf     ###
###    Computation Institute   ###
###    University of Chicago   ###
###                            ###
##################################


## ______________ 1st Stage - Run NetworkX Graph Program _______________ ##

python __main.py



## ______________ 2nd Stage - Organize Created Files _______________ ##

mkdir Source_Files
mkdir Expanded_Graphs
mkdir Expanded_Graphs/Yearly_Subgraphs
mkdir Expanded_Graphs/Full_Multigraph
mkdir Auxillary_Graphs
mkdir Auxillary_Graphs/Yearly_Subgraphs
mkdir Auxillary_Graphs/Other_Graphs


mv *aux_* Auxillary_Graphs/Yearly_Subgraphs
mv *19* Expanded_Graphs/Yearly_Subgraphs
mv *20* Expanded_Graphs/Yearly_Subgraphs


## ______________ 3rd Stage - Clean Source Files _______________ ##

#mv entity_date_multigraph.graphml Source_Files
#mv entity_date_multigraph_fx.graphml Source_Files