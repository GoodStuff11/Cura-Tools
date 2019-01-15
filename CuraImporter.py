import tkinter as tk
from tkinter import ttk
import os
import shutil
import re
import pathlib


class Window(tk.Frame):
    i = 0
    VARIABLES = []

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("Cura Importer")
        self.windows = [self.window0, self.window1, self.window2]

        # get address of cura and the latest cura version you have
        self.cura_address = str(pathlib.Path.home()).replace('\\', '/') + '/AppData/Roaming/cura'
        versions = os.walk(self.cura_address).__next__()[1]
        for v in versions[::-1]:
            if not os.path.exists(self.cura_address + '/' + v + '/cura.cfg'):
                versions.remove(v)

        # define later
        self.cura_dir = ''

        self.config(padx=10, pady=10)
        self.grid(column=0, row=0)

        # window 0
        self.upperLabel0 = ttk.Label(self, text='Select a Cura version to import to.')
        self.radiobuttons0 = []
        self.radiobuttons_var0 = tk.StringVar()
        self.radiobuttons_var0.set(versions[-1])
        for v in versions:
            temp = ttk.Radiobutton(self, text=v, value=v, variable=self.radiobuttons_var0)
            self.radiobuttons0.append(temp)

        self.cura_dir = self.cura_address + '/' + self.radiobuttons_var0.get()
        self.cura_profile_dir = self.cura_dir + self.profile_folder(self.cura_dir)

        self.next_button0 = ttk.Button(self, text='Next', command=self.next_window)
        self.skipped = False
        if len(versions) == 1:
            self.skipped = True
            self.i = 1

        self.config(padx=10, pady=10)
        self.grid(column=0, row=0)

        # window 1
        self.lowerLabel1 = ttk.Label(self, text='')
        self.upperLabel1 = ttk.Label(self, text='Please input the directory where you want to import,\n'
                                                'typing in nothing will import from the folder of the executable')
        self.folder_dir = tk.StringVar()
        self.VARIABLES.append(self.folder_dir)
        self.entry1 = ttk.Entry(self, textvariable=self.folder_dir)
        self.next_button1 = ttk.Button(self, text='Next')
        self.back_button1 = ttk.Button(self, text='Back', command=self.last_window)

        # window 2
        self.exported_folders = []  # folder names
        self.folders_check = []  # variables of folder checkboxes

        self.check_box2 = []
        self.upperLabel2 = ttk.Label(self, text='Select the exported folders which you want to import to Cura.\n'
                                                'Your folder must be in the same folder as the one listed \nbefore to appear.')
        self.import_button2 = ttk.Button(self, text='Import', command=self.ignore, state=tk.DISABLED)
        self.back_button2 = ttk.Button(self, text='Back', command=self.last_window)
        self.update_window()

    @staticmethod
    def find(string, search_list):
        for l in search_list:
            if re.search(string, l) is not None:
                return l  # setting_version = 4

    @staticmethod
    def index(string, search_list):
        for i in range(len(search_list)):
            if re.search(string, search_list[i]) is not None:
                return i  # setting_version = 4

    def run(self):
        # get the needed information in order for the profile to be compatible with earlier versions
        # this includes: extruder = custom_extruder_1
        # as well that the version must be correct
        for folder_name in self.exported_folders:
            extruders = []
            for ext_file in os.listdir(self.cura_dir + self.extruder_folder(self.cura_dir)):
                try:
                    file = open(self.cura_dir + self.extruder_folder(self.cura_dir) + '/' + ext_file, 'r')
                    lines = file.readlines()
                    profile_version = lines[1]  # version = 4
                    extruders.append(lines[3].split(' ')[-1])  # definition = custom_extruder_1
                    file.close()
                except PermissionError:
                    pass

            extruders.sort(key=lambda x: -len(x))  # sorts from largest to smallest

            for ext_file in os.listdir(self.cura_dir + '/extruders'):
                try:
                    file = open(self.cura_dir + '/extruders/' + ext_file, 'r')
                    lines = file.readlines()
                    setting_version = self.find('setting_version', lines)
                    file.close()
                    break
                except PermissionError:
                    pass

            # import profiles if the profile folder is in the EXPORTED CuraFiles #N folder
            if os.path.exists(self.folder_dir + '/' + folder_name + '/profiles'):
                directory_information = []
                directory = os.listdir(self.folder_dir + '/' + folder_name + '/profiles')
                directory.sort(key=lambda x: -len(x))
                # consider os.walk
                # https://stackoverflow.com/questions/18383384/python-copy-files-to-a-new-directory-and-rename-if-file-name-already-exists
                for file_name in directory:
                    n = 0
                    new_file_name = file_name
                    # if the file in Cura has the same name as the imported one
                    if os.path.exists(self.cura_dir + self.profile_folder(self.cura_dir) + '/' + file_name):
                        # go through numberings until you get a unique one
                        # C:/Users/htpc/AppData/Roaming/cura/3.6/quality_change/

                        # NAMING CONVENTION CAN USE SOME WORK
                        while os.path.exists(
                                self.cura_dir + self.profile_folder(self.cura_dir) + '/' + file_name[:-9] + '_' + str(
                                    n) + '.inst.cfg'):
                            n += 1
                        new_file_name = file_name[:-9] + '_' + str(n) + '.inst.cfg'

                    with open(self.folder_dir + '/' + folder_name + '/profiles/' + file_name, 'r') as f:
                        file_lines = f.readlines()
                        name = file_lines[2][7:-1]

                    # check if any files have the same name
                    dup_count = 1
                    duplicates = True
                    while duplicates:
                        duplicates = False
                        for di in os.listdir(self.cura_dir + self.profile_folder(self.cura_dir) + '/'):
                            try:
                                f = open(self.cura_dir + self.profile_folder(self.cura_dir) + '/' + di, 'r')
                                cura_lines = f.readlines()
                                if cura_lines[2][7:-1] == name and dup_count == 1 or cura_lines[2][
                                                                                     7:-1] == name + ' #' + str(
                                    dup_count) and dup_count != 1:
                                    dup_count += 1
                                    duplicates = True
                                    break
                                f.close()
                            except PermissionError:
                                pass

                    # get extruder name and send that information
                    found = False
                    for ext in extruders:
                        # ext[-1] is to remove \n
                        if re.search(ext[:-1], file_name) is not None:
                            # gives all important information for file
                            found = True
                            directory_information.append([file_name, new_file_name, dup_count, ext])
                            extruders.remove(ext)
                            break
                    if not found:
                        directory_information.append([file_name, new_file_name, dup_count, None])

                # add to the file once all information has been received
                for d in directory_information:
                    with open(self.folder_dir + '/' + folder_name + '/profiles/' + d[0], 'r') as file:
                        lines = file.readlines()
                    shutil.copy(self.folder_dir + '/' + folder_name + '/profiles/' + d[0],
                                self.cura_dir + self.profile_folder(self.cura_dir) + '/' + d[1])

                    # modify the file
                    if d[2] != 1:
                        lines[2] = lines[2][:-1] + ' #' + str(d[2]) + '\n'
                    # insert "extruder = " only if an extruder was found AND "extruder = " isnt currently in the file
                    # having multiple "extruder=" causes corruption
                    if d[3] is not None and 'extruder = ' + d[3] not in lines:
                        lines.insert(7, 'extruder = ' + d[3])  # specify the extruder of the profile
                    lines[self.index('version', lines)] = profile_version  # update version
                    lines[self.index('setting_version', lines)] = setting_version
                    with open(self.cura_dir + self.profile_folder(self.cura_dir) + '/' + d[1], 'w') as file:
                        for L in lines:
                            file.write(L)

            # ---------------------------------------------------------
            # import profiles if the materials folder is in the EXPORTED CuraFiles #N folder
            if os.path.exists(self.folder_dir + '/' + folder_name + '/materials'):
                directory = os.listdir(self.folder_dir + '/' + folder_name + '/materials')
                for file_name in directory:
                    dup_count = 0
                    if os.path.exists(self.cura_dir + '/materials/' + file_name):
                        while os.path.exists(
                                self.cura_dir + '/materials/' + file_name[:-17] + str(dup_count) + '.xml.fdm_material'):
                            dup_count += 1

                    shutil.copy(
                        self.folder_dir + '/' + folder_name + '/materials/' + file_name[:-17] + '.xml.fdm_material',
                        self.cura_dir + '/materials/' + file_name[:-17] + str(dup_count) + '.xml.fdm_material')

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
        self.update_window()

    def last_window(self):
        self.i -= 1
        self.update_window()

    def ignore(self):
        pass

    def update_window(self):
        self.clear(self)
        self.windows[self.i]()

    # Cura profiles folder name. It was /quality until 3.4, where it was converted to /quality_change.
    # quality_change is prioritized since it is the newer version, but program will pick /quailty if it doesn't
    # exist
    @staticmethod
    def profile_folder(address):
        address = address.replace('\\', '/')
        if os.path.exists(address + '/quality_changes'):
            return '/quality_changes'
        else:
            return '/quality'

    @staticmethod
    def extruder_folder(address):
        address = address.replace('\\', '/')
        if os.path.exists(address + '/definition_changes'):
            return '/definition_changes'
        else:
            return '/definition'

    def window0(self):
        self.next_button0.grid(row=len(self.radiobuttons0) + 1, column=0, sticky=tk.E)
        self.upperLabel0.grid(row=0, column=0)
        for i in range(len(self.radiobuttons0)):
            self.radiobuttons0[i].grid(row=i + 1, column=0, sticky=tk.W)

        def callback(*arg):
            self.cura_dir = self.cura_address + '/' + self.radiobuttons_var0.get()

        self.radiobuttons_var0.trace('w', callback)

    def window1(self):
        # asks for which folder to put exported files into
        def check_dir():
            s = self.folder_dir.get().replace('\\', '/')
            if os.path.exists(s):
                self.next_window()
            elif s == '':
                self.folder_dir.set('.')
                self.next_window()
            else:
                self.lowerLabel1.config(text='Cannot find this directory.', foreground='red')

        def callback(*arg):
            if len(self.exported_folders) != 0:
                self.check_box2 = []

                self.folders_check = []
                self.exported_folders = []

        self.upperLabel1.grid(row=0, column=0)
        self.entry1.grid(row=1, column=0, sticky=tk.W)
        self.entry1.config(width=40)
        self.lowerLabel1.grid(row=2, column=0)
        self.lowerLabel1.config(text='')
        self.next_button1.grid(row=3, column=0, sticky=tk.E)
        self.back_button1.grid(row=3, column=0, sticky=tk.W)
        self.next_button1.config(command=check_dir)

        self.folder_dir.trace('w', callback)

    def window2(self):
        # get names of folders that were exported from CuraExporter
        self.exported_folders = []
        directory = os.listdir(self.folder_dir.get())
        for d in directory:
            if os.path.exists(self.folder_dir.get() + '/' + d + '/profiles') or os.path.exists(
                    self.folder_dir.get() + '/' + d + '/materials'):
                self.exported_folders.append(d)
        folders_check = [tk.IntVar() for i in self.exported_folders]
        self.VARIABLES += folders_check

        # create check boxes
        for i in range(len(self.exported_folders)):
            check = ttk.Checkbutton(self, variable=folders_check[i], text=self.exported_folders[i])
            self.check_box2.append(check)

        self.upperLabel2.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        for i in range(len(self.exported_folders)):
            self.check_box2[i].grid(row=1 + i, column=0, sticky=tk.W)
        self.import_button2.grid(row=1 + len(self.exported_folders), column=1, sticky=tk.E)
        if not self.skipped:
            self.back_button2.grid(row=1 + len(self.exported_folders), column=0, sticky=tk.W)

        def callback(*arg):
            if all(i.get() == 0 for i in folders_check):
                self.import_button2.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.import_button2.config(state=tk.NORMAL, command=self.run)

        for i in folders_check:
            i.trace('w', callback)


def main():
    root = tk.Tk()
    Window(root)
    root.mainloop()


main()
