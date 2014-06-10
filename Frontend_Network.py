from Tkinter import *
print 'Loading image library...'
from ImageTk import PhotoImage

print 'Loading additional dialogs...'
import tkMessageBox, tkFileDialog
import os

print 'Loading basic functions from CreateSig...'
import CreateSig

DEFAULT_DIR = os.path.join('.', 'Database')
DIRECT = True #Whether or not to ask if user wants to input own database

############### Custom widgets #######################

class Listbox_w_Scroll:
        """
        Creates a Frame containing a Listbox linked to a Scrollbar.
        Most methods are mapped to the Listbox.
        """
	def __init__(self, master):
		self.frame = Frame(master)
		self.scrollbar = Scrollbar(self.frame)
		self.scrollbar.pack(side = RIGHT, fill = Y, expand = 1)
		self.listbox = Listbox(self.frame, yscrollcommand = self.scrollbar.set)
		self.listbox.pack(side = LEFT, fill = BOTH, expand = 1)
		self.scrollbar.config(command = self.listbox.yview)
	
	def insert(self, index, *items):
		return self.listbox.insert(index, *items)

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

###################################


############### Custom Dialogs ###########################

class OutputDirDialog:
	def __init__(self, default, parent = None):
                self.parent = parent
		self.root = Toplevel(parent)

		Label(self.root, text = 'Output directory: ').grid(row = 0, column = 0, pady = 5)
		self.output_dir_entry = Entry(self.root)
		self.output_dir_entry.insert(0, os.path.abspath(default))
		self.output_dir_entry.grid(row = 0, column = 1, padx = 5, pady = 5)
		Button(self.root, text='Browse', command = self.browse_dir).grid(row = 0, column = 2, pady = 5)

		Button(self.root, text='Ok', command = self.accept).grid(row = 1, column = 0, columnspan = 3, pady = 5)

		self.parent.wait_window(self.root)

	def browse_dir(self):
		filename = tkFileDialog.askdirectory().replace('/', os.sep)
		if not filename:
			return None
		self.output_dir_entry.delete(0, END)
		self.output_dir_entry.insert(0, filename)

	def accept(self):
		self.output_dir = self.output_dir_entry.get()
		if os.path.exists(self.output_dir):
			self.output_dir = os.path.abspath(self.output_dir)
			if tkMessageBox.askyesno(title = 'Output Directory', message = 'Directory exists.  Overwrite?'):
				for item in os.listdir(self.output_dir):
					if os.path.isfile( os.path.join(self.output_dir, item) ):
						os.remove( os.path.join(self.output_dir, item) )
					elif os.path.isdir( os.path.join(self.output_dir, item) ):
						for file in os.listdir( os.path.join(self.output_dir, item) ):
							os.remove( os.path.join(self.output_dir, item, file) )
						os.rmdir( os.path.join(self.output_dir, item) )
			else:
				return None
		else:
			os.mkdir( self.output_dir )

		self.root.destroy()
		return None

def askOutputDir(default, parent = None):
	output = OutputDirDialog(default, parent)
	return output.output_dir

class ChooseDBQueryDialog:
	def __init__(self, default = DEFAULT_DIR):
                if DIRECT:
                        QueryDialog(DEFAULT_DIR)
                else:
                        print '\nChoose directory for query...'
                        self.root = Toplevel()
                        self.root.title('Query')
                        
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
		QueryDialog(db_loc)
		return None

class ChooseDBWholeNetworkDialog:
	def __init__(self, default = DEFAULT_DIR):
                if DIRECT:
                        WholeNetworkDialog(DEFAULT_DIR)

                else:
                        print '\nChoose directory for analysis...'
                        self.root = Toplevel()
                        self.root.title('Whole Network')
                        
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
		WholeNetworkDialog(db_loc)
		return None
	
##################################################


############  Viewers ###########################

