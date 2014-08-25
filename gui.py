from Tkinter import *
import tkFileDialog
import tkSimpleDialog

class CreateHgdFromExprDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        Label(master, text = "Output Directory").grid(row = 0, column = 0, sticky = W)
        Label(master, text = "Expression Matrix").grid(row = 1, column = 0, sticky = W)
        Label(master, text = "# Top Reg").grid(row = 2, column = 2, sticky = W)
        Label(master, text = "# Down Reg").grid(row = 2, column = 4, sticky = W)

        self.odir = Entry(master)
        self.ifname = Entry(master)
        self.transpose = IntVar(); self.transpose_box = Checkbutton(master, text = "Transpose", var = self.transpose)
        self.num_top = Entry(master, width = 8)
        self.num_bot = Entry(master, width = 8)

        self.odir.grid(row = 0, column = 1, columnspan = 3, sticky = W + E)
        self.ifname.grid(row = 1, column = 1, columnspan = 3, sticky = W + E)
        self.transpose_box.grid(row = 2, column = 0)
        self.num_top.grid(row = 2, column = 3)
        self.num_bot.grid(row = 2, column = 5)

        self.odir_b = Button(master, text = "Choose dir...", command = self.choose_dir)
        self.ifname_b = Button(master, text = "Choose file...", command = self.choose_file)

        self.odir_b.grid(row = 0, column = 4, columnspan = 2, sticky = W + E)
        self.ifname_b.grid(row = 1, column = 4, columnspan = 2, sticky = W + E)

        return self.odir

    def apply(self):
        print(self.odir.get())
        print(self.ifname.get())
        print(self.transpose.get())
        print(self.num_top.get())
        print(self.num_bot.get())
        return None

    def choose_dir(self):
        dir_name = tkFileDialog.askdirectory()
        self.odir.delete(0, END)
        self.odir.insert(0,dir_name)
        return None

    def choose_file(self):
        file_name = tkFileDialog.askopenfilename()
        self.ifname.delete(0, END)
        self.ifname.insert(0, file_name)
        return None       

class AddHgdFromExprDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        Label(master, text = "Output Directory").grid(row = 0, column = 0, sticky = W)
        Label(master, text = "Old Similarity Dir").grid(row = 1, column = 0, sticky = W)
        Label(master, text = "Expression Matrix").grid(row = 2, column = 0, sticky = W)
        Label(master, text = "# Top Reg").grid(row = 3, column = 2, sticky = W)
        Label(master, text = "# Down Reg").grid(row = 3, column = 4, sticky = W)

        self.odir = Entry(master)
        self.ifname = Entry(master)
        self.old_dir = Entry(master)
        self.transpose = IntVar(); self.transpose_box = Checkbutton(master, text = "Transpose", var = self.transpose)
        self.num_top = Entry(master, width = 8)
        self.num_bot = Entry(master, width = 8)

        self.odir.grid(row = 0, column = 1, columnspan = 3, sticky = W + E)
        self.ifname.grid(row = 1, column = 1, columnspan = 3, sticky = W + E)
        self.old_dir.grid(row= 2, column = 1, columnspan = 3, sticky = W + E)
        self.transpose_box.grid(row = 3, column = 0)
        self.num_top.grid(row = 3, column = 3)
        self.num_bot.grid(row = 3, column = 5)

        self.odir_b = Button(master, text = "Choose dir...", command = self.choose_dir)
        self.ifname_b = Button(master, text = "Choose file...", command = self.choose_file)
        self.old_dir_b = Button(master, text = "Choose dir...", command = self.choose_dir_b)

        self.odir_b.grid(row = 0, column = 4, columnspan = 2, sticky = W + E)
        self.ifname_b.grid(row = 1, column = 4, columnspan = 2, sticky = W + E)
        self.old_dir_b.grid(row = 2, column = 4, columnspan = 2, sticky = W + E)

        return self.odir

    def apply(self):
        print(self.odir.get())
        print(self.ifname.get())
        print(self.old_dir.get())
        print(self.transpose.get())
        print(self.num_top.get())
        print(self.num_bot.get())
        return None

    def choose_dir(self):
        dir_name = tkFileDialog.askdirectory()
        self.odir.delete(0, END)
        self.odir.insert(0,dir_name)
        return None

    def choose_dir_b(self):
        dir_name = tkFileDialog.askdirectory()
        self.old_dir.delete(0, END)
        self.old_dir.insert(0,dir_name)

        old_sig_mtx, _, _ = read_mtx( os.path.join(old_dir, 'sig_mtx.csv'), transpose = False, rowname = True, colname = True)
        self.num_top.delete(0, END)
        self.num_top.insert(0, (old_sig_mtx[0,] == 1).sum())
        self.num_bot.delete(0, END)
        self.num_bot.delete(0, (old_sig_mtx[0,] == -1).sum())

        return None

    def choose_file(self):
        file_name = tkFileDialog.askopenfilename()
        self.ifname.delete(0, END)
        self.ifname.insert(0, file_name)
        return None       

class CreateHgdFromSigsDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        Label(master, text = "Output Directory").grid(row = 0, column = 0, sticky = W)
        Label(master, text = "Signature Files").grid(row = 1, column = 0, sticky = W)
        Label(master, text = "# Top Reg").grid(row = 2, column = 2, sticky = W)
        Label(master, text = "# Down Reg").grid(row = 2, column = 4, sticky = W)

        self.odir = Entry(master)
        self.ifnames = Entry(master)
        self.transpose = IntVar(); self.transpose_box = Checkbutton(master, text = "Transpose", var = self.transpose)
        self.num_top = Entry(master, width = 8)
        self.num_bot = Entry(master, width = 8)

        self.odir.grid(row = 0, column = 1, columnspan = 3, sticky = W + E)
        self.ifnames.grid(row = 1, column = 1, columnspan = 3, sticky = W + E)
        self.transpose_box.grid(row = 2, column = 0)
        self.num_top.grid(row = 2, column = 3)
        self.num_bot.grid(row = 2, column = 5)

        self.odir_b = Button(master, text = "Choose dir...", command = self.choose_dir)
        self.ifnames_b = Button(master, text = "Choose file...", command = self.choose_files)

        self.odir_b.grid(row = 0, column = 4, columnspan = 2, sticky = W + E)
        self.ifnames_b.grid(row = 1, column = 4, columnspan = 2, sticky = W + E)

        return self.odir

    def apply(self):
        print(self.odir.get())
        print(self.ifnames.get())
        print(self.transpose.get())
        print(self.num_top.get())
        print(self.num_bot.get())
        return None

    def choose_dir(self):
        dir_name = tkFileDialog.askdirectory()
        self.odir.delete(0, END)
        self.odir.insert(0,dir_name)
        return None

    def choose_files(self):
        file_name = tkFileDialog.askopenfilenames()
        self.ifnames.delete(0, END)
        self.ifnames.insert(0, file_name)
        return None       

class AddHgdFromSigsDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        Label(master, text = "Output Directory").grid(row = 0, column = 0, sticky = W)
        Label(master, text = "Old Similarity Dir").grid(row = 1, column = 0, sticky = W)
        Label(master, text = "Signature Files").grid(row = 2, column = 0, sticky = W)
        Label(master, text = "# Top Reg").grid(row = 3, column = 2, sticky = W)
        Label(master, text = "# Down Reg").grid(row = 3, column = 4, sticky = W)

        self.odir = Entry(master)
        self.ifnames = Entry(master)
        self.old_dir = Entry(master)
        self.transpose = IntVar(); self.transpose_box = Checkbutton(master, text = "Transpose", var = self.transpose)
        self.num_top = Entry(master, width = 8)
        self.num_bot = Entry(master, width = 8)

        self.odir.grid(row = 0, column = 1, columnspan = 3, sticky = W + E)
        self.ifnames.grid(row = 1, column = 1, columnspan = 3, sticky = W + E)
        self.old_dir.grid(row= 2, column = 1, columnspan = 3, sticky = W + E)
        self.transpose_box.grid(row = 3, column = 0)
        self.num_top.grid(row = 3, column = 3)
        self.num_bot.grid(row = 3, column = 5)

        self.odir_b = Button(master, text = "Choose dir...", command = self.choose_dir)
        self.ifnames_b = Button(master, text = "Choose file...", command = self.choose_files)
        self.old_dir_b = Button(master, text = "Choose dir...", command = self.choose_dir_b)

        self.odir_b.grid(row = 0, column = 4, columnspan = 2, sticky = W + E)
        self.ifnames_b.grid(row = 1, column = 4, columnspan = 2, sticky = W + E)
        self.old_dir_b.grid(row = 2, column = 4, columnspan = 2, sticky = W + E)

        return self.odir

    def apply(self):
        print(self.odir.get())
        print(self.ifnames.get())
        print(self.old_dir.get())
        print(self.transpose.get())
        print(self.num_top.get())
        print(self.num_bot.get())
        return None

    def choose_dir(self):
        dir_name = tkFileDialog.askdirectory()
        self.odir.delete(0, END)
        self.odir.insert(0,dir_name)
        return None

    def choose_dir_b(self):
        dir_name = tkFileDialog.askdirectory()
        self.old_dir.delete(0, END)
        self.old_dir.insert(0,dir_name)
        
        old_sig_mtx, _, _ = read_mtx( os.path.join(old_dir, 'sig_mtx.csv'), transpose = False, rowname = True, colname = True)
        self.num_top.delete(0, END)
        self.num_top.insert(0, (old_sig_mtx[0,] == 1).sum())
        self.num_bot.delete(0, END)
        self.num_bot.delete(0, (old_sig_mtx[0,] == -1).sum())

        return None

    def choose_files(self):
        file_name = tkFileDialog.askopenfilenames()
        self.ifnames.delete(0, END)
        self.ifnames.insert(0, file_name)
        return None       

root = Tk()
Button(root, text = "Hello!").pack()
root.update()

d = AddHgdFromSigsDialog(root, title = "This is a PSA")

#Tk().withdraw()
##filename = askopenfilename()
#print(filename)
