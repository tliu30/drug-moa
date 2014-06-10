###Decide on an algorithm for create sig!!!

import os, sys, time, re
import networkx as nx
from mpmath import factorial, log
from matplotlib import pyplot as plt

default_num_top = 300
default_num_bottom = 300
default_sig_output = os.path.join('..','Sigs')
default_corr_output = os.path.join('..','Corr') 

###Utility functions###

def items(list_a):
    '''creates list of all items in list --> [[1,2][3,4]] to [1,2,3,4]'''
    new = []
    for list_b in list_a:
        for item in list_b:
            new.append(item)
    return new

###

def mean( *nums ):
	"""Returns the mean of the given set of numbers."""

        # ---------------------
        # just use numpy!
        # ---------------------

	total = 0.0
	for num in nums:
		total += float(num)
	return total / float(len(nums))

###

def match(list_1, list_2):
	"""Returns the number of items shared by list_1 and list_2."""

        # -------------------------------
        # can be replaced byset forcing
        # -------------------------------

	match_count = 0
	for item in list_1:
		if item in list_2:
                        match_count += 1
	return match_count

###

def get_top_bottom(filename):
    sig_data = open(filename).readlines()

    cutoff_index = None
    for line_num in range( len(sig_data) ):
        if 'BOTTOM\t' in sig_data[line_num]:
            cutoff_index = line_num
            break

    top = [ line.split('\t')[1].strip().strip('"').strip("'") for line in sig_data[:cutoff_index] ]
    bottom = [ line.split('\t')[1].strip().strip('"').strip("'") for line in sig_data[cutoff_index:] ]

    return top, bottom

###

def add_sig( samp_name, dic, dir_of_sigs ):
	if samp_name not in dic.keys():
		dic[samp_name] = {}
		dic[samp_name]['TOP'], dic[samp_name]['BOTTOM'] = get_top_bottom( os.path.join( dir_of_sigs, samp_name + '.txt' ) )
	return dic

###

def add_fac( samp_name, sig_dic, fac_dic, num_of_total_genes ):
	if samp_name not in fac_dic.keys():
		fac_dic[samp_name] = {}
		fac_dic[samp_name]['TOP'] = factorial( len(sig_dic[samp_name]['TOP']) )
		fac_dic[samp_name]['BOTTOM'] = factorial( len(sig_dic[samp_name]['BOTTOM']) )
		fac_dic[samp_name]['TOT_MIN_TOP'] = factorial( num_of_total_genes - len(sig_dic[samp_name]['TOP']) )
		fac_dic[samp_name]['TOT_MIN_BOTTOM'] = factorial( num_of_total_genes - len(sig_dic[samp_name]['BOTTOM']) )

	return fac_dic

###     
def calc_hgd( query, curr_samp, matches, num_of_total_genes, factorial_total, sig_dic, fac_dic, type ):
	if matches < 1:
		hgd_, hgd_min_one = 0,0
	else:
		hgd_ = hgd(
			num_of_total_genes,
			len( sig_dic[query][type] ),
			len( sig_dic[curr_samp][type] ),
			matches,
			factorial_total,
			fac_dic[query][type],
			fac_dic[curr_samp][type],
			fac_dic[query]['TOT_MIN_' + type],
			fac_dic[curr_samp]['TOT_MIN_' + type] )
		hgd_min_one = hgd(
			num_of_total_genes,
			len( sig_dic[query][type] ),
			len( sig_dic[curr_samp][type] ),
			matches - 1,
			factorial_total,
			fac_dic[query][type],
			fac_dic[curr_samp][type],
			fac_dic[query]['TOT_MIN_' + type],
			fac_dic[curr_samp]['TOT_MIN_' + type] )

	return hgd_, hgd_min_one

###

def neighbors(node, graph):
	nodes = graph.nodes()

	nearby_nodes = [node]
	completed = False

	while not completed:
		completed = True
		for (node_a, node_b) in graph.edges(nbunch = nearby_nodes):
			if node_a not in nearby_nodes:
				nearby_nodes.append(node_a)
				completed = False
			if node_b not in nearby_nodes:
				nearby_nodes.append(node_b)
				completed = False

	return nearby_nodes