class OutputViewer_SingleQuery:
	"""
	Show output (network images & content) from the main window's output
	"""
	def __init__(self, directory, parent = None):
                print '\nInitializing viewer...'
		self.directory = directory
		self.root = Toplevel(parent)
		self.root.title(os.path.abspath(self.directory))

		self.comm_box = Frame(self.root)
		self.comm_list = Listbox_w_Scroll(self.comm_box)
		for item in sorted({}.fromkeys([os.path.splitext(file)[0] for file in os.listdir(self.directory)]).keys(), reverse = True):
			self.comm_list.insert(END, item)
		self.comm_list.activate(0)
		self.comm_list.pack(side = TOP, fill = BOTH, padx = 5, pady = 5)
		self.open_new = Button( self.comm_box, text = 'Open in New Window', command = self.display_new )
		self.save = Button( self.comm_box, text = 'Save', command = self.save)
		self.open_new.pack(side = TOP)
		self.save.pack(side = TOP)

		self.display_box = Frame(self.root)
		self.scrollbar = Scrollbar(self.display_box)
		self.scrollbar.pack(side = RIGHT, fill = Y)
		self.img = Label( self.display_box, image = None)
		self.desc = Text( self.display_box, state = DISABLED, yscrollcommand = self.scrollbar.set)
		self.scrollbar.config(command = self.desc.yview)
		self.img.pack(side = LEFT, fill = BOTH, expand = 1, padx = 5, pady = 10)
		self.desc.pack(side = LEFT, fill = BOTH, expand = 1, padx = 5, pady = 10)

		self.comm_box.pack( side = LEFT, fill = BOTH, expand = 1, padx = 10, pady = 10 )
		self.display_box.pack( side = RIGHT, fill = BOTH, expand = 1, padx = 10, pady = 10 )
		
		self.comm_list.bind( '<Double-Button-1>', self.display )
		self.comm_list.bind( '<Return>', self.display )

		self.display()

		print 'Ok...viewer loaded.'

	def display(self, event = None):
		cur_item = self.comm_list.get(ACTIVE)

		imgobj = PhotoImage( file = os.path.join( self.directory, cur_item + '.png' ) )
		item_list = '\n'.join([line.strip().split('\t')[0] for line in open( os.path.join( self.directory, cur_item + '.txt' ) ).readlines()])
		self.img.configure(image = imgobj)
		self.img.image = imgobj

		self.desc.config(state = NORMAL)
		self.desc.delete(1.0, END)
		self.desc.insert(END,item_list)
		self.desc.config(state = DISABLED)

		return None

	def display_new(self):
		display_box = Toplevel()

		scrollbar = Scrollbar(display_box)
		scrollbar.pack(side = RIGHT, fill = Y)

		cur_item = self.comm_list.get(ACTIVE)
		display_box.title(cur_item)
		
		imgobj = PhotoImage( file = os.path.join( self.directory, cur_item + '.png' ) )
		item_list = '\n'.join([line.strip().split('\t')[0] for line in open( os.path.join( self.directory, cur_item + '.txt' ) ).readlines()])

		img = Label(display_box, image = imgobj )
		img.image = imgobj
		img.pack(side = LEFT, padx = 10, pady = 10)
		text = Text( display_box, yscrollcommand = scrollbar.set)
		text.insert(END, item_list)
		text.config(state = DISABLED)
		text.pack(side = LEFT, fill = BOTH, expand = 1, padx = 10, pady = 10)
		scrollbar.config(command = text.yview)

		return None

	def save(self):
		cur_item = self.comm_list.get(ACTIVE)

		tgt_dir = tkFileDialog.askdirectory()
		open( os.path.join(tgt_dir, cur_item + '.txt'), 'w' ).write( open(os.path.join(self.directory, cur_item + '.txt') ).read() )
		open( os.path.join(tgt_dir, cur_item + '.png'), 'wb' ).write( open(os.path.join(self.directory, cur_item + '.png'), 'rb').read() )

                print '\nSaved to ' + os.path.join(tgt_dir, cur_item + '.txt')
                print 'Saved to ' + os.path.join(tgt_dir, cur_item + '.png')
		return None

