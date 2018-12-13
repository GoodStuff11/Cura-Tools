import tkinter as tk
from tkinter import ttk
import os
import shutil


class Window(tk.Frame):
    s = ''
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

        if os.path.isfile('./Cura_Directory'):
            f = open('./Cura_Directory')
            self.cura_dir.set(f.readline())
            f.close()
            self.i += 1

        # get directory of Cura
        if os.path.exists('./Cura_Directory'):
            file = open('./Cura_Directory', 'r')
            self.s = file.readline()
            file.close()

        # Window 1
        self.next_button1 = ttk.Button(self, text='Next')
        self.lowerLabel1 = ttk.Label(self, text='')
        self.upperLabel1 = ttk.Label(self,
                                     text='Cura > help > show configuration folder\nCopy and paste directory')
        self.entry1 = ttk.Entry(self, textvariable=self.cura_dir)
        self.entry1.config(width=35)

        # Window 2
        self.upperLabel2 = ttk.Label(self,
                                     text='Please put the previously exported folder into the folder with the executable.\n'
                                          'Please input the name of the folder you would like to import.')
        if self.i == 0:
            self.skipped = True
        self.folder_name = tk.StringVar()
        self.entry2 = ttk.Entry(self, textvariable=self.folder_name)
        self.next_button2 = ttk.Button(self, text='Import')
        self.back_button2 = ttk.Button(self, text='Back')
        self.lowerLabel2 = ttk.Label(self, text='')

        self.update_window()

    def run(self):

        try:
            directory_information = []
            directory = os.listdir('./' + self.folder_name.get() + '/profiles')
            for file_name in directory:
                n = 0
                if os.path.exists(self.s + self.profile_folder(self.s) + '/' + file_name):
                    while os.path.exists(
                            self.s + self.profile_folder(self.s) + '/' + file_name[:-9] + '_' + str(n) + '.inst.cfg'):
                        n += 1
                    new_file_name = file_name[:-9] + '_' + str(n) + '.inst.cfg'

                with open('./' + self.folder_name.get() + '/profiles/' + d, 'r') as f:
                    lines = f.readlines()
                    name = lines[2][7:-1]

                # check if any files have the same name
                dup_count = 1
                duplicates = True
                while duplicates:
                    duplicates = False
                    for di in os.listdir(self.s + self.profile_folder(self.s) + '/'):
                        f = open(self.s + self.profile_folder(self.s) + '/' + di, 'r')
                        L = f.readlines()
                        if L[2][7:-1] == name and dup_count == 1 or L[2][7:-1] == name + ' #' + str(dup_count) and dup_count != 1:
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
                            self.s + self.profile_folder(self.s) + '/' + d[1])
                lines[2] = lines[2][:-1] + ' #' + str(d[2]) + '\n'
                with open(self.s + self.profile_folder(self.s) + '/' + d[1], 'w') as file:
                    for L in lines:
                        file.write(L)
        except:
            pass

        try:
            directory = os.listdir('./' + self.folder_name.get() + '/materials')
            for file_name in directory:
                dup_count = 0
                if os.path.exists(self.s + '/materials/' + file_name):
                    while os.path.exists(self.s + '/materials/' + file_name[:-17] + str(dup_count) + '.xml.fdm_material'):
                        dup_count += 1
                    os.rename('./' + self.folder_name.get() + '/materials/' + file_name, './' + self.folder_name.get() + '/materials/' +
                              file_name[:-17] + str(dup_count) + '.xml.fdm_material')
                    file_name = file_name[:-17] + str(dup_count) + '.xml.fdm_material'
                shutil.copy('./' + self.folder_name.get() + '/materials/' + file_name, self.s + '/materials')
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
        self.update_window()

    def last_window(self):
        self.i -= 1
        self.update_window()

    def ignore(self):
        pass

    def update_window(self):
        self.clear(self)
        self.windows[self.i]()

    @staticmethod
    def profile_folder(address):
        version = address.split('/')[-1]
        if float('.'.join(version.split('.')[0:2])) >= 3.4:
            return '/quality_changes'
        else:
            return '/quality'

    def window1(self):
        def check_dir():
            self.s = self.cura_dir.get().replace('\\', '/')
            s = self.s + self.profile_folder(self.s)
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
            if not self.cura_dir.get():
                self.next_button1.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button1.config(state=tk.NORMAL, command=check_dir)

        # first time
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
        if self.skipped:
            self.back_button2.grid(row=3, column=0, sticky=tk.W)
        self.next_button2.grid(row=3, column=0, sticky=tk.E)
        self.upperLabel2.grid(row=0, column=0)
        self.lowerLabel2.grid(row=2, column=0)
        self.entry2.grid(row=1, column=0, sticky=tk.W)
        self.entry2.config(width=50)

        def check_dir():
            if os.path.exists('./' + self.folder_name.get()):
                self.run()
            else:
                self.lowerLabel2.config(text='Cannot find this directory.', foreground='red')

        def callback(*arg):
            if not self.folder_name.get():
                self.next_button2.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button2.config(state=tk.NORMAL, command=check_dir)

        self.folder_name.trace('w', callback)


def main():
    root = tk.Tk()
    root.title("Cura Exporter")
    Window(root)
    root.mainloop()


main()