###

def GN(graph, num):
	for i in range(num):
		max_btwn_edge = sorted( nx.edge_betweenness_centrality( graph, weighted_edges = True ).items(), key = lambda x: x[1], reverse = True)[0][0]
		graph.remove_edge( max_btwn_edge[0], max_btwn_edge[1] )

	return graph
###

def get_indices(header_items):
	instance_index, smp_index, cmpd_index = None, None, None
	indices = (smp_index, cmpd_index, instance_index)

	for index in range( len(header_items) ):
		item = header_items[index]

		if re.search( r'cmap.name', item, re.IGNORECASE|re.DOTALL):
			cmpd_index = index

		if re.search( r'instance.id', item, re.IGNORECASE|re.DOTALL ):
			instance_index = index

		if re.search( r'cel_file_name', item, re.IGNORECASE ):
			smp_index = index

	indices = (smp_index, cmpd_index, instance_index)

	if (instance_index != None) and (smp_index != None) and (cmpd_index != None):
		return indices

	else:
		print 'Indices unavailable!!!'
		print 'cmpd_index'
		print cmpd_index
		print 'instance_index'
		print instance_index
		print 'smp_index'
		print smp_index
		raise IndexError

###End of utility functions###


def create_sig ( 
	data_file, 
	num_top = default_num_top, 
	num_bottom = default_num_bottom, 
	output_dir = default_sig_output):

###Program description###
	"""
	This function takes normalized gene expression data and creates a gene 
	signature by ranking the genes and then taking the 'x' topmost regulated and
	the 'y' downmost regulated.

	data_file:
		Address of file containing normalized data

		Data file should be formatted so that the gene list runs down the left-most
		column and compound/disease/etc. is along the top-most column

	num_top, num_bottom:
		Number of genes to be included in the top/bottom signatures

	output_dir:
		Output directory.  Defaults to directory where all other sigs are located.
	"""

###Program starts###

        # ---------------------------------------- 
        # Fix data I/O - switch to CSV library
        # (That stuff is more flexible than my code)
        # ---------------------------------------- 

	expression_data = open( data_file )
	header = expression_data.readline().strip().split('\t')
	titles = [ ( header[column_num].strip('"').strip("'").strip(), column_num) for column_num in range( 1, len(header) ) ]
		###Creates list containing header data (name of cmpd/disease, etc described)
		###Then, associates each data item with a column number
	num_diff_items = len(titles) ###Number of diff header items
	num_done = 0 ###Keeps track of number of items completed

	print '%i items\n'%(num_diff_items)

        # ------------------------
        # What is this?! v (down there)
        # ------------------------


	start_of_data = expression.tell()
		###Index at which the data table (past the header) begins


	###Iterate across each title -> open file, rank data, pull out ranks, put in files
	for ( title, column_num) in titles:
            # -------------------------------------------------------------------------------
            # There's got to be a more efficient way to track this info / take care of ties
            # Steps:
            #  1) Read each row
            #  2) Sort row
            #  3) Find thresh scores
            #  4) IF ORDERING DOESN'T MATTER - just do a single pass!
            # Compare the efficiency of sorting thresh scores, then examining indices to get
            # genes & compare against zipping together genes and scores
            # Also...find more efficient way than forcing myself to read columns (transpose docs?)
            # -------------------------------------------------------------------------------

		title_data = []
		for row in expression_data:
			row = row.strip().replace('"', '').replace("'", '').replace('\r', '').split('\t')
				###Some quick editing to remove whitespace and quotes

			gene_name = row[0] ###Gene assoc with row's data
			data_point = float( row[column_num] )
				###Normalized expression data of that gene and that cmpd/disease/etc

			title_data += [ ( data_point, gene_name ) ]
				###Record data (and assoc gene) to list

		###Primary algorithm (Counts top/bottom number of genes)
		title_data.sort( reverse = True )
		ranked_gene_list = [ gene_name for (data_point, gene_name) in title_data ]
			###Sorts list by data point and extracts associated gene names in order
		top = ranked_gene_list[ :num_top ]
		bottom = ranked_gene_list[ -num_bottom: ]

		###Secondary algorithm (accounts for possibility of genes with equal (Counts top/bottom number of data points)
		title_data.sort( reverse = True )
		data_points_only = {}.fromkeys( [ data_point for ( data_point, gene_name ) in title_data ] ).keys()
		data_points_only.sort( reverse = True )
		
		top, bottom = [], []
		for ( data_point, gene_name ) in title_data:
			if data_point >= data_points_only[ num_top - 1 ]:
				top.append( gene_name )
			elif data_point <= data_points_only[ -num_bottom ]:
				bottom.append( gene_name )
		###############################################

                # -------------------------------------------------------------------------------
                # Rather than outputting each individually, create matrix?
                # Once again, see if ordering matters
                # -------------------------------------------------------------------------------

		###Now, to output to a file
		output_file = open( os.path.join( output_dir, title.upper().replace( '.CEL', '') ) + '.txt', 'w' )
		output_file.write( 'TOP\t' )
		output_file.write( '\n\t'.join( top ) )
		output_file.write( '\nBOTTOM\t' )
		output_file.write( '\n\t'.join( bottom ) )
		output_file.close()

		###Reset to start of data
		expression_data.seek( start_of_data )
		###

		num_done += 1
		print  '%s - %s (%i of %i)'%(os.path.basename(data_file), title, num_done, num_total )
		print '\nDONE\n'

		return None



