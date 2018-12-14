import tkinter as tk
from tkinter import ttk
import os
import shutil


class Window(tk.Frame):
    i = 0
    VARIABLES = []
    skipped = False

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.windows = [self.window1, self.window2]
        self.cura_dir = tk.StringVar()
        self.VARIABLES.append(self.cura_dir)

        self.config(padx=10, pady=10)
        self.grid(column=0, row=0)

        if os.path.exists('./Cura_Directory'):
            f = open('./Cura_Directory')
            self.cura_dir.set(f.readline())
            self.skipped = True
            f.close()
            self.i += 1

        # Window 1
        self.next_button1 = ttk.Button(self, text='Next')
        self.lowerLabel1 = ttk.Label(self, text='')
        self.upperLabel1 = ttk.Label(self,
                                     text='Cura > help > show configuration folder\n'
                                          'Copy and paste directory')
        self.entry1 = ttk.Entry(self, textvariable=self.cura_dir)
        self.entry1.config(width=35)

        # Window 2
        self.upperLabel2 = ttk.Label(self,
                                     text='Please put the previously exported folder into the folder with the executable.\n'
                                          'Please input the name of the folder you would like to import.')

        self.folder_name = tk.StringVar()
        self.entry2 = ttk.Entry(self, textvariable=self.folder_name)
        self.next_button2 = ttk.Button(self, text='Import')
        self.back_button2 = ttk.Button(self, text='Back')
        self.lowerLabel2 = ttk.Label(self, text='')

        self.update_window()

    def run(self):
        self.cura_dir = self.cura_dir.get()

        # import profiles if the profile folder is in the EXPORTED CuraFiles #N folder
        if os.path.exists('./' + self.folder_name.get() + '/profiles'):
            directory_information = []
            directory = os.listdir('./' + self.folder_name.get() + '/profiles')

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
                        f = open(self.cura_dir + self.profile_folder(self.cura_dir) + '/' + di, 'r')
                        cura_lines = f.readlines()
                        if cura_lines[2][7:-1] == name and dup_count == 1 or cura_lines[2][7:-1] == name + ' #' + str(dup_count) and dup_count != 1:
                            dup_count += 1
                            duplicates = True
                            break
                        f.close()
                directory_information.append([file_name, new_file_name, dup_count])

            # add to the file once all information has been received
            for d in directory_information:
                with open('./' + self.folder_name.get() + '/profiles/' + d[0], 'r') as file:
                    lines = file.readlines()
                shutil.copy('./' + self.folder_name.get() + '/profiles/' + d[0],
                            self.cura_dir + self.profile_folder(self.cura_dir) + '/' + d[1])

                # modify the file
                if d[2] != 1:
                    lines[2] = lines[2][:-1] + ' #' + str(d[2]) + '\n'
                with open(self.cura_dir + self.profile_folder(self.cura_dir) + '/' + d[1], 'w') as file:
                    for L in lines:
                        file.write(L)

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

    def window1(self):
        def check_dir():
            # Cura profiles directory
            cura_profile_dir = self.cura_dir.get() + self.profile_folder(self.cura_dir.get())
            if os.path.exists(cura_profile_dir):
                # write Cura directory to file for future use
                if not os.path.exists('./Cura_Directory'):
                    file = open('./Cura_Directory', 'w+')
                    file.write(self.cura_dir.get())
                    file.close()
                self.next_window()
            else:
                self.lowerLabel1.config(text='Cannot find the right folder in this directory.', foreground='red')

        # update
        def callback(*args):
            if not self.cura_dir.get():
                self.next_button1.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button1.config(state=tk.NORMAL, command=check_dir)

        # put each widget in place, reorient if was forgotten
        self.upperLabel1.grid(row=0, column=0, columnspan=3)
        self.lowerLabel1.grid(row=2, column=0, columnspan=2)
        self.lowerLabel1.config(text='')
        self.entry1.grid(row=1, sticky=tk.W, columnspan=2)
        self.next_button1.grid(row=3, column=1, columnspan=2)

        self.cura_dir.trace('w', callback)

    def window2(self):
        # remove back button if the first window was skipped
        if not self.skipped:
            self.back_button2.grid(row=3, column=0, sticky=tk.W)

        self.next_button2.grid(row=3, column=0, sticky=tk.E)
        self.upperLabel2.grid(row=0, column=0)
        self.lowerLabel2.grid(row=2, column=0)
        self.entry2.grid(row=1, column=0, sticky=tk.W)
        self.entry2.config(width=50)

        def check_dir():
            if os.path.exists('./' + self.folder_name.get()) and self.folder_name.get():
                self.run()
            else:
                self.lowerLabel2.config(text='Cannot find this directory.', foreground='red')

        self.next_button2.config(command=check_dir)


def main():
    root = tk.Tk()
    root.title("Cura Importer")
    Window(root)
    root.mainloop()


main()
