from Tkinter import *
print 'Importing additional dialogs...'
from tkSimpleDialog import askstring
from ScrolledText import ScrolledText
from tkMessageBox import askyesno, showwarning
import tkMessageBox, tkFileDialog
import os

print 'Importing basic functions from CreateSig...'
import CreateSig


DEFAULT_DIR = os.path.abspath('.\\Database')
DIRECT = True

########## Utility functions #################

def rev_dict(dictionary):
	"""
	Takes original dictionary, where
		d[key] = value
	and turns into dictionary where
		d[value] = (each key for which d[key] = value)
	"""
	new_d = {}
	for key in dictionary.keys():
		value = dictionary[key]
		if not new_d.has_key(value):
			new_d[value] = []
		new_d[value].append(key)
		
	return new_d
	

def mktable( *columns ):
	'''
	Takes columns in the form of lists
	and formats data into a table with even
	row and column lengths.
	'''
	output = ''
	col_len = max( len(x) for x in columns )
	row_len = 1
	table_cols = []
	
	for column in columns:
		
		### Normalize column length, so that each column is same length ####
		if len(column) < col_len:
			column += [''] + (col_len - len(column))
		######################################################
		
		### Note longest item in column and then normalize item length ######
		max_len = max( len(x) for x in column ) + 3 
		table_cols.append( ['   ' + x.ljust(max_len) + '|' for x in column] )
		#####################################################################
		
		row_len += max_len + 1 + 3
	
	columns = table_cols
	for i in range(col_len):
		output += '-'*row_len + '\n|'
		for column in columns:
			output += column[i]
		output += '\n'
	output += '_' * row_len
	return output, row_len
		
###########################################################################



########## Custom widgets ####################

class Listbox_w_Scroll:
	def __init__(self, master, width = 20):
		self.frame = Frame(master)
		self.scrollbar = Scrollbar(self.frame)
		self.scrollbar.pack(side = RIGHT, fill = Y, expand = 1)
		self.listbox = Listbox(self.frame, yscrollcommand = self.scrollbar.set, width = width)
		self.listbox.pack(side = LEFT, fill = BOTH, expand = 1)
		self.scrollbar.config(command = self.listbox.yview)
	
	def insert(self, index, *items):
		self.listbox.insert(index, *items)

	def get(self, index):
		return self.listbox.get(index)

	def curselection(self):
		return self.listbox.curselection()

	def delete(self, first, last = None):
		return self.listbox.delete(first, last)

	def bind(self, sequence = None, func = None, add = None):
		return self.listbox.bind(sequence, func, add)

	def pack(self, **options):
		return self.frame.pack(**options)

	def activate(self, index):
		return self.listbox.activate(index)

	def selection_clear(self, first, last = None):
		return self.listbox.selection_clear(first, last)

	def selection_set(self, first, last = None):
		return self.listbox.selection_set(first, last)

	def see(self, index):
		return self.listbox.see(index)
		
#####################################################


########## Custom dialogs ###################################