def hgd (
	total_population,
	sample_1,
	sample_2,
	matches,
	f_total = None, 
	f_samp_1 = None, 
	f_samp_2 = None, 
	f_total_minus_samp_1 = None, 
	f_total_minus_samp_2 = None):

###Program description###
	"""
	This function takes the given data and calculates the hypergeometric distribution.

	total_population:
		The entire population

	sample_1, sample_2:
		The size of the two samples

	matches:
		The number of common items.

	f_total, f_samp_1, f_samp_2, f_total_minus_samp_1, f_total_minus_samp_2:
		The factorial values, if they've been precalculated.
	"""

###Program starts###
	
	###To cover, if values were not precalculated###
	if not f_total:
		f_total = factorial( total_population )
	if not f_samp_1:
		f_samp_1 = factorial( sample_1  )
	if not f_samp_2:
		f_samp_2 = factorial( sample_2 )
	if not f_total_minus_samp_1:
		f_total_minus_samp_1 = factorial( total_population - sample_1 )
	if not f_total_minus_samp_2:
		f_total_minus_samp_2 = factorial( total_population - sample_2 )
	######

	probability = ( ( f_samp_1 * f_samp_2 * f_total_minus_samp_1 * f_total_minus_samp_2 ) / ( f_total * factorial(matches) * factorial( sample_1 - matches ) * factorial( sample_2 - matches ) * factorial( total_population - sample_1 - sample_2 + matches) ) )

	return probability



###Do I still need the name_descriptor file here?###
def calc_correlations(
	query,
	dir_of_sigs,
	num_of_total_genes,
	output_dir = default_corr_output,
	temp = False):

###Program description###
	"""
	Takes one signature and compares it against the signatures for the other samples
	found in the output directory.
	If it is not a temp, it will also copy these values to the existing correlation data sheets.

	query:
		Name of query

	dir_of_sigs:
		Location of signature files

	num_of_total_genes:
		Self-explanatory

	output_dir:
		Where to output the correlation file.  Also, where the other correlation files are.
	"""

