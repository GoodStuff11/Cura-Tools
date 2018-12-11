import tkinter as tk
from tkinter import ttk
import os
import shutil


class Window(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.i = 0
        self.windows = [self.window1, self.window2, self.window3, self.window4, self.window5]
        self.windows_skip = [1 for i in self.windows]

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

        # window 2
        self.settings = [tk.IntVar(), tk.IntVar()]  # material profile
        self.VARIABLES += self.settings

        if self.i == 0:
            self.skipped = True
        self.back_button2 = ttk.Button(self, text='Back', command=self.last_window)
        self.upperLabel2 = ttk.Label(self, text='Export material or profile settings?')
        self.checkMaterial2 = ttk.Checkbutton(self, text='Material', variable=self.settings[0])
        self.checkProfile2 = ttk.Checkbutton(self, text='Profile', variable=self.settings[1])
        self.next_button2 = ttk.Button(self, text='Next', command=self.ignore, state=tk.DISABLED)

        # window 3
        self.profiles = []
        self.new_profiles = []
        self.check_box3 = []
        self.entries3 = []
        self.upperLabel3 = ttk.Label(self, text='Select which profiles you would like to export.\nInput the name you want the files to be renamed to.\nInputting nothing will keep it as is.')
        self.next_button3 = ttk.Button(self, text='Next', command=self.ignore, state=tk.DISABLED)
        self.back_button3 = ttk.Button(self, text='Back', command=self.last_window)

        # window 4
        self.materials = []
        self.new_materials = []
        self.check_box4 = []
        self.entries4 = []
        self.upperLabel4 = ttk.Label(self, text='Select which materials you would like to export.\nInput the name you want the files to be renamed to.\nInputting nothing will keep it as is.')
        self.next_button4 = ttk.Button(self, text='Next', command=self.ignore, state=tk.DISABLED)
        self.back_button4 = ttk.Button(self, text='Back', command=self.last_window)

        # window 5
        self.lowerLabel5 = ttk.Label(self, text='')
        self.upperLabel5 = ttk.Label(self, text='Please input the directory where you want to export,\ntyping in nothing will export to the file of the executable')
        self.dir2 = tk.StringVar()
        self.VARIABLES.append(self.dir2)
        self.entry5 = ttk.Entry(self,textvariable=self.dir2)
        self.next_button5 = ttk.Button(self, text='Export')
        self.back_button5 = ttk.Button(self, text='Back', command=self.last_window)

        self.update_window()

    def run(self):
        file = open('./Cura_Directory', 'r')
        s = file.readline()
        file.close()

        # create folder to export to
        n = 0
        name = self.dir2.get() + '/' + 'EXPORTED CuraFiles #'
        while os.path.exists(name + str(n)):
            n += 1
        address = name + str(n)
        os.makedirs(address)
        if self.settings[1].get() == 1:
            os.makedirs(address + '/profiles')
        if self.settings[0].get() == 1:
            os.makedirs(address + '/materials')

        directory = os.listdir(s + '/quality_changes')
        for d in directory:
            with open(s + '/quality_changes/' + d, 'r') as file:
                lines = file.readlines()
            if lines[2][7:-1] in [self.profiles[i] for i in range(len(self.profiles)) if self.profiles_check[i].get() == 1]:

                # make copy of profile
                shutil.copy(s + '/quality_changes/' + d, address + '/profiles')

                # rename copied profile
                lines[2] = 'name = ' + self.new_profiles[self.profiles.index(lines[2][7:-1])].get() + '\n'
                with open(address + '/profiles/' + d, 'w') as file:
                    for L in lines:
                        file.write(L)

        directory = os.listdir(s + '/materials')
        for d in directory:
            with open(s + '/materials/' + d, 'r') as file:
                lines = file.readlines()
            if lines[7][13:-9] in [self.materials[i] for i in range(len(self.materials)) if self.materials_check[i].get() == 1]:
                shutil.copy(s + '/materials/' + d, address + '/materials')
                lines[7] = '      <label>' + self.new_materials[self.materials.index(lines[7][13:-9])].get() + '</label>\n'
                with open(address + '/materials/' + d, 'w') as file:
                    for L in lines:
                        file.write(L)

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
            self.back_button2.grid(row=3, column=0)
        self.next_button2.grid(row=3, column=1)
        self.upperLabel2.grid(row=0, column=0)
        self.checkMaterial2.grid(row=1, column=0, sticky=tk.W)
        self.checkProfile2.grid(row=2, column=0, sticky=tk.W)

        def callback(*arg):
            self.windows_skip[3] = self.settings[0].get() #material
            self.windows_skip[2] = self.settings[1].get() #profile

            if all(i.get() == 0 for i in self.settings):
                self.next_button2.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button2.config(state=tk.NORMAL, command=self.next_window)

        for i in self.settings:
            i.trace('w', callback)

    def window3(self):
        # PROFILES
        file = open('./Cura_Directory', 'r')
        s = file.readline() + '/quality_changes'
        file.close()

        # get profile names
        if not hasattr(self, 'profiles_check'):
            directory = os.listdir(s)
            for d in directory:
                with open(s + '/' + d, 'r') as file:
                    lines = file.readlines()
                if lines[2][7:-1] not in self.profiles:
                    self.profiles.append(lines[2][7:-1])
            self.profiles_check = [tk.IntVar() for i in self.profiles]
            self.VARIABLES += self.profiles_check

            # create check boxes
            for i in range(len(self.profiles)):
                self.new_profiles.append(tk.StringVar())
                self.VARIABLES.append(self.new_profiles[-1])
                entry = ttk.Entry(self, textvariable=self.new_profiles[-1])
                check = ttk.Checkbutton(self, variable=self.profiles_check[i], text=self.profiles[i])
                self.entries3.append(entry)
                self.check_box3.append(check)

        self.upperLabel3.grid(row=0, column=0)
        for i in range(len(self.entries3)):
            self.check_box3[i].grid(row=1 + i, column=0, sticky=tk.W)
            self.entries3[i].grid(row=1 + i, column=0, sticky=tk.E)

        self.back_button3.grid(row=1 + len(self.profiles), column=0, sticky=tk.W)
        self.next_button3.grid(row=1 + len(self.profiles), column=0, sticky=tk.E)

        def callback(*arg):
            if all(i.get() == 0 for i in self.profiles_check):
                self.next_button3.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button3.config(state=tk.NORMAL, command=self.next_window)

        for i in self.profiles_check:
            i.trace('w', callback)

    def window4(self):
        # MATERIALS
        file = open('./Cura_Directory', 'r')
        s = file.readline() + '/materials'
        file.close()

        # get profile names
        if not hasattr(self, 'materials_check'):
            directory = os.listdir(s)
            for d in directory:
                with open(s + '/' + d, 'r') as file:
                    lines = file.readlines()
                if lines[7][13:-9] not in self.materials:
                    self.materials.append(lines[7][13:-9])
            self.materials_check = [tk.IntVar() for i in self.materials]
            self.VARIABLES += self.materials_check

            # create check boxes
            for i in range(len(self.materials)):
                self.new_materials.append(tk.StringVar())
                self.VARIABLES.append(self.new_materials[-1])
                check = ttk.Checkbutton(self, variable=self.materials_check[i], text=self.materials[i])
                entry = ttk.Entry(self, textvariable=self.new_materials[-1])
                self.entries4.append(entry)
                self.check_box4.append(check)

        self.upperLabel4.grid(row=0, column=0)
        for i in range(len(self.entries4)):
            self.check_box4[i].grid(row=1 + i, column=0, sticky=tk.W)
            self.entries4[i].grid(row=1 + i, column=0, sticky=tk.E)
        self.back_button4.grid(row=1 + len(self.materials), column=0, sticky=tk.W)
        self.next_button4.grid(row=1 + len(self.materials), column=0, sticky=tk.E)

        def callback(*arg):
            if all(i.get() == 0 for i in self.materials_check):
                self.next_button4.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button4.config(state=tk.NORMAL, command=self.next_window)

        for i in self.materials_check:
            i.trace('w', callback)

    def window5(self):
        def checkDir():
            s = self.dir2.get().replace('\\', '/')
            if os.path.exists(s):
                self.run()
            elif s == '':
                self.dir2.set('.')
                self.run()
            else:
                self.lowerLabel5.config(text='Cannot find this directory.', foreground='red')

        self.upperLabel5.grid(row=0, column=0)
        self.entry5.grid(row=1, column=0, sticky=tk.W)
        self.entry5.config(width=40)
        self.lowerLabel5.grid(row=2, column=0)
        self.lowerLabel5.config(text='')
        self.next_button5.grid(row=3, column=0, sticky=tk.E)
        self.back_button5.grid(row=3, column=0, sticky=tk.W)
        self.next_button5.config(command=checkDir)

def main():
    root = tk.Tk()
    root.title("Cura Exporter")
    Window(root)
    root.mainloop()


main()
