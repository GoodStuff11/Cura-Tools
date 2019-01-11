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
        self.windows = [self.window1]

        cura_address = str(pathlib.Path.home()).replace('\\', '/') + '/AppData/Roaming/cura'
        versions = os.walk(cura_address).__next__()[1]
        for v in versions[::-1]:
            if os.path.exists(cura_address + '/' + v + '/cura.cfg'):
                version = v
                break
        self.cura_dir = cura_address + '/' + version

        self.config(padx=10, pady=10)
        self.grid(column=0, row=0)

        # Window 1
        self.upperLabel1 = ttk.Label(self,
                                     text='Please put the previously exported folder into the folder with the executable.\n'
                                          'Please input the name of the folder you would like to import.')

        self.folder_name = tk.StringVar()
        self.entry1 = ttk.Entry(self, textvariable=self.folder_name)
        self.next_button1 = ttk.Button(self, text='Import')
        self.back_button1 = ttk.Button(self, text='Back')
        self.lowerLabel1 = ttk.Label(self, text='')

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
        if os.path.exists('./' + self.folder_name.get() + '/profiles'):
            directory_information = []
            directory = os.listdir('./' + self.folder_name.get() + '/profiles')
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
                    while os.path.exists(self.cura_dir + self.profile_folder(self.cura_dir) + '/' + file_name[:-9] + '_' + str(n) + '.inst.cfg'):
                        n += 1
                    new_file_name = file_name[:-9] + '_' + str(n) + '.inst.cfg'

                with open('./' + self.folder_name.get() + '/profiles/' + file_name, 'r') as f:
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
                            if cura_lines[2][7:-1] == name and dup_count == 1 or cura_lines[2][7:-1] == name + ' #' + str(dup_count) and dup_count != 1:
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
                with open('./' + self.folder_name.get() + '/profiles/' + d[0], 'r') as file:
                    lines = file.readlines()
                shutil.copy('./' + self.folder_name.get() + '/profiles/' + d[0],
                            self.cura_dir + self.profile_folder(self.cura_dir) + '/' + d[1])

                # modify the file
                if d[2] != 1:
                    lines[2] = lines[2][:-1] + ' #' + str(d[2]) + '\n'
                if d[3] is not None:
                    lines.insert(7, 'extruder = ' + d[3])  # specify the extruder of the profile
                lines[self.index('version', lines)] = profile_version  # update version
                lines[self.index('setting_version', lines)] = setting_version
                with open(self.cura_dir + self.profile_folder(self.cura_dir) + '/' + d[1], 'w') as file:
                    for L in lines:
                        file.write(L)

        # ---------------------------------------------------------
        # import profiles if the materials folder is in the EXPORTED CuraFiles #N folder
        if os.path.exists('./' + self.folder_name.get() + '/materials'):
            directory = os.listdir('./' + self.folder_name.get() + '/materials')
            for file_name in directory:
                dup_count = 0
                if os.path.exists(self.cura_dir + '/materials/' + file_name):
                    while os.path.exists(self.cura_dir + '/materials/' + file_name[:-17] + str(dup_count) + '.xml.fdm_material'):
                        dup_count += 1

                shutil.copy('./' + self.folder_name.get() + '/materials/' + file_name[:-17] + '.xml.fdm_material',
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

    def window1(self):

        self.next_button1.grid(row=3, column=0, sticky=tk.E)
        self.upperLabel1.grid(row=0, column=0)
        self.lowerLabel1.grid(row=2, column=0)
        self.entry1.grid(row=1, column=0, sticky=tk.W)
        self.entry1.config(width=50)

        def check_dir():
            if os.path.exists('./' + self.folder_name.get()) and self.folder_name.get():
                self.run()
            else:
                self.lowerLabel1.config(text='Cannot find this directory.', foreground='red')

        self.next_button1.config(command=check_dir)


def main():
    root = tk.Tk()
    Window(root)
    root.mainloop()


main()