###Program starts###
	os.chdir( dir_of_sigs )

	output_file = open( os.path.join( output_dir, query + '.txt' ), 'w' )
	output_file.write( '\tTOP\tBOTTOM\tOVERALL' )   ###Keep header?  Or remove header?

	samps = [ os.path.splitext(file)[0] for file in os.listdir(output_dir) ]
	
	stored_sigs, stored_samp_facs = {}, {}
	stored_sigs = add_sig( query, stored_sigs, dir_of_sigs )
	stored_samp_facs = add_fac( query, stored_sigs, stored_samp_facs, num_of_total_genes )
	factorial_total = factorial( num_of_total_genes )
		###To save sig lists and factorials, to reduce computations
	num_left = len( samps )

	print num_left

	while samps:
		curr_samp = samps.pop(0)
		if 'DS_Store' in curr_samp or query in curr_samp:
			num_left -= 1
			continue

		stored_sigs = add_sig( curr_samp, stored_sigs, dir_of_sigs )
		stored_samp_facs = add_fac( curr_samp, stored_sigs, stored_samp_facs, num_of_total_genes )

		top_matches =  match( stored_sigs[query]['TOP'], stored_sigs[curr_samp]['TOP'] )
		bottom_matches = match( stored_sigs[query]['BOTTOM'], stored_sigs[curr_samp]['BOTTOM'] )

		###Now, to calculate the hypergeometric distributions
		top_hgd, top_hgd_min_one = calc_hgd( query, curr_samp, top_matches, num_of_total_genes, factorial_total, 
			stored_sigs, stored_samp_facs, 'TOP')
		bottom_hgd, bottom_hgd_min_one = calc_hgd( query, curr_samp, bottom_matches, num_of_total_genes, factorial_total, 
			stored_sigs, stored_samp_facs, 'BOTTOM')

		###Now to calculate correlation values (logs of hgd's) based on hgd's
		###[If hgd's are such that are on increasing part of curve, are ignored and default to 0]

                # ----------------------------------------
                # I ought to look at the theory again to
                # understand why we're ignoring the HGD
                # if the derivative is positive
                # ----------------------------------------

		top_corr, bottom_corr, overall_corr = 0, 0, 0

		if (top_hgd_min_one - top_hgd) > 0:
			top_corr = -log( top_hgd )
		if (bottom_hgd_min_one - bottom_hgd) > 0:
			bottom_corr = log( bottom_hgd)
			if top_corr != 0:
				overall_corr = mean( abs(top_corr), abs(bottom_corr) )

		###And now to output
		output_file.write( '\n' + curr_samp + '\t' + str(top_corr) + '\t' + str(bottom_corr) + '\t' + str(overall_corr) )

		###Create the condition:
		if not temp:
			open( os.path.join( output_dir, curr_samp + '.txt' ), 'a' ).write( 
				'\n' + query + '\t' + str(top_corr) + '\t' + str(bottom_corr) + '\t' + str(overall_corr) )
		###

		num_left -= 1
		if num_left%1000 == 0:
			print num_left

		if num_left < 1000:
			if num_left%100 == 0:
				print num_left

	output_file.close()

	return None



###Graphing functions###
def query_cmpd(
	query, 
	dir_of_corr, 
	output_dir,
	name_descriptor_file,
	cutoff,
	finish_point,
	mode = 3):

###Program description###
	"""
	This function starts at the query compound, and draws edges connecting it
	with any compound/disease/etc that has a correlation above the cutoff.  It then 
	expands to construct a network, examining each connected cmpd for more connections.

	After a graph is drawn, the function then utilizes the girvan-newman algorithm
	to begin trimming down edges, and hopefully eventually identifying a community.
	The program outputs a graph at each stage of edge removal that produces a new community
	so that further analysis can be performed.
	"""

