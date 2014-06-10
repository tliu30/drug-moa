from Tkinter import *
from Frontend_DB import ChooseDBDialog
from Frontend_Network import ChooseDBQueryDialog, ChooseDBWholeNetworkDialog

root = Tk()
root.title('Community Analysis')

#Create title
Label(root, text = 'Community Analysis V2.0 - Anthony Liu 2011', anchor = E).pack(side = TOP, fill = Y)
Label(root, text = 'Compare query signatures to existing signatures using graph theory.\nUseful in comparing MOA of different drugs.', justify = LEFT).pack(side = TOP)
###

#Network functions
network = LabelFrame(root, text = 'Network')
Label(network, text = 'Use the network algorithm to compare signatures.\n', justify = LEFT, anchor = E).grid(row = 0, column = 0, columnspan = 2, sticky = W)
Label(network, text = 'Compare a signature against the database.', anchor = E).grid(row = 1, column = 0, sticky = W)
Label(network, text = 'Analyzes the entire database to identify communities\nof similar drugs.', anchor = E, justify = LEFT).grid(row = 2, column = 0, sticky = W)
Button(network, text = 'Query', command = ChooseDBQueryDialog).grid(row = 1, column = 1, sticky = N+E+W+S)
Button(network, text = 'Whole Network', command = ChooseDBWholeNetworkDialog).grid(row = 2, column = 1, sticky = N+E+W+S)
network.pack(side = LEFT, fill =Y)
###########

#Database viewer
db = LabelFrame(root, text = 'Database', height = network['height'])
Label(db, text = 'View/edit the databases where the data is stored.\n').grid(row = 0, column = 0, columnspan = 2, sticky = W)
Label(db, text = 'View/edit existing databases.', anchor = E).grid(row = 1, column = 0, sticky = W)
Label(db, text = 'Create new database.', anchor = E).grid(row = 2, column = 0, sticky = W)
Button(db, text = 'View', command = ChooseDBDialog).grid(row = 1, column = 1, sticky = N+E+W+S)
Button(db, text = 'Create new database', state = DISABLED).grid(row = 2, column = 1, sticky = N+E+W+S)
db.pack(side = RIGHT, fill= Y)
############

root.mainloop()
