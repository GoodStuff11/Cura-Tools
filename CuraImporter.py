import tkinter as tk
from tkinter import ttk
import os
import shutil


class Window(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.i = 0
        self.windows = [self.window1, self.window2]

        self.config(padx=10, pady=10)
        self.grid(column=0, row=0)
        self.skipped = False

        self.VARIABLES = []

        self.dir = tk.StringVar()
        self.VARIABLES.append(self.dir)

        if os.path.isfile('./Cura_Directory'):
            f = open('./Cura_Directory')
            self.dir.set(f.readline())
            f.close()
            self.i += 1

        # Window 1
        self.next_button1 = ttk.Button(self, text='Next', command=self.ignore, state=tk.DISABLED)
        self.lowerLabel1 = ttk.Label(self, text='')
        self.upperLabel1 = ttk.Label(self,
                                     text='Cura > help > show configuration folder\nCopy and paste directory')
        self.entry1 = ttk.Entry(self, textvariable=self.dir)
        self.entry1.config(width=35)

        # Window 2
        self.upperLabel2 = ttk.Label(self, text='Please put the previously exported folder into the folder with the executable.\nPlease input the name of the folder you would like to import.')
        if self.i == 0:
            self.skipped = True
        self.dir = tk.StringVar()
        self.entry2 = ttk.Entry(self,textvariable=self.dir)
        self.next_button2 = ttk.Button(self,text='Import', state=tk.DISABLED, command=self.ignore)
        self.back_button2 = ttk.Button(self,text='Back')
        self.lowerLabel2 = ttk.Label(self, text='')

        self.update_window()

    def run(self):
        file = open('./Cura_Directory', 'r')
        s = file.readline()
        file.close()


        try:
            directory_information = []
            directory = os.listdir('./' + self.dir.get() + '/profiles')
            for d in directory:
                n = 0
                if os.path.exists(s + '/quality_changes/' + d):
                    new_d = d
                    while os.path.exists(s + '/quality_changes/' + d[:-9] + '_' + str(n) + '.inst.cfg'):
                        n += 1
                    new_d = d[:-9] + '_' + str(n) + '.inst.cfg'

                with open('./' + self.dir.get() + '/profiles/' + d, 'r') as file:
                    lines = file.readlines()
                    name = lines[2][7:-1]

                # check if any files have the same name
                N = 1
                duplicates = True
                while duplicates:
                    duplicates = False
                    for di in os.listdir(s + '/quality_changes'):
                        f = open(s + '/quality_changes/' + di,'r')
                        L = f.readlines()
                        if L[2][7:-1] == name and N == 1 or L[2][7:-1] == name + ' #' + str(N) and N != 1:
                            N += 1
                            duplicates = True
                            break
                        f.close()
                directory_information.append([d, new_d, N])
            # add to the file once all information has been received
            for d in directory_information:
                with open('./' + self.dir.get() + '/profiles/' + d[0], 'r') as file:
                    lines = file.readlines()
                shutil.copy('./' + self.dir.get() + '/profiles/' + d[0], s + '/quality_changes/' + d[1])
                lines[2] = lines[2][:-1] + ' #' + str(d[2]) + '\n'
                with open(s + '/quality_changes/' + d[1], 'w') as file:
                    for L in lines:
                        file.write(L)
        except:
            pass

        try:
            directory = os.listdir('./' + self.dir.get() + '/materials')
            for d in directory:
                n = 0
                if os.path.exists(s + '/materials/' + d):
                    while os.path.exists(s + '/materials/' + d[:-17] + str(n) + '.xml.fdm_material'):
                        n += 1
                    os.rename('./' + self.dir.get() + '/materials/' + d, './' + self.dir.get() + '/materials/' + d[:-17] + str(n) + '.xml.fdm_material')
                    d = d[:-17] + str(n) + '.xml.fdm_material'
                shutil.copy('./' + self.dir.get() + '/materials/' + d, s + '/materials')
        except:
            pass
        self.master.destroy()

    def clear(self, frame):
        # removing unused trace
        for p in self.VARIABLES:
            # iterate through all traces corresponding to each profile
            for t in p.trace_vinfo():
                p.trace_vdelete(t[0], t[1])
        # moving unused widgets
        for widget in frame.winfo_children():
            widget.grid_forget()

    def next_window(self):
        self.i += 1
        while self.windows_skip[self.i] == 0:
            self.i += 1
        self.update_window()

    def last_window(self):
        self.i -= 1
        while self.windows_skip[self.i] == 0:
            self.i -= 1
        self.update_window()

    def ignore(self):
        pass

    def update_window(self):
        self.clear(self)
        self.windows[self.i]()

    def window1(self):
        def checkDir():
            s = self.dir.get().replace('\\', '/') + '/quality_changes'
            if os.path.exists(s):
                if not os.path.exists('./Cura_Directory'):
                    file = open('./Cura_Directory', 'w+')
                    file.write(s[:-16])
                    file.close()
                self.next_window()
            else:
                self.lowerLabel1.config(text='Cannot find the right folder in this directory.', foreground='red')

        # update
        def callback(*args):
            if not self.dir.get():
                self.next_button1.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button1.config(state=tk.NORMAL, command=checkDir)

        self.dir.trace('w', callback)

        # first time
        if not self.dir.get():
            self.next_button1.config(state=tk.DISABLED, command=self.ignore)
        else:
            self.next_button1.config(state=tk.NORMAL, command=checkDir)

        # put each widget in place, reorient if was forgotten
        self.upperLabel1.grid(row=0, column=0, columnspan=3)
        self.lowerLabel1.grid(row=2, column=0, columnspan=2)
        self.lowerLabel1.config(text='')
        self.entry1.grid(row=1, sticky=tk.W, columnspan=2)
        self.next_button1.grid(row=3, column=1, columnspan=2)

    def window2(self):
        if self.skipped:
            self.back_button2.grid(row=3, column=0, sticky=tk.W)
        self.next_button2.grid(row=3, column=0, sticky=tk.E)
        self.upperLabel2.grid(row=0, column=0)
        self.lowerLabel2.grid(row=2, column=0)
        self.entry2.grid(row=1, column=0, sticky=tk.W)
        self.entry2.config(width=50)

        def check_dir():
            if os.path.exists('./' + self.dir.get()):
                self.run()
            else:
                self.lowerLabel2.config(text='Cannot find this directory.', foreground='red')

        def callback(*arg):
            if self.dir.get() == '':
                self.next_button2.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button2.config(state=tk.NORMAL, command=check_dir)

        self.dir.trace('w',callback)


def main():
    root = tk.Tk()
    root.title("Cura Exporter")
    Window(root)
    root.mainloop()


main()