###Program  starts###
	if name_descriptor_file:
		name_dict = extract_names(name_descriptor_file)
	else:
		name_dict = None

	###Begin constructing the initial graph (pre cutting edges)###
	print 'Creating initial graph...'

	graph = nx.Graph()
	num_edges = 0

	items_to_visit, items_visited = [query], []
	while items_to_visit:
		curr_samp = items_to_visit.pop(0)
                if curr_samp in items_visited:
                        continue

		if name_dict:
			graph.add_node( name_dict[curr_samp], samp_id = curr_samp )

		samp_corr = open( os.path.join( dir_of_corr, curr_samp + '.txt' ) ).readlines()[1:]
		for line in samp_corr:
			other_samp = line.strip().replace('"', '').replace("'", '').split('\t')[0]
                        corr = abs(float(line.strip().replace('"', '').replace("'", '').split('\t')[mode]))

                        if corr >= cutoff:
                                if other_samp not in items_visited:
                                        if name_dict:
                                                graph.add_node( name_dict[other_samp], samp_id = other_samp )
                                                graph.add_edge( name_dict[curr_samp], name_dict[other_samp], weight = corr )
                                        else:
                                                graph.add_edge( curr_samp, other_samp, weight = corr )

                                        num_edges += 1
                                        if num_edges%100 == 0:
                                                print str(num_edges) + '\t' + str(len(items_visited)) + '\t' + str(len(items_to_visit))
                                                
                                        items_to_visit.append(other_samp)

		items_visited.append(curr_samp)
	###Hooray!  Graph has been created :) ###
	###Next step is to apply Girvan-Newman to remove extraneous edges###
	print '\nApplying Girvan-Newman...'	
	
	curr_size = len( graph.nodes() )
	prev_size = 0
	while curr_size > finish_point:
		if curr_size != prev_size:
			###Output###
			table = open( os.path.join( output_dir, str(curr_size).zfill(5) + '.txt' ), 'w' )
			table.write( 'Compounds\n' )

			rows = []
			for node in graph:
                                row = '\n' + node
                                if name_dict:
                                        row += '\t' + graph.node[node]['samp_id']
                                rows.append( row )
                        table.writelines(sorted(rows))

			plt.cla()
			nx.draw_spring(graph)
			plt.savefig( os.path.join( output_dir, str(curr_size).zfill(5) + '.png' ))
			###Output done###

                        print curr_size

                graph = GN(graph, 1)

                if name_dict:
                        comm = neighbors( name_dict[query], graph )
                        
                        a = nx.Graph()
                        a.add_nodes_from( [ (node, graph.node[node]) for node in comm ] )
                        a.add_weighted_edges_from([ (node_a, node_b, attr_dict['weight']) for (node_a, node_b, attr_dict) in graph.edges( nbunch = comm, data = True)])

                        graph = a
                else:
                        graph = nx.Graph( data = graph.edges( nbunch = neighbors(query, graph), data = True ) )

                prev_size = curr_size
		curr_size = len( graph.nodes() )

                print str(curr_size) + '\t' + str(len(graph.edges()))
	###When reaches here, curr_size has gone below finish point.  We are done.

	return None