class OutputViewer_Entire:
	def __init__(self, directory, parent = None):
                print 'Initializing viewer...'
		self.root_directory = directory
		self.root = Toplevel(parent)
		self.root.title(os.path.abspath(self.root_directory))

		self.comm_box = Frame(self.root)
		self.folder_list = Listbox_w_Scroll(self.comm_box)
		self.folder_list.bind( '<Button-1>', self.select_folder )
		self.folder_list.bind( '<Return>', self.select_folder )
		for item in sorted(os.listdir(self.root_directory), reverse = True):
			self.folder_list.insert(END,item)
		self.folder_list.pack(side = TOP, fill = BOTH, expand = 1, padx = 5, pady = 5)
		self.folder_list.selection_set(0)
		self.comm_list = Listbox_w_Scroll(self.comm_box)
		self.comm_list.pack(side = TOP, fill = BOTH, expand = 1, padx = 5, pady = 5)
		self.open_new = Button( self.comm_box, text = 'Open in New Window', command = self.display_new )
		self.save = Button( self.comm_box, text = 'Save', command = self.save)
		self.open_new.pack(side = TOP)
		self.save.pack(side = TOP)

		self.display_box = Frame(self.root)
		self.scrollbar = Scrollbar(self.display_box)
		self.scrollbar.pack(side = RIGHT, fill = Y)
		self.img = Label( self.display_box, image = None)
		self.desc = Text( self.display_box, state = DISABLED, yscrollcommand = self.scrollbar.set)
		self.scrollbar.config(command = self.desc.yview)
		self.img.pack(side = LEFT, fill = BOTH, expand = 1, padx = 5, pady = 10)
		self.desc.pack(side = LEFT, fill = BOTH, expand = 1, padx = 5, pady = 10)

		self.comm_box.pack( side = LEFT, fill = BOTH, expand = 1, padx = 10, pady = 10 )
		self.display_box.pack( side = RIGHT, fill = BOTH, expand = 1, padx = 10, pady = 10 )
		
		self.comm_list.bind( '<Button-1>', self.display )
		self.comm_list.bind( '<Return>', self.display )

		self.select_folder()
		self.display()

		print 'Ok...viewer loaded.'

	def select_folder(self, event = None):
		cur_item = self.folder_list.get(ACTIVE)

		self.directory = os.path.join( self.root_directory, cur_item )
		self.comm_list.delete(0, END)
		for item in sorted({}.fromkeys([os.path.splitext(file)[0] for file in os.listdir(self.directory)]).keys()):
			self.comm_list.insert(END, item)

		root_file = [line.strip().split('\t') for line in open( os.path.join( self.directory, cur_item + '.txt' ) ).readlines()]
		header = root_file[0]
		self.item_data = {cur_item : ''}
		singles = ''
		for item in header:
			self.item_data[item] = ''
		for line in root_file[1:]:
			for index in range(len(line)):
				try:
					header[index]
				except:
					singles += '\n' + line[index]
					continue
				self.item_data[header[index]] += '\n' + line[index]
		for comm in header:
			self.item_data[cur_item] += comm + '\n    '.join(self.item_data[comm].split('\n')) + '\n\n'
			self.item_data[comm] = 'Compounds\n' + self.item_data[comm]
		self.item_data[cur_item] += singles

		self.comm_list.selection_set(0)
		self.display()

	def display(self, event = None):
		cur_item = self.comm_list.get(ACTIVE)

		imgobj = PhotoImage( file = os.path.join( self.directory, cur_item + '.png' ) )
		item_list = self.item_data[cur_item]
		self.img.configure(image = imgobj)
		self.img.image = imgobj

		self.desc.config(state = NORMAL)
		self.desc.delete(1.0, END)
		self.desc.insert(END,item_list)
		self.desc.config(state = DISABLED)

		return None

	def display_new(self):
		display_box = Toplevel()

		scrollbar = Scrollbar(display_box)
		scrollbar.pack(side = RIGHT, fill = Y)

		cur_item = self.comm_list.get(ACTIVE)
		display_box.title(cur_item)
		
		imgobj = PhotoImage( file = os.path.join( self.directory, cur_item + '.png' ) )
		item_list = self.item_data[cur_item]
		img = Label(display_box, image = imgobj )
		img.image = imgobj
		img.pack(side = LEFT, padx = 10, pady = 10)
		text = Text( display_box, yscrollcommand = scrollbar.set)
		text.insert(END, item_list)
		text.config(state = DISABLED)
		text.pack(side = LEFT, fill = BOTH, expand = 1, padx = 10, pady = 10)
		scrollbar.config(command = text.yview)

		return None

	def save(self):
		cur_item = self.comm_list.get(ACTIVE)

		tgt_dir = tkFileDialog.askdirectory()
		open( os.path.join(tgt_dir, cur_item + '.txt'), 'w' ).write( self.item_data[cur_item] )
		open( os.path.join(tgt_dir, cur_item + '.png'), 'wb' ).write( open(os.path.join(self.directory, cur_item + '.png'), 'rb').read() )

                print '\nSaved to ' + os.path.join(tgt_dir, cur_item + '.txt')
                print 'Saved to ' + os.path.join(tgt_dir, cur_item + '.png')

		return None

############################################


############### Main Window ############################

