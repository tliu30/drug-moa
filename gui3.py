import os
from sig_msg_box import *
from utils import *
from sigs import *
import interface
from Tkinter import *
import ttk
import tkFileDialog
import tkSimpleDialog
import tkMessageBox

def _make_entry_field(master, label_text, button_text, button_command):
    l = Label(master, text = label_text)
    e = Entry(master)
    b = Button(master, text = button_text, command = button_command(e) )
    return (l,e,b)

def _grid_row(row, cols, items, colspans = None, stickys = None):
    if not colspans: colspans = [1] * len(cols)
    if not stickys : stickys  = [W + E] * len(cols)
    for (col, item, colspan, sticky) in zip(cols, items, colspans, stickys):
        item.grid(row = row, column = col, columnspan = colspan, sticky = sticky)

class BaseDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        # Output directory (odir)
        self.odir_l, self.odir_e, self.odir_b = _make_entry_field(
            master, "Output Directory", "Choose dir...", self._choose_dir)

        # Expression matrix
        self.expr_l, self.expr_e, self.expr_b = _make_entry_field(
            master, "Expression Matrix", "Choose file...", self._choose_expr)
        self.expr_t = Label(master, text = "0 x 0", width = 15)

        # Transpose check
        self.trans_val = IntVar()
        self.trans_chk = Checkbutton(master, text = "Transpose", var = self.trans_val)

        # Signature files
        self.sigs_l, self.sigs_e, self.sigs_b = _make_entry_field(
            master, "Signature Files", "Choose Files...", self._choose_files)

        # Probe list
        self.plist_l, self.plist_e, self.plist_b = _make_entry_field(
            master, "Probe List", "Choose File...", self._choose_plist)

        # Construct probe list
        self.create_val = IntVar()
        self.create_chk = Checkbutton(master, text = "Create", var = self.create_val, command = self.clear)

        # Up Reg
        self.top_l = Label(master, text = "# Up Reg")
        self.top_e = Entry(master, width = 12)
        
        # Down Reg
        self.bot_l = Label(master, text = "# Down Reg")
        self.bot_e = Entry(master, width = 12)

        # Old directory
        self.old_l, self.old_e, self.old_b = _make_entry_field(
            master, "Old Directory", "Choose dir...", self._choose_dir)

        # Find similarity matrix
        self.sim_l, self.sim_e, self.sim_b = _make_entry_field(
            master, "Similarity Matrix", "Choose file...", self._choose_file)

        # Cutoff
        self.cutoff_l = Label(master, text = "Cutoff")
        self.cutoff_e = Entry(master)

        # Focus
        self.focus_val = IntVar(); self.focus_val.set(0)
        self.focus_chk = Checkbutton(master, text = "Focus", var = self.focus_val, command = self.off_entry)
        self.focus_e = Entry(master, state = DISABLED)

        self.construct()

    # Create dialogues for locating files / directories

    def _choose(self, chooser, FUN = lambda x: x):
        def FUN1(entry):
            def FUN2():
                name = chooser()
                entry.delete(0, END)
                entry.insert(0, name)
                FUN(name)
            return FUN2
        return FUN1
    
    def _choose_dir(self, entry):   return self._choose(tkFileDialog.askdirectory)(entry)
    def _choose_file(self, entry):  return self._choose(tkFileDialog.askopenfilename)(entry)
    def _choose_files(self, entry): return self._choose(tkFileDialog.askopenfilenames)(entry)

    def _choose_expr(self, entry):  
        def FUN(name):
            m, _, _ = read_mtx(name, transpose = False)
            self.expr_t.config(text = "%i x %i"%m.shape)
        return self._choose(tkFileDialog.askopenfilename, FUN)(entry)

    def _choose_old(self, entry):
        def FUN(name):
            m, _, _ = read_mtx(os.path.join(name, 'sig_mtx.csv'), transpose = False)
            self.top_e.delete(0, END)
            self.top_e.insert(0, (old_sig_mtx[0,] ==  1).sum())
            self.bot_e.delete(0, END)
            self.bot_e.insert(0, (old_sig_mtx[0,] == -1).sum())
        return self._choose(tkFileDialog.askdirectory, FUN)(entry)

    def _choose_plist(self, entry):
        def FUN(name):
            self.create_chk.deselect()
        return self._choose(tkFileDialog.askopenfilename, FUN)(entry)

    # Aux function for self.create_chk
    
    def clear(self): self.plist_e.delete(0, END)

    def off_entry(self):
        if self.focus_val.get() == 0:
            self.focus_e.config(state = DISABLED)
        else: self.focus_e.config(state = NORMAL)

    # Apply the stuff

    def mark(self):
        self.marked = {}

    def apply(self):
        self.mark()
        self.result = dict( map(lambda (x,y,z): (x, z(y.get())), self.marked ) )

    # Validate

    def validate_path(self, path, text, FUN):
        if not FUN(path):
            tkMessageBox.showwarning("Invalid Path", text)
            raise OSError
        else: pass

    def validate_expr_transpose(self):
        m, _, _    = read_mtx(self.expr_e.get(), transpose = self.trans_val.get())
        nrow, ncol = m.shape
        if nrow > ncol:
            ans = tkMessageBox.askokcancel("Transpose matrix?",
                """The expression matrix currently has more rows than
                columns, suggesting tests are arranged in columns.  The
                program prefers tests along rows.  Click "OK" to continue,
                or click "Cancel" to return to dialog.""")
            if not ans: raise OSError
        else: pass

    def validate_top_bot(self):
        m, _, _  = read_mtx(self.expr_e.get(), transpose = self.trans_val.get())
        _, ncol  = m.shape

        if ncol < ( int(self.top_e.get()) + int(self.bot_e.get()) ):
            tkMessageBox.showwarning("Invalid Up/Down Reg",
                "The sum of up/down regulated genes requested is greater than the number of probes.")
            raise OSError
        else: pass

    def validate_create_plist(self):
        if self.plist_e.get() != '' and self.create_val.get():
            tkMessageBox.showwarning("Conflict",
                "Either choose an existing probe list OR create one from current options.")
            raise OSError
        elif self.plist_e.get() == '' and (not self.create_val.get()):
            tkMessageBox.showwarning("Invalid List",
                "Either choose an existing probe list OR create one from current options.")
            raise OSError
        else: pass

    def validate_sigs(self):
        sigs = self.sigs_e.get().split(' ')
        ans  = SigMsgBox(self, sigs)
        self.wait_window(ans.top)
        if not ans.result: raise OSError

    def validate_sigs_plist(self):
        sigs = self.sigs_e.get().split(' ')
        probe_set = set()
        for sig in sigs:
            self.validate_path(sig, "%s was not found"%(sig), os.path.exists)
            top, bot = read_sig_file(sig)
            probe_set.update(top, bot)
        plist_set = set( open(self.plist_e.get()).read().strip().split('\n') )
        if not probe_set.issubset(plist_set):
            ans = tkMessageBox.askokcancel("Discrepency", "Not all genes in provided signatures were found in probe list.  If we continue, all probes not in list will be ignored.")
            if not ans: raise OSError

    def validate_old_dir(self):
        fnames = ['HGD_AVG.csv', 'HGD_UP_REG.csv', 'HGD_DOWN_REG.csv', 'sig_mtx.csv', 'probelist.csv']
        missing = bool( sum( map(lambda x: not os.path.exists( os.path.join(self.old_e.get(), x)), fnames) ) ) 
        if missing:
            tkMessageBox.showwarning("Invalid Input", "Chosen director does not hold similarity data.")
            raise OSError
        else: pass
     
    def validate_cutoff(self):
        if float(self.cutoff_e.get()) >= 1:
            tkMessageBox.showwarning("Invalid Input", "Cutoff value needs to be [0,1)")
            raise OSError
        else: pass

    def validate_focus(self):
        _, names, _ = read_mtx(self.sim_e.get(), transpose = False)
        if self.focus_e.get() in names: pass
        else:
            tkMessageBox.showwarning("Invalid Input", "Chosen focus not in similarity matrix.")
            raise OSError
               
    def validate(self):
        return 1