def whole_network( dir_of_corr, cutoff, output_directory, name_descriptor_file = None, mode = 3):
        if name_descriptor_file:
                name_dict = extract_names(name_descriptor_file)
        else:
                name_dict = None

        items_to_visit = [ os.path.splitext(corr_file)[0] for corr_file in os.listdir( dir_of_corr ) ]

        graph = nx.Graph()
        num_edges = 0
    
        while items_to_visit:
                curr_samp = items_to_visit.pop(0)
                if not os.path.isfile( os.path.join(dir_of_corr, curr_samp + '.txt') ):
                        continue

                samp_corr = open( os.path.join(dir_of_corr, curr_samp + '.txt') ).readlines()[1:]
                for line in samp_corr:
                        other_samp = line.strip().replace('"', '').replace("'", '').split('\t')[0]
                        corr = abs(float(line.strip().replace('"', '').replace("'", '').split('\t')[mode]))

                        if corr >= cutoff:
                                if other_samp in items_to_visit: #i.e., if other_samp yet to be visited
                                        if name_dict:
                                                graph.add_node( name_dict[curr_samp], curr_id = curr_samp )
                                                graph.add_node( name_dict[other_samp], samp_id = other_samp )
                                                graph.add_edge( name_dict[curr_samp], name_dict[other_samp], weight = corr )
                                        else:
                                                graph.add_edge( curr_samp, other_samp, weight = corr )

                                        num_edges += 1
                                        if num_edges%25 == 0:
                                                print str(num_edges) + '\t' + str(len(items_to_visit))

        print 'Graph drawn...'

        init_edges = len(graph.edges())
        nodes = graph.nodes()

        print """\nInitial number of edges: %i\nInitial number of nodes: %i\n"""%( init_edges, len(nodes) )

        prev_comm = []
        communities = []

        while len(prev_comm) < len(nodes):
                for node in nodes:
                        if node not in items(communities):
                                communities.append( neighbors( node, graph ) )

                communities.sort( key = len, reverse = True )

                if communities != prev_comm:
                        communities.sort( key = len, reverse = True)

                        if not os.path.exists( os.path.join(output_directory, str(len(graph.edges())).zfill(8) ) ):
                                os.mkdir( os.path.join(output_directory, str(len(graph.edges())).zfill(8)) )
                                
                        f = open( os.path.join( output_directory, str(len(graph.edges())).zfill(8), str(len(graph.edges())).zfill(8) + '.txt' ), 'w' )
                        rows = {}
                        header = []

                        for index in range( len(communities)):
                                comm = communities[index]
                                if len(comm) > 1:
                                        comm_graph = nx.Graph()
                                        comm_graph.add_nodes_from( [ (node, graph.node[node]) for node in comm ] )
                                        comm_graph.add_weighted_edges_from([ (node_a, node_b, attr_dict['weight']) for (node_a, node_b, attr_dict) in graph.edges( nbunch = comm, data = True)])
                                        
                                        plt.cla()
                                        nx.draw_spring(comm_graph)
                                        plt.savefig( os.path.join(output_directory, str(len(graph.edges())).zfill(8), str(len(graph.edges())).zfill(8) + '_' + str(index).zfill(3) + '.png') )
                                        
                                        header.append( str(len(graph.edges())).zfill(8) + '_' + str(index).zfill(3) )
                                else:
                                        header.append('')
                                        
                                for index in range( len(comm) ):
                                        if not rows.has_key(index):
                                                rows[index] = [ comm[index] ]
                                        else:
                                                rows[index].append( comm[index] )

                                for index in range( len(comm), len(rows.keys()) ):
                                        rows[index].append( '' )

                        f.write( '\t'.join(header) + '\n' ) 
                        f.write( '\n'.join( ['\t'.join(rows[row]) for row in range(len(rows.keys()) ) ] ) )
                        f.close()

                        plt.cla()
                        nx.draw_spring(graph)
                        plt.savefig( os.path.join( output_directory, str(len(graph.edges())).zfill(8), str( len( graph.edges() ) ).zfill(8) + '.png'))

                prev_comm = communities
                communities = []

                print len(graph.edges())
                if len(graph.edges()) > 0:
                    graph = GN(graph, 1)

        return None

###A couple functions for database creation###

def dev_pairs(dir_of_sigs):

###Program description###
	"""
	Takes a set of sigs and develops a list of pairs
	so that correlations can be processed by multiple processes
	without worries of misoverlap, etc.
	"""

###Program starts
	sig_list = [os.path.splitext(sig)[0]  for sig in os.listdir( dir_of_sigs )]
	if not os.path.exists( os.path.join( dir_of_sigs, 'PAIRS' ) ):
		os.mkdir( os.path.join( dir_of_sigs, 'PAIRS' ) )

	file_count = 1
	pair_count = 0
	curr_pair_file = open( os.path.join( dir_of_sigs, 'PAIRS', str(file_count).zfill(4) + '.pr' ), 'w' )
	while sig_list:
		curr_sig = sig_list.pop(0)
		for other_sig in sig_list:
			curr_pair_file.write( '%s|||%s\n'%(curr_sig, other_sig) )
			pair_count += 1
			if pair_count > 10000:
				curr_pair_file.close()
				file_count += 1
				curr_pair_file = open( os.path.join( dir_of_sigs, 'PAIRS', str(file_count).zfill(4) + '.pr' ), 'w' )
                                print pair_count * file_count
                                pair_count = 0
	curr_pair_file.close()

	return None



def calc_corr_from_pairs(
	list_of_pair_files,
	dir_of_sigs,
	num_of_total_genes,
	output_dir = default_corr_output):

