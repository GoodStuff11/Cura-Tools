import tkinter as tk
from tkinter import ttk
import os
import shutil
import pathlib


class Window(tk.Frame):
    # window number
    i = 0

    VARIABLES = []

    # binary list of which profiles and materials you want to export, from checkboxes
    profiles_check = []
    materials_check = []

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("Cura Exporter")
        self.windows = [self.window1, self.window2, self.window3, self.window4]
        self.windows_skip = [1] * len(self.windows)

        cura_address = str(pathlib.Path.home()).replace('\\', '/') + '/AppData/Roaming/cura'
        self.cura_dir = cura_address + '/' + os.walk(cura_address).__next__()[1][-1]

        self.config(padx=10, pady=10)
        self.grid(column=0, row=0)

        # window 1
        self.settings = [tk.IntVar(), tk.IntVar()]  # material profile
        self.VARIABLES += self.settings

        self.back_button1 = ttk.Button(self, text='Back', command=self.last_window)
        self.upperLabel1 = ttk.Label(self, text='Export material or profile settings?')
        self.checkMaterial1 = ttk.Checkbutton(self, text='Material', variable=self.settings[0])
        self.checkProfile1 = ttk.Checkbutton(self, text='Profile', variable=self.settings[1])
        self.next_button1 = ttk.Button(self, text='Next', command=self.ignore, state=tk.DISABLED)

        # window 2
        self.profiles = []
        self.new_profiles = []
        self.check_box2 = []
        self.entries2 = []
        self.upperLabel2 = ttk.Label(self, text='Select which profiles you would like to export.\n'
                                                'Input the name you want the files to be renamed to.\n'
                                                'Inputting nothing will keep it as is.')
        self.next_button2 = ttk.Button(self, text='Next', command=self.ignore, state=tk.DISABLED)
        self.back_button2 = ttk.Button(self, text='Back', command=self.last_window)

        # window 3
        self.materials = []
        self.new_materials = []
        self.check_box3 = []
        self.entries3 = []
        self.upperLabel3 = ttk.Label(self, text='Select which materials you would like to export.\n'
                                                'Input the name you want the files to be renamed to.\n'
                                                'Inputting nothing will keep it as is.')
        self.next_button3 = ttk.Button(self, text='Next', command=self.ignore, state=tk.DISABLED)
        self.back_button3 = ttk.Button(self, text='Back', command=self.last_window)

        # window 4
        self.lowerLabel4 = ttk.Label(self, text='')
        self.upperLabel4 = ttk.Label(self, text='Please input the directory where you want to export,\n'
                                                'typing in nothing will export to the file of the executable')
        self.folder_name = tk.StringVar()
        self.VARIABLES.append(self.folder_name)
        self.entry4 = ttk.Entry(self, textvariable=self.folder_name)
        self.next_button4 = ttk.Button(self, text='Export')
        self.back_button4 = ttk.Button(self, text='Back', command=self.last_window)

        self.update_window()

    def run(self):
        # create folder to export to
        n = 0
        name = self.folder_name.get() + '/' + 'EXPORTED CuraFiles #'
        while os.path.exists(name + str(n)):
            n += 1
        address = name + str(n)
        os.makedirs(address)
        if self.settings[1].get() == 1:
            os.makedirs(address + '/profiles')
        if self.settings[0].get() == 1:
            os.makedirs(address + '/materials')

        # profiles
        directory = os.listdir(self.cura_dir + self.profile_folder(self.cura_dir))
        for d in directory:
            with open(self.cura_dir + self.profile_folder(self.cura_dir) + '/' + d, 'r') as file:
                lines = file.readlines()
            if lines[2][7:-1] in [self.profiles[i] for i in range(len(self.profiles)) if self.profiles_check[i].get() == 1]:
                # make copy of profile
                shutil.copy(self.cura_dir + self.profile_folder(self.cura_dir) + '/' + d, address + '/profiles')

                # rename copied profile
                if self.new_profiles[self.profiles.index(lines[2][7:-1])].get() != '':
                    lines[2] = 'name = ' + self.new_profiles[self.profiles.index(lines[2][7:-1])].get() + '\n'
                with open(address + '/profiles/' + d, 'w') as file:
                    for L in lines:
                        file.write(L)

        # materials
        directory = os.listdir(self.cura_dir + '/materials')
        for d in directory:
            with open(self.cura_dir + '/materials/' + d, 'r') as file:
                lines = file.readlines()

            name_line = lines[7][13:-9]
            if name_line == '':
                name_line = lines[4][13:-9] + ' ' + lines[6][13:-9] + ' ' + lines[5][16:-12]

            if name_line in [self.materials[i] for i in range(len(self.materials)) if self.materials_check[i].get() == 1]:
                shutil.copy(self.cura_dir + '/materials/' + d, address + '/materials')
                # check if the new name is blank
                if self.new_materials[self.materials.index(name_line)].get() != '':
                    lines[7] = '      <label>' + self.new_materials[self.materials.index(name_line)].get() + '</label>\n'
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

    @staticmethod
    def profile_folder(address):
        address = address.replace('\\', '/')
        if os.path.exists(address + '/quality_changes'):
            return '/quality_changes'
        else:
            return '/quality'

    def window1(self):
        self.next_button1.grid(row=3, column=1)
        self.upperLabel1.grid(row=0, column=0)
        self.checkMaterial1.grid(row=1, column=0, sticky=tk.W)
        self.checkProfile1.grid(row=2, column=0, sticky=tk.W)

        def callback(*arg):
            self.windows_skip[3] = self.settings[0].get()  # material
            self.windows_skip[2] = self.settings[1].get()  # profile
            # select at least one of the check boxes to continue
            if all(i.get() == 0 for i in self.settings):
                self.next_button1.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button1.config(state=tk.NORMAL, command=self.next_window)

        for i in self.settings:
            i.trace('w', callback)

    def window2(self):
        # asks for profiles to export
        # PROFILES
        s = self.cura_dir + self.profile_folder(self.cura_dir)

        # get profile names
        if len(self.profiles_check) == 0:
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
                self.entries2.append(entry)
                self.check_box2.append(check)

        self.upperLabel2.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        for i in range(len(self.entries2)):
            self.check_box2[i].grid(row=1 + i, column=0, sticky=tk.W)
            self.entries2[i].grid(row=1 + i, column=1, sticky=tk.E)

        self.back_button2.grid(row=1 + len(self.profiles), column=0, sticky=tk.W)
        self.next_button2.grid(row=1 + len(self.profiles), column=1, sticky=tk.E)

        def callback(*arg):
            if all(i.get() == 0 for i in self.profiles_check):
                self.next_button2.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button2.config(state=tk.NORMAL, command=self.next_window)

        for i in self.profiles_check:
            i.trace('w', callback)

    def window3(self):
        # asks for materials to export

        # MATERIALS
        s = self.cura_dir + '/materials'

        # get profile names
        if len(self.materials_check) == 0:
            directory = os.listdir(s)
            for d in directory:
                with open(s + '/' + d, 'r') as file:
                    lines = file.readlines()
                if lines[7][13:-9] not in self.materials:
                    if lines[7][13:-9] == '':
                        self.materials.append(lines[4][13:-9] + ' ' + lines[6][13:-9] + ' ' + lines[5][16:-12])
                    else:
                        self.materials.append(lines[7][13:-9])
            self.materials_check = [tk.IntVar() for i in self.materials]
            self.VARIABLES += self.materials_check

            # create check boxes
            for i in range(len(self.materials)):
                self.new_materials.append(tk.StringVar())
                self.VARIABLES.append(self.new_materials[-1])
                check = ttk.Checkbutton(self, variable=self.materials_check[i], text=self.materials[i])
                entry = ttk.Entry(self, textvariable=self.new_materials[-1])
                self.entries3.append(entry)
                self.check_box3.append(check)

        self.upperLabel3.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        for i in range(len(self.entries3)):
            self.check_box3[i].grid(row=1 + i, column=0, sticky=tk.W)
            self.entries3[i].grid(row=1 + i, column=1, sticky=tk.E)
        self.back_button3.grid(row=1 + len(self.materials), column=0, sticky=tk.W)
        self.next_button3.grid(row=1 + len(self.materials), column=1, sticky=tk.E)

        def callback(*arg):
            if all(i.get() == 0 for i in self.materials_check):
                self.next_button3.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button3.config(state=tk.NORMAL, command=self.next_window)

        for i in self.materials_check:
            i.trace('w', callback)

    def window4(self):
        # asks for which folder to put exported files into
        def check_dir():
            s = self.folder_name.get().replace('\\', '/')
            if os.path.exists(s):
                self.run()
            elif s == '':
                self.folder_name.set('.')
                self.run()
            else:
                self.lowerLabel4.config(text='Cannot find this directory.', foreground='red')

        self.upperLabel4.grid(row=0, column=0)
        self.entry4.grid(row=1, column=0, sticky=tk.W)
        self.entry4.config(width=40)
        self.lowerLabel4.grid(row=2, column=0)
        self.lowerLabel4.config(text='')
        self.next_button4.grid(row=3, column=0, sticky=tk.E)
        self.back_button4.grid(row=3, column=0, sticky=tk.W)
        self.next_button4.config(command=check_dir)


def main():
    root = tk.Tk()
    Window(root)
    root.mainloop()


main()