class CreateExpr(BaseDialog):

    def construct(self):
        _grid_row(0, [0,1,3], [self.odir_l, self.odir_e, self.odir_b], [1,2,2], [W, W+E, W+E])
        _grid_row(1, [0,1,3,5], [self.expr_l, self.expr_e, self.expr_b, self.expr_t], [1,2,2,1], [W, W+E, W+E, W+E])
        _grid_row(2, [0,1,2,3,4], [self.trans_chk, self.top_l, self.top_e, self.bot_l, self.bot_e])
        #_grid_row(1, [0,1,3], [self.expr_l, self.expr_e, self.expr_b], [1,2,2], [W, W+E, W+E])
        #_grid_row(2, [1,2], [self.expr_t, self.trans_chk])
        #_grid_row(3, [0,1,2,3], [self.top_l, self.top_e, self.bot_l, self.bot_e])

    def validate(self):
        try:
            self.validate_path(self.odir_e.get(), "The directory %s was not found!"%(self.odir_e.get()), os.path.exists)
            self.validate_path(self.expr_e.get(), "The file %s was not found!"%(self.expr_e.get()), os.path.exists)
            self.validate_expr_transpose()
            self.validate_top_bot()
            return 1
        except OSError:
            return 0

    def mark(self):
        names = ['odir', 'ifname', 'transpose', 'num_top', 'num_bot']
        items = [self.odir_e, self.expr_e, self.trans_val, self.top_e, self.bot_e]
        funcs = [str, str, bool, int, int]

        self.marked = zip(names, items, funcs)