class AddItemDialog:
	def __init__(self, database, parent = None):
		self.parent = parent
		self.root = Toplevel(parent)
		self.root.title('Add Item')
		self.database = database
		self.numtotal_default = '22277'  ###Find a way to get numtotal more mutable
		self.name_descriptor_file = os.path.join(database, 'Names.txt') ##Fix for filename
		
		self.query_loc = {  'desc': Label(self.root, text = 'Location of query: ', anchor = E),
							'entry': Entry(self.root),
							'button': Button(self.root, text = 'Browse', command = self.browse_query)       }
		self.query_name = { 'desc': Label(self.root, text = 'Compound/Disease/etc. name: ', anchor = E),
							'entry': Entry(self.root)       }
		self.numtotal = {'desc': Label(self.root, text = 'Number of Total Genes', anchor = E),
							'entry': Entry(self.root)       }

		self.query_loc['desc'].grid(row = 0, column = 0, columnspan = 2)
		self.query_loc['entry'].grid(row = 0, column = 2)
		self.query_loc['button'].grid(row = 0, column = 3)
		self.query_name['desc'].grid(row = 1, column = 0, columnspan = 2)
		self.query_name['entry'].grid(row = 1, column = 2)
		self.numtotal['desc'].grid(row = 2, column = 0, columnspan = 2)
		self.numtotal['entry'].grid(row = 2, column = 2)

		self.numtotal['entry'].insert(END, self.numtotal_default)

		Button(self.root, text = 'Ok', command = self.run).grid(row = 3, column = 2)
		Button(self.root, text = 'Cancel', command = self.root.destroy).grid(row = 3, column = 3)

		if parent:
			self.parent.wait_window(self.root)
		
	def browse_query(self):
		filename = tkFileDialog.askopenfilename()
		self.query_loc['entry'].delete(0, END)
		self.query_loc['entry'].insert(0, filename)
		
		return None
		
	def run(self):
		query_loc = self.query_loc['entry'].get()
		query_name = self.query_name['entry'].get()
		sample_name = os.path.splitext( os.path.split(query_loc)[1] )[0]
		numtotal = int(self.numtotal['entry'].get())
		
		### Check for missing times ##############################
		if not query_name or not sample_name or not query_loc:
			tkMessageBox.showwarning( title = 'Error', message = 'Missing information!' )
			return None

		if not os.path.exists( query_loc ):
			tkMessageBox.showwarning( title = 'Error', message = '%s does not exist!'%(item) )
			return None
		###########################################################

		print '\nAdding %s to database...'%(query_name)
		CreateSig.add_name( sample_name, query_name, self.name_descriptor_file )
		open( os.path.join(self.database, 'Sigs', sample_name + '.txt'), 'w' ).write( open(query_loc).read() )
		print 'Calculating correlations...'
		CreateSig.calc_correlations( sample_name, os.path.join(self.database, 'Sigs'), numtotal, os.path.join(self.database, 'Corr') )
                print 'Ok...%s added to database.'%(query_name)
		self.root.destroy()
		return None
		
class ChooseDBDialog:
	def __init__(self, default = DEFAULT_DIR):
                if DIRECT:
                        print '\nStarting database editor...'
                        DBView(DEFAULT_DIR)

                else:
                        print '\nChoose directory for database editor...'
                        self.root = Toplevel()
                        self.root.title('View database')
                        
                        self.db_loc = {  'desc': Label(self.root, text = 'Location of database: ', anchor = E),
                                                                'entry': Entry(self.root),
                                                                'button': Button(self.root, text = 'Browse', command = self.browse_db)       }

                        self.db_loc['desc'].grid(row = 0, column = 0, columnspan = 2)
                        self.db_loc['entry'].grid(row = 0, column = 2)
                        self.db_loc['button'].grid(row = 0, column = 3)

                        Button(self.root, text = 'Ok', command = self.run).grid(row = 3, column = 2)
                        Button(self.root, text = 'Cancel', command = self.root.destroy).grid(row = 3, column = 3)

                        if default:
                                self.db_loc.insert(0, default)
		
	def browse_db(self):
		filename = tkFileDialog.askdirectory()
		self.db_loc['entry'].delete(0, END)
		self.db_loc['entry'].insert(0, filename)
		
		return None
		
	def run(self):
		db_loc = self.db_loc['entry'].get()
		if not os.path.exists( db_loc ):
			tkMessageBox.showwarning( title = 'Error', message = '%s does not exist!'%(item) )
			return None
		
		self.root.destroy()

		print 'Starting database editor...'
		DBView(db_loc)
		return None

###############################################################


############ Main window ######################################