class QueryDialog:
        """
        Asks info needed to run query.
        Prompts for output directory.
        Then, runs query or query_cmpd functions from CreateSig.py
        [Displays progress in command line].
        Finally, displays results in Output Viewer.
        """
        def __init__(self, directory, parent = None):
                self.directory = directory

                if parent:
                        self.root = Toplevel(parent)
                else:
                        self.root = Toplevel()
                self.root.title('Query - %s'%(os.path.abspath(self.directory)))
		self.query = LabelFrame(self.root, text = 'Query information')
		self.values = LabelFrame(self.root, text = 'Values')

                ### Each of the following tuples describes a info-input line (with label, entry area, button, etc.) ###
		self.query_loc = {      'desc': Label(self.query, text = 'Location of query: ', anchor = E),
					'entry': Entry(self.query),
					'button': Button(self.query, text = 'Browse', command = self.browse_query)       }
		self.query_name = {     'desc': Label(self.query, text = 'Compound/Disease/etc. name: ', anchor = E),
					'entry': Entry(self.query)       }
		self.sample_name = {    'desc': Label(self.query, text = 'Sample ID', anchor = E),
					'entry': Entry(self.query)       }
		self.cutoff = {         'desc': Label(self.values, text = 'Cutoff: ', anchor = E),
                                        'entry': Entry(self.values, width = 10)   }
		self.numtotal = {       'desc': Label(self.values, text = 'Total number of genes: ', anchor = E),
					'entry': Entry(self.values, width = 10)   }
		###############################

                ### Radiobuttons for the mode ###
		self.mode_box = Frame(self.values)
		Label(self.mode_box, text = 'Mode: ').grid(row = 0, column = 0)
		self.mode = StringVar()
		for (item, value) in [ ('Top', 1), ('Bottom', 2), ('Overall', 3) ]:
			Radiobutton(self.mode_box, text = item, variable = self.mode, value = value).grid(row = 1, column = value - 1)
		self.mode.set(3)
		###############################

		self.query_loc['desc'].grid(row = 0, column = 0)
		self.query_loc['entry'].grid(row = 0, column = 1)
		self.query_loc['button'].grid(row = 0, column = 2, padx = 2)
		self.query_name['desc'].grid(row = 1, column = 0)
		self.query_name['entry'].grid(row = 1, column = 1)
		self.sample_name['desc'].grid(row = 2, column = 0)
		self.sample_name['entry'].grid(row = 2, column = 1)
		self.query.pack(side = TOP, fill = X)

		self.cutoff['desc'].grid(row = 0, column = 0)
		self.cutoff['entry'].grid(row = 0, column = 1)
		self.numtotal['desc'].grid(row = 1, column = 0)
		self.numtotal['entry'].grid(row = 1, column = 1)
		self.mode_box.grid(row = 0, column = 2, rowspan = 2, columnspan = 2)
		self.values.pack(side = TOP, fill = X)

		Button(self.root, text = 'Run', command = self.run).pack(side = TOP, fill = X)

	def browse_query(self):
		filename = tkFileDialog.askopenfilename().replace('/', os.sep)
		if not filename:
			return None
		self.query_loc['entry'].delete(0, END)
		self.query_loc['entry'].insert(0, filename)
		self.sample_name['entry'].delete(0, END)
		self.sample_name['entry'].insert(0, os.path.splitext(os.path.split(self.query_loc['entry'].get())[1])[0])

	def run(self):
		### Gather info ######################
		query_loc = self.query_loc['entry'].get()
		query_name = self.query_name['entry'].get()
		sample_name = self.sample_name['entry'].get()
		db_loc = os.path.abspath(self.directory)
		cutoff = int(self.cutoff['entry'].get())
		numtotal = int(self.numtotal['entry'].get())
		mode = self.mode.get()
		###################################

                print '\nParameters entered -'
                print '\tQuery name: %s'%(query_name)
                print '\tQuery location: %s'%(query_loc)
                print '\tSample name: %s'%(sample_name)
                print '\tDatabase: %s'%(db_loc)
                print '\tCutoff: %i'%(cutoff)
                print '\tNumber of total genes: %i'%(numtotal)
                print '\tMode: %s'%(mode)

		### Catch missing info #################
		if not cutoff or not query_loc or not db_loc or not query_name or not numtotal or not mode or not sample_name:
			tkMessageBox.showwarning( title = 'Error', message = 'Missing information!' )
			return None

		fail = False
		for item in (db_loc, query_loc):
			if not os.path.exists( item ):
				tkMessageBox.showwarning( title = 'Error', message = '%s does not exist!'%(item) )
				fail = True
		if fail:
			return None
		####################################

		query_dir = os.path.split(query_loc)[0]
		output_dir = os.path.abspath(askOutputDir( os.path.join( db_loc, 'Graph'), self.root ))

                print '\nOuputted to %s...'%(output_dir)
                print '\nRunning analysis...'
                print db_loc
		if query_dir != os.path.join(db_loc, 'Sigs'):
			CreateSig.query(query_loc, query_name, os.path.join( db_loc, 'Sigs' ), os.path.join( db_loc, 'Corr' ), os.path.join( db_loc, 'Names.txt' ), numtotal, output_dir, cutoff, 1, True)
		else:
			CreateSig.query_cmpd(query_loc, os.path.join( db_loc, 'Corr' ), output_dir, os.path.join( db_loc, 'Names.txt' ), cutoff, 1, mode)

		print 'Ok...analysis complete.'
		OutputViewer_SingleQuery(output_dir, self.root)

		return None