###Program description###
	"""
	Takes a list of paired signatures and cross-compares to create a
	database of correlation data.

	list_of_pair_files:
		Path to said pair files

	dir_of_sigs:
		Location of signature files

	num_of_total_genes:
		Self-explanatory

	output_dir:
		Where to output the correlation file.  Also, where the other correlation files are.
	"""

###Program starts###
	os.chdir( dir_of_sigs )

	stored_sigs, stored_samp_facs = {}, {}
        stored_sigs = {}
	factorial_total = factorial( num_of_total_genes )
	num_left = len(list_of_pair_files) * 10000

	print num_left
	for pair_file in list_of_pair_files:
		curr_pair_file = open(pair_file)

		for pair in curr_pair_file:
			curr_samp, other_samp = pair.strip().split('|||')

			for samp in curr_samp, other_samp:
				stored_sigs = add_sig( samp, stored_sigs, dir_of_sigs )
				stored_samp_facs = add_fac( samp, stored_sigs, stored_samp_facs, num_of_total_genes )

			top_matches =  match( stored_sigs[curr_samp]['TOP'], stored_sigs[other_samp]['TOP'] )
			bottom_matches = match( stored_sigs[curr_samp]['BOTTOM'], stored_sigs[other_samp]['BOTTOM'] )

			###Now, to calculate the hypergeometric distributions
			top_hgd, top_hgd_min_one = calc_hgd( curr_samp, other_samp, top_matches, num_of_total_genes, factorial_total, 
				stored_sigs, stored_samp_facs, 'TOP')
			bottom_hgd, bottom_hgd_min_one = calc_hgd( curr_samp, other_samp, bottom_matches, num_of_total_genes, factorial_total, 
				stored_sigs, stored_samp_facs, 'BOTTOM')

			###Now to calculate correlation values (logs of hgd's) based on hgd's
			###[If hgd's are such that are on increasing part of curve, are ignored and default to 0]
			top_corr, bottom_corr, overall_corr = 0, 0, 0

			if ( top_hgd_min_one - top_hgd > 0 ):
				top_corr = -log( top_hgd )
			if (bottom_hgd_min_one - bottom_hgd > 0):
				bottom_corr = log( bottom_hgd)
				if top_corr != 0:
					overall_corr = mean( abs(top_corr), abs(bottom_corr) )
				
			###And now to output
			for samp in curr_samp, other_samp:
				if not os.path.exists( os.path.join( output_dir, samp + '.txt' ) ):
					open( os.path.join( output_dir, samp + '.txt' ), 'w' ).write( '\tTOP\tBOTTOM\tOVERALL' )
			open( os.path.join( output_dir, curr_samp + '.txt' ), 'a' ).write( '\n' + other_samp + '\t' + str(top_corr) + '\t' + str(bottom_corr) + '\t' + str(overall_corr) )
			open( os.path.join( output_dir, other_samp + '.txt' ), 'a' ).write( '\n' + curr_samp + '\t' + str(top_corr) + '\t' + str(bottom_corr) + '\t' + str(overall_corr) )
			
                        num_left -= 1
			print num_left
			###Done!

	return None

def consolidate( dirs_of_corr_files, output_dir = None ):
        if not output_dir:
                output_dir = dirs_of_corr_files[0]
        if not os.path.exists(output_dir):
                os.mkdir(output_dir)
                
	files_held = {}
	
	for corr_dir in dirs_of_corr_files:
		for corr_file in os.listdir(corr_dir):
			if not files_held.has_key(corr_file):
				files_held[corr_file] = []
			files_held[corr_file].append(corr_dir)

	for corr_file in files_held.keys():
		data = ['\tTOP\tBOTTOM\tOVERALL']
		for corr_dir in files_held[corr_file]:
			data += [ '\n' + line for line in open( os.path.join( corr_dir, corr_file ) ).read().strip().split('\n')[1:] ]
                print corr_file
                
		open( os.path.join( output_dir, corr_file ), 'w').writelines(data)

        ###Cleanup files (currently lack permissions?)###
