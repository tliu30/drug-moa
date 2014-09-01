import os
from Tkinter import *
from ScrolledText import *
from sigs import *
import tkSimpleDialog

class SigMsgBox:

    def __init__(self, parent, fnames):
        self.fnames = fnames
        self.parent = parent
        self.top = Toplevel(parent)
        self.result = None

        Label(self.top, text = "Verify that the size of the signatures is as expected: ").grid(row = 0, columnspan = 2)

        self.text = ScrolledText(self.top, bg = '#D9D9D9', width = 32, height = 10)
        self.text.config(state = DISABLED)
        self.text.grid(row = 1, columnspan = 2)

        self.ok_b = Button(self.top, text = "OK", command = self.ok)
        self.no_b = Button(self.top, text = "No", command = self.cancel)

        self.ok_b.grid(row = 2, column = 0)
        self.no_b.grid(row = 2, column = 1)

        self.add_sigs()

    def ok(self):
        self.result = 1
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    def cancel(self):
        self.result = 0
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    def destroy(self):
        self.top.destroy()

    def add_sigs(self):
        self.text.config(state = NORMAL)
        for fname in self.fnames:
            name = os.path.splitext( os.path.split(fname)[1] )[0]
            ct = str( map(lambda x: len(x), read_sig_file(fname) ) )
            self.text.insert(END, name + ' ' + ct + '\n')
        self.text.config(state = DISABLED)

if __name__ == "__result__":
    root = Tk(); root.withdraw()
    a = SigMsgBox(root, ['./test/sigs/' + x for x in os.listdir('./test/sigs')])
    root.wait_window(a.top)
    print a.result