class DBView:
	def __init__(self, database, parent = None):
                print 'Initializing viewer...'
		self.parent = parent
		self.database = database
		print 'Loading files...'
		self.db_samps = [os.path.splitext(item)[0] for item in os.listdir( os.path.join(database, 'Corr') )]
		self.name_dict_samp_to_cmpd = CreateSig.extract_names( os.path.join(database, 'Names.txt') )
		self.name_dict_cmpd_to_samp = rev_dict(self.name_dict_samp_to_cmpd)
		self.mode = 'CMPD' #Describes which type of name is displayed on the list
                print 'Curr mode: %s'%(self.mode)
		self.keys = sorted( [self.name_dict_samp_to_cmpd[item] for item in self.db_samps] )
		self.curselection = None

		if not parent:
                        self.root = Toplevel()
                else:
                        self.root = Toplevel(parent)
                self.root.title('Database Viewer - %s'%(self.database))
		Label(self.root, text = self.database).pack(side = TOP, pady = 20)

		self.search_frame = Frame(self.root)
		Label(self.search_frame, text = 'Search: ').pack(side = LEFT)
		self.search = Entry(self.search_frame)
		self.search.pack(side = RIGHT)
		self.search.bind( '<Key>', self.scroll )
		self.search_frame.pack(side = TOP)

		self.sample_list = Listbox_w_Scroll(self.root, width = 40)
		self.sample_list.pack(side = TOP, padx = 60, pady = 20)
		self.sample_list.bind( '<Return>', self.get_item )
		self.sample_list.bind( '<Button-1>', self.get_item )
		
		self.info = Frame(self.root)
		self.info_box = {       'label' : Label(self.info, text = '', anchor = W, justify = LEFT),
							'delitem' : Button(self.info, text = 'Delete Item', command = self.delete_item),
							'changename': Button(self.info, text = 'Change Name', command = self.changename, state = DISABLED),
							'view' : Button(self.info, text = 'View', command = self.view) }
		self.info_box['label'].grid(row = 0, column = 0, rowspan = 3, sticky = W+E+N+S, padx = 5)
		self.info_box['delitem'].grid(row = 0, column = 1, sticky = W+E)
		self.info_box['changename'].grid(row = 1, column = 1, sticky = W+E)
		self.info_box['view'].grid(row = 2, column = 1, sticky = W+E)
		self.info.pack(side = TOP)
		
		Button(self.root, text = 'Change Mode', command = self.changemode).pack(side = TOP)
		Button(self.root, text = 'Add Items', command = self.add_item).pack(side = TOP)

		print 'Ok...set up complete.'
		self.fill()
		self.sample_list.selection_set(0)
		self.get_item()
		if parent:
			self.parent.wait_window(self.root)
		
	def fill(self):
                print '\nLoading list...'
		self.sample_list.delete(0, END)
		
		for key in self.keys:
			self.sample_list.insert(END, key)
			
                print 'Ok...completely loaded.'
		return None
		
	def changename(self):
		new_name = askstring('Change Name', '%s <=> %s\n\nNew name:'%(self.name_dict_forward[self.curselection], self.curselection) )
		old_name = self.curselection
		
		if not self.curselection:
			return None
		
		if new_name and askyesno(message = 'Change name to %s?'%(new_name)):
			self.name_dict_samp_to_cmpd[self.curselection] = new_name
			self.name_dict_backward = rev_dict(self.name_dict_samp_to_cmpd)
			
			orig = open( os.path.join(self.database, 'Names.txt') ).read().strip().split('\n')
			new = open( os.path.join(self.database, 'Names.txt'), 'w')
			for line in orig:
				line = line.replace('"', '').replace("'", '').strip().split('\t')
				if self.curselection == line[0]:
					line[1] = new_name
				new.write('\t'.join(line) + '\n')
			new.close()

		print '\nName changed: %s to %s'%(old_name, new_name)
			
		return None
		
	def scroll(self, event = None):
		if event.char in [chr(x) for x in range(33, 256)] + [chr(8)]:
			## Non-whitespace characters & the backspace character
			if event.char != chr(8):
				self.search.insert(END, event.char)
				cur = self.search.get()
				self.search.delete( len(cur)-1, END )
			else:
				cur = self.search.get()
			
			len_cur = len(cur)
			
			for key in self.keys:
				if key[:len_cur].upper() == cur.upper():
					index = self.keys.index(key)
					self.sample_list.selection_clear(0,END)
					self.sample_list.selection_set(index)
					self.sample_list.see(index)
					self.get_item()
					return None
					
		return None
		
	def get_item(self, event = None):
		cur = self.sample_list.get( self.sample_list.curselection()[0] )
		
		if self.mode == 'CMPD':
			items = '\n' + '\n'.join(self.name_dict_cmpd_to_samp[cur])
		elif self.mode == 'SMP':
			items = '\n' + self.name_dict_samp_to_cmpd[cur]
		
		self.info_box['label'].config( text = '%s:\n'%(cur) + items )
		self.curselection = cur
		
		return None
		
	def changemode(self):
		if self.mode == 'CMPD':
			self.mode = 'SMP'
			self.info_box['changename'].config( state = NORMAL )
			self.keys = sorted( self.db_samps )
		elif self.mode == 'SMP':
			self.mode = 'CMPD'
			self.info_box['changename'].config( state = DISABLED )
			self.keys = sorted( [self.name_dict_samp_to_cmpd[item] for item in self.db_samps] )

		print '\nCurr mode: %s'%(self.mode)
		self.fill()
		
		return None
		
	def add_item(self):
		AddItemDialog(self.database, self.root)
		
		self.db_samps = [os.path.splitext(item)[0] for item in os.listdir( os.path.join(self.database, 'Corr') )]
		self.name_dict_samp_to_cmpd = CreateSig.extract_names( os.path.join(self.database, 'Names.txt') )
		self.name_dict_cmpd_to_samp = rev_dict(self.name_dict_samp_to_cmpd)
		if self.mode == 'CMPD':
			self.keys = sorted( [self.name_dict_samp_to_cmpd[item] for item in self.db_samps] )
		elif self.mode == 'SMP':
			self.keys = sorted( self.db_samps )

		print 'Updating list...'
		self.fill()
		
		return None
		
	def delete_item(self):
		cur_item = self.curselection
		prompt = askyesno( 'Delete item?', 'Are you sure?')
		if prompt:
                        print '\nRemoving associated files...'
			if self.mode == 'CMPD':
				cur_item = self.name_dict_cmpd_to_samp[self.curselection][0]
                                print cur_item
			for subdir in ['Corr', 'Sigs']:
				os.remove( os.path.join( self.database, subdir, cur_item + '.txt' ) )

                        print 'Removing from list of names...'
			orig = open( os.path.join(self.database, 'Names.txt') ).read().strip().split('\n')
			lines = []
			for line in orig:
				line = line.replace('"', '').replace("'", '').strip().split('\t')
				if cur_item == line[0]:
					continue
				lines.append('\t'.join(line))
                        open( os.path.join(self.database, 'Names.txt'), 'w').write('\n'.join(lines))
                        
			print 'Removing all associated datapoints from database...'
			num_left = len(os.listdir( os.path.join( self.database, 'Corr' ) ) )
			for item in os.listdir( os.path.join( self.database,'Corr') ):
				orig = open( os.path.join(self.database, 'Corr', item) ).read().strip().split('\n')
				lines = []
				for line in orig:
					line = line.replace('"', '').replace("'", '').strip().split('\t')
					if cur_item == line[0]:
						continue
					lines.append('\t'.join(line))
				open( os.path.join(self.database, 'Corr', item), 'w' ).write('\n'.join(lines))

				num_left -= 1
				if num_left%1000 == 0:
                                        print num_left
                                if num_left < 1000:
                                        if num_left%100 ==0:
                                                print num_left

		print 'Ok...completely deleted from database.'
		print '\nUpdating list...'
		self.db_samps = [os.path.splitext(item)[0] for item in os.listdir( os.path.join(self.database, 'Corr') )]
		self.name_dict_samp_to_cmpd = CreateSig.extract_names( os.path.join(self.database, 'Names.txt') )
		self.name_dict_cmpd_to_samp = rev_dict(self.name_dict_samp_to_cmpd)
		if self.mode == 'CMPD':
			self.keys = sorted( [self.name_dict_samp_to_cmpd[item] for item in self.db_samps] )
		elif self.mode == 'SMP':
			self.keys = sorted( self.db_samps )
			
		self.fill()
		
		return None
		
	def view(self):
		if self.mode == 'CMPD':
			item = self.name_dict_cmpd_to_samp[self.curselection][0]
			title = self.curselection
		else:
			item = self.curselection
			title = self.name_dict_samp_to_cmpd[self.curselection][0]
		viewer = Toplevel()
		viewer.title(title)
		
		text = ScrolledText(viewer, width = 100)
		text.grid(row = 0, columnspan = 4, padx = 10, pady = 10)
		Button(viewer, text = 'Close', command = viewer.destroy).grid(row=1, column=3)
		
		tops = []
		bottoms = []
		overalls = []
		samples = []
		raw_data = [line.strip().split('\t') for line in open( os.path.join( self.database, 'Corr', item + '.txt' ) ).readlines()[1:]]
		raw_data.sort( key = lambda tuple: float(tuple[-1]), reverse = True )
		
		for (sample, top, bottom, overall) in raw_data:
			samples.append(sample)
			tops.append(top)
			bottoms.append(bottom)
			overalls.append(overall)
		names = [self.name_dict_samp_to_cmpd[sample] for sample in samples]
		
		data, row_len = mktable(samples, names, tops, bottoms, overalls)
		
		text.config(width = row_len)
		text.insert(END, data)
		
		text.config(state = DISABLED)

                print '\nCurr file located at %s'%(os.path.join(self.database, 'Corr', item + '.txt') )
		
		return None
		
if __name__ == '__main__':
        root = Tk()
	DBView( 'C:\\Tony\\TestZone', root)