class AddExpr(BaseDialog):

    def construct(self):
        _grid_row(0, [0,1,3], [self.odir_l, self.odir_e, self.odir_b], [1,2,2], [W, W+E, W+E])
        _grid_row(1, [0,1,3], [self.old_l, self.old_e, self.old_b], [1,2,2], [W, W+E, W+E])
        _grid_row(2, [0,1,3,5], [self.expr_l, self.expr_e, self.expr_b, self.expr_t], [1,2,2,1], [W, W+E, W+E, W+E])
        _grid_row(3, [0,1,2,3,4], [self.trans_chk, self.top_l, self.top_e, self.bot_l, self.bot_e])

    def validate(self):
        try:
            self.validate_path(self.odir_e.get(), "The directory %s was not found!"%(self.odir_e.get()), os.path.exists)
            self.validate_path(self.expr_e.get(), "The file %s was not found!"%(self.expr_e.get()), os.path.exists)
            self.validate_old_dir()
            self.validate_expr_transpose()
            self.validate_top_bot()
            return 1
        except OSError:
            return 0

    def mark(self):
        names = ['odir', 'old_dir', 'ifname', 'transpose', 'num_top', 'num_bot']
        items = [self.odir_e, self.old_e, self.expr_e, self.trans_val, self.top_e, self.bot_e]
        funcs = [str, str, str, bool, int, int]

        self.marked = zip(names, items, funcs)

class CreateSigs(BaseDialog):

    def construct(self):
        _grid_row(0, [0,1,3], [self.odir_l, self.odir_e, self.odir_b], [1,2,2], [W, W+E, W+E])
        _grid_row(1, [0,1,3], [self.sigs_l, self.sigs_e, self.sigs_b], [1,2,2], [W, W+E, W+E])
        _grid_row(2, [0,1,3,4], [self.plist_l, self.plist_e, self.plist_b, self.create_chk], [1,2,1,1], [W, W+E, W+E, W+E])

        self.odir_e.insert(0, "/home/anthony/Documents/Projects/drug_moa/test2/sigs")
        self.plist_e.insert(0, "/home/anthony/Documents/Projects/drug_moa/test/main/probelist.csv")
        self.sigs_e.insert(0, ' '.join([os.path.join('/home/anthony/Documents/Projects/drug_moa/test/sigs/', x) for x in os.listdir('/home/anthony/Documents/Projects/drug_moa/test/sigs')]))

    def validate(self):
        try:
            self.validate_path(self.odir_e.get(), "The directory %s was not found!"%(self.odir_e.get()), os.path.exists)
            self.validate_create_plist()
            if self.plist_e.get() != '':
                self.validate_path(self.plist_e.get(), "The file %s was not found!"%(self.plist_e.get()), os.path.exists)
                self.validate_sigs_plist()
            self.validate_sigs()
            return 1
        except OSError:
            return 0

    def mark(self):
        def FUN(x):
            if x == '': return None
            else: return str(x)
        names = ['odir', 'sig_files', 'master_fname']
        items = [self.odir_e, self.sigs_e, self.plist_e]
        funcs = [str, lambda x: x.split(' '), FUN]

        self.marked = zip(names, items, funcs)

class AddSigs(BaseDialog):

    def construct(self):
        _grid_row(0, [0,1,3], [self.odir_l, self.odir_e, self.odir_b], [1,2,2], [W, W+E, W+E])
        _grid_row(1, [0,1,3], [self.old_l, self.old_e, self.old_b], [1,2,2], [W, W+E, W+E])
        _grid_row(2, [0,1,3], [self.sigs_l, self.sigs_e, self.sigs_b], [1,2,2], [W, W+E, W+E])

    def validate(self):
        try:
            self.validate_path(self.odir_e.get(), "The directory %s was not found!"%(self.odir_e.get()), os.path.exists)
            self.validate_path(self.old_e.get(), "The directory %s was not found!"%(self.old_e.get()), os.path.exists)
            self.validate_old_dir()
            self.validate_sigs()
            return 1
        except OSError:
            return 0

    def mark(self):
        names = ['odir', 'old_dir', 'sig_files']
        items = [self.odir_e, self.old_e, self.sigs_e]
        funcs = [str, str, lambda x: x.split(' ')]

        self.marked = zip(names, items, funcs)