class WholeNetworkDialog:
        """
        Asks info needed to run whole network analysis.
        Prompts for output directory.
        Then, runs whole_network function from CreateSig.py
        [Displays progress in command line].
        Finally, displays results in Output Viewer.
        """
        def __init__(self, directory, parent = None):
                self.directory = directory

                if parent:
                        self.root = Toplevel(parent)
                else:
                        self.root = Toplevel()
                self.root.title('Whole Network - %s'%(self.directory) )
		self.values = LabelFrame(self.root, text = 'Values')

                ### Each of the following tuples describes a info-input line (with label, entry area, button, etc.) ###
		self.cutoff = {         'desc': Label(self.values, text = 'Cutoff: ', anchor = E),
                                        'entry': Entry(self.values, width = 10)   }
		self.numtotal = {       'desc': Label(self.values, text = 'Total number of genes: ', anchor = E),
					'entry': Entry(self.values, width = 10)   }
		###############################

                ### Radiobuttons for the mode ###
		self.mode_box = Frame(self.values)
		Label(self.mode_box, text = 'Mode: ').grid(row = 0, column = 0)
		self.mode = StringVar()
		for (item, value) in [ ('Top', 1), ('Bottom', 2), ('Overall', 3) ]:
			Radiobutton(self.mode_box, text = item, variable = self.mode, value = value).grid(row = 1, column = value - 1)
		self.mode.set(3)
		###############################

		self.cutoff['desc'].grid(row = 0, column = 0)
		self.cutoff['entry'].grid(row = 0, column = 1)
		self.numtotal['desc'].grid(row = 1, column = 0)
		self.numtotal['entry'].grid(row = 1, column = 1)
		self.mode_box.grid(row = 0, column = 2, rowspan = 2, columnspan = 2)
		self.values.pack(side = TOP, fill = X)

		Button(self.root, text = 'Run', command = self.run).pack(side = TOP, fill = X)

	def run(self):
		### Gather info #########
		db_loc = self.directory
		cutoff = int(self.cutoff['entry'].get())
		numtotal = int(self.numtotal['entry'].get())
		mode = int(self.mode.get())
		######################

                print '\nParameters entered -'
                print '\tDatabase: %s'%(db_loc)
                print '\tCutoff: %i'%(cutoff)
                print '\tNumber of total genes: %i'%(numtotal)
                print '\tMode: %s'%(mode)

		### Catching missing information #################
		if not cutoff or not db_loc or not numtotal or not mode:
			tkMessageBox.showwarning( title = 'Error', message = 'Missing information!' )
			return None

		if not os.path.exists( db_loc ):
			tkMessageBox.showwarning( title = 'Error', message = '%s does not exist!'%(item) )
			return None
		#############################################

		output_dir = askOutputDir( os.path.join( db_loc, 'Graph'), self.root )

		print '\nOuputted to %s...'%(output_dir)
                print '\nRunning analysis...'
		CreateSig.whole_network( os.path.join( db_loc, 'Corr' ), cutoff, output_dir, os.path.join( db_loc, 'Names.txt' ), mode )

		print 'Ok...analysis complete.'
		OutputViewer_Entire(output_dir, self.root)

		return None

##########################################################

if __name__ == '__main__':
        root = Tk()
        WholeNetworkDialog('C:\\Tony\\TestZone', root)
        root.mainloop()