#	for dirk in dirs_of_corr_files:
 #               if dirk != output_dir:
  #                      for f in os.listdir(dirk):
   #                             os.chdir(dirk)
    #                            os.remove(f)
     #                   os.chdir('..')
      #                  os.remove(os.path.abspath(dirk))

	return None
#########################

###Now, to create the top-level runtime query functions###
def query( 
	query_samp, 
	query_name,
	dir_of_sigs, 
	dir_of_corr,
	name_descriptor_file,
	num_of_total_genes,
	graph_output = None,
	cutoff = None,
	finish_point = None,
	temp = False ):

###Program description###
	"""
	This function takes a new query and can do one of three things:
		a) add to database and graph it
		b) add to database and don't graph it
		c) don't add to database, but graph it

	query_samp:
		Location of query data.

	query_name:
		Identifying name of query_samp.

	dir_of_sigs:
		Directory containing signature database.

	dir_of_corr:
		Directory containing correlation data database.

	num_of_total_genes:
		The number of genes in the population.
	
	name_descriptor_file:
		File linking sample names and actual names.

	graph_output:
		Where to output the graph; defaults to None.

	cutoff:
		Correlation cutoff (for graphing).

	finish_point:
		The point at which the program should stop paring down edges.
		(for graphing)

	temp:
		Whether to add to database or not; defaults to adding to database.
	"""

###Program starts###
	
	query = os.path.splitext( os.path.split( query_samp )[1] )[0]
	open( os.path.join(dir_of_sigs, query + '.txt'), 'w' ).write( open( query_samp ).read() )
	###Step 1: Adjust name info to include new sample###
	name_descriptor_file = add_name( query, query_name, name_descriptor_file, temp )
	
	###Step 2: Create signature
#	create_sig ( query_samp, default_num_top, default_num_bottom, dir_of_sigs)

	###Step 3: Calc correlations
        print 'Calculating correlation data...'
	calc_correlations( query, dir_of_sigs, num_of_total_genes, dir_of_corr, temp)
	
	###Finally, graph, if needed
	if graph_output:
		query_cmpd( query,  dir_of_corr, graph_output, name_descriptor_file, cutoff, finish_point, mode = 3)

	###And clean up if was a temp
	if temp:
		os.remove( name_descriptor_file )
		os.remove( os.path.join( dir_of_sigs, query + '.txt' ) )
		os.remove( os.path.join( dir_of_corr, query + '.txt' ) )

	return None
#####################


###Functions for converting meaningless sample names to compound names###
def add_name_from_file( name_descriptor_file, output_file ):
	names = [ line.strip().split('\t') for line in open( name_descriptor_file ).readlines() ]
	header, names = names[0], names[1:]
	
	smp_index, cmpd_index, instance_index = get_indices(header)

	output_file = open( output_file, 'a' )
	name_list = []
	for line in names:
		name_list.append( line[smp_index].upper().replace('.CEL','') + '\t' + '_'.join( [line[cmpd_index].upper(), line[instance_index].upper()] ) )

	output_file.write('\n'.join(name_list))
	output_file.close()

	return None


def add_name( samp_name, cmpd_name, name_descriptor_file, temp = False ):
        data = open(name_descriptor_file).read()
        data += '\n' + samp_name + '\t' + cmpd_name
        if temp:
                name_descriptor_file = os.path.join( os.path.split(name_descriptor_file)[0], 'TEMP_' + os.path.split(name_descriptor_file)[1])
	open(name_descriptor_file,'w').write(data)

	return name_descriptor_file


def extract_names (name_descriptor_file): 
	names = [ line.split('\t') for line in open(name_descriptor_file).read().strip().split('\n') ]

	name_dict = {}
	for (samp_name, cmpd_name) in names:
		name_dict[ samp_name ] = cmpd_name

	return name_dict
#######################

if __name__ == '__main__':
    for arg in sys.argv[1:]: #First item in sys.argv is program itself
        Rank_and_Sig ( arg )