class AnalyzeNet(BaseDialog):

    def construct(self):
        _grid_row(0, [0,1,3], [self.odir_l, self.odir_e, self.odir_b], [1,2,2], [W, W+E, W+E])
        _grid_row(1, [0,1,3], [self.sim_l, self.sim_e, self.sim_b], [1,2,2], [W, W+E, W+E] )
        _grid_row(2, [0,1,2,3], [self.cutoff_l, self.cutoff_e, self.focus_chk, self.focus_e], [1,1,1,1], [W, W+E, W, W+E])

        self.odir_e.insert(0, '/home/anthony/Documents/Projects/drug_moa/test2/gn_focus/')
        self.sim_e.insert(0, '/home/anthony/Documents/Projects/drug_moa/test2/main/HGD_AVG.csv')
        self.cutoff_e.insert(0, '0.9')

    def validate(self):
        try:
            self.validate_path(self.odir_e.get(), "The directory %s was not found!"%(self.odir_e.get()), os.path.exists) 
            self.validate_path(self.sim_e.get(), "The file %s was not found!"%(self.sim_e.get()), os.path.exists)
            self.validate_cutoff()
            if self.focus_val.get():
                self.validate_focus()
            return 1
        except OSError:
            return 0


    def mark(self):
        def FUN(x):
            if self.focus_val.get():
                if x == '': return None
                else: return x
            else: return None
        names = ['odir', 'ifname', 'cutoff', 'focus']
        items = [self.odir_e, self.sim_e, self.cutoff_e, self.focus_e]
        funcs = [str, str, float, FUN]

        self.marked = zip(names, items, funcs)

class ViewNet(BaseDialog):

    def construct(self):
        _grid_row(0, [0,1,3], [self.odir_l, self.odir_e, self.odir_b], [1,2,2], [W, W+E, W+E])

    def validate(self):
        try:
            self.validate_path(self.odir_e.get(), "The directory %s was not found!"%(self.odir_e.get()), os.path.exists)
            return 1
        except OSError:
            return 0

    def mark(self):
        names = ['idir']
        items = [self.odir_e]
        funcs = [str]

        self.marked = zip(names, items, funcs)

class MainDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        #self.text = Text(master, width = 32, height = 10, bg = '#DDD', bd = 0)
        #self.text.insert(END, 'Info\n\n')
        #self.text.insert(END, 'If you want to know...')
        #self.text.grid(row = 0, column = 2, rowspan = 10)
        #self.text.config(state = DISABLED)

        self.b1 = Button(master, text = "Create HGD from Expression Matrix", command = self.f1)
        self.b2 = Button(master, text = "Create HGD from Signature Files", command = self.f2)
        self.b3 = Button(master, text = "Add to HGD from Expression Matrix", command = self.f3)
        self.b4 = Button(master, text = "Add to HGD from Signature Files", command = self.f4)
        self.b5 = Button(master, text = "Network Analysis of HGD", command = self.f5)
        self.b6 = Button(master, text = "View Network", command = self.f6)

        Label(master, text = "Create").grid(row = 0, sticky = W)
        ttk.Separator(master, orient = HORIZONTAL).grid(row = 1, sticky = W+E)
        self.b1.grid(row = 2, sticky = W + E)
        self.b2.grid(row = 3, sticky = W + E)
        Label(master, text = "   ").grid(row = 4)
        Label(master, text = "Add").grid(row = 5, sticky = W)
        ttk.Separator(master, orient = HORIZONTAL).grid(row = 6, sticky = W+E)
        self.b3.grid(row = 7, sticky = W + E)
        self.b4.grid(row = 8, sticky = W + E)
        Label(master, text = "   ").grid(row = 9)
        Label(master, text = "View").grid(row = 10, sticky = W)
        ttk.Separator(master, orient = HORIZONTAL).grid(row = 6, sticky = W+E)
        self.b5.grid(row = 11, sticky = W + E)
        self.b6.grid(row = 12, sticky = W + E)

    def _f(self, dialog, title, post_fun):
        def FUN():
            query = dialog(self, title = title)
            result = query.result
            if not result: pass
            else: post_fun(**result)
        return FUN

    def f1(self): 
        self._f(CreateExpr, "Create Similarity Matrix from Expression Data", interface.create_hgd_from_expr)()

    def f2(self): 
        self._f(CreateSigs, "Create Similarity Matrix from Signature Files", interface.create_hgd_from_sigs)()

    def f3(self): self._f(AddExpr, "Augment Similarity Matrix from Expression Data", interface.add_hgd_from_expr)()

    def f4(self): self._f(AddSigs, "Augment Similarity Matrix from Signature Files", interface.add_hgd_from_sigs)()

    def f5(self): self._f(AnalyzeNet, "Find Clusters", interface.gn_go)()

    def f6(self): self._f(ViewNet, "View Network", interface.view_gn)()
    
if __name__ == '__main__':
    root = Tk()
    root.withdraw()

    MainDialog(root, title = "Main")
