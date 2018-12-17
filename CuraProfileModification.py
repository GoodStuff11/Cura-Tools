import tkinter as tk
from tkinter import ttk
import os


class Window(tk.Frame):
    i = 0
    profiles_check = []
    VARIABLES = []

    def __init__(self, master):
        # making use of the tk.Frame object
        tk.Frame.__init__(self, master)

        self.cura_dir = tk.StringVar()
        self.VARIABLES.append(self.cura_dir)

        self.windows = [self.window1, self.window2, self.window3, self.window4, self.window5, self.window6]
        self.windows_skip = [1] * len(self.windows)
        self.config(padx=10, pady=10)
        self.grid(column=0, row=0)

        # automatically get directory of cura

        if os.path.exists('./Cura_Directory'):
            f = open('./Cura_Directory')
            self.cura_dir.set(f.readline())
            self.windows_skip[1] = 0
            self.cura_profile_dir = self.cura_dir.get() + self.profile_folder(self.cura_dir.get())
            f.close()

        # define all widgets

        # window 1

        self.upperLabel1 = ttk.Label(self,
                                     text='This program will ask for information so that it\n'
                                          ' can automatically manipulate the Cura files.')
        self.lowerLabel1 = ttk.Label(self, text='Please open Cura')
        self.next_button1 = ttk.Button(self, text='Next', command=self.next_window)

        # Window 2

        self.next_button2 = ttk.Button(self, text='Next', command=self.ignore, state=tk.DISABLED)
        self.lowerLabel2 = ttk.Label(self, text='')
        self.upperLabel2 = ttk.Label(self,
                                     text='Cura > help > show configuration folder\nCopy and paste directory')
        self.entry2 = ttk.Entry(self, textvariable=self.cura_dir)
        self.entry2.config(width=35)
        self.back_button2 = ttk.Button(self, text='Back', command=self.last_window)

        # window3
        self.profiles = []
        self.VARIABLES += self.profiles
        self.upperLabel3 = ttk.Label(self,
                                     text='Check the profiles which you want to be modified')
        self.back_button3 = ttk.Button(self, text='Back', command=self.last_window)
        self.next_button3 = ttk.Button(self, text='Next', command=self.ignore, state=tk.DISABLED)
        self.check_box3 = []
        # window 4

        self.upperLabel4 = ttk.Label(self, text='Check in the settings you want to reset.')
        self.checkBoxLabels4 = ['Retraction distance', 'Retraction speed', 'Print temperature', 'Fan speed']
        self.checkBoxLabels42 = ['retraction_amount', 'retraction_speed', 'material_print_temperature',
                                 'cool_fan_speed']
        self.settings = [tk.IntVar() for i in self.checkBoxLabels4]
        self.VARIABLES += self.settings
        self.checkBoxes4 = [tk.Checkbutton(self, text=self.checkBoxLabels4[i], variable=self.settings[i]) for i in
                            range(len(self.checkBoxLabels4))]
        self.back_button4 = ttk.Button(self, text='Back', command=self.last_window)
        self.next_button4 = ttk.Button(self, text='Next', command=self.ignore,
                                       state=tk.DISABLED)  # command will be added with a condition

        # window5
        self.upperLabel5 = ttk.Label(self, text='Is all of this correct?')
        self.lowerLabel5 = ttk.Label(self,
                                     text='Note that the changes will be displayed in the console\n'
                                          'you may revert back using Cura as needed.')
        self.dirLabel5 = ttk.Label(self)
        self.profileLabel5 = ttk.Label(self)
        self.settingsLabel5 = ttk.Label(self)
        self.back_button5 = ttk.Button(self, text='Back', command=self.last_window)
        self.exit_button5 = ttk.Button(self, text='Modify Files', command=self.run)

        # window6
        self.upperLabel6 = ttk.Label(self)
        self.close_button6 = ttk.Button(self, text='Close', command=self.master.destroy)
        self.end_message = ''

        self.update_window()

    def run(self):
        # removes .inst and .cfg and uses the _ as delimiter for different words
        directory = os.listdir(self.cura_profile_dir)

        for d in directory:
            try:
                with open(self.cura_profile_dir + '/' + d, 'r') as file:
                    lines = file.readlines()
                # match names
                for profiles in self.profiles:
                    changed = False
                    if profiles == lines[2][7:-1]:
                        for j in range(len(self.checkBoxLabels42)):
                            if self.settings[j].get() == 1:
                                for l in lines:
                                    if self.checkBoxLabels42[j] in l:
                                        # only display what has been changed
                                        if not changed:
                                            self.end_message += profiles + ':\n'
                                        self.end_message += 'CHANGED\t' + self.checkBoxLabels4[j] + ' : ' + \
                                                            l.split(' ')[-1]
                                        changed = True
                                        lines.remove(l)
                                        break  # found the line you were looking for
                    # override the file and create a new one with ORIGINAL added
                    with open(self.cura_profile_dir + '/' + d, 'w') as file:
                        for L in lines:
                            file.write(L)
            except PermissionError:
                print("Couldn't get permission to use file")

        self.next_window()

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
        self.next_button1.grid(row=2, columnspan=3)
        self.lowerLabel1.grid(row=1, column=0, columnspan=3)
        self.upperLabel1.grid(row=0, column=0, columnspan=3)

    @staticmethod
    def profile_folder(address):
        address = address.replace('\\', '/')
        if os.path.exists(address + '/quality_changes'):
            return '/quality_changes'
        else:
            return '/quality'

    def window2(self):

        def check_dir():
            self.cura_profile_dir = self.cura_dir.get() + self.profile_folder(self.cura_dir.get())
            if os.path.exists(self.cura_profile_dir):
                # create Cura_directory file if it doesn't exist
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
                self.next_button2.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button2.config(state=tk.NORMAL, command=check_dir)

        # first time
        if not self.cura_dir.get():
            self.next_button2.config(state=tk.DISABLED, command=self.ignore)
        else:
            self.next_button2.config(state=tk.NORMAL, command=check_dir)

        # put each widget in place, reorient if was forgotten
        self.upperLabel2.grid(row=0, column=0, columnspan=3)
        self.lowerLabel2.grid(row=2, column=0, columnspan=2)
        self.lowerLabel2.config(text='')
        self.entry2.grid(row=1, sticky=tk.W, columnspan=2)
        self.back_button2.grid(row=3, sticky=tk.W)
        self.next_button2.grid(row=3, column=1, columnspan=2)

        self.cura_dir.trace('w', callback)

    def window3(self):
        # PROFILES

        # get profile names
        if len(self.profiles_check) == 0:
            print(self.cura_profile_dir)
            directory = os.listdir(self.cura_profile_dir)
            for d in directory:
                with open(self.cura_profile_dir + '/' + d, 'r') as file:
                    lines = file.readlines()
                if lines[2][7:-1] not in self.profiles:
                    self.profiles.append(lines[2][7:-1])
            self.profiles_check = [tk.IntVar() for i in self.profiles]
            self.VARIABLES += self.profiles_check

            # create check boxes
            for i in range(len(self.profiles)):
                check = ttk.Checkbutton(self, variable=self.profiles_check[i], text=self.profiles[i])
                self.check_box3.append(check)

        self.upperLabel3.grid(row=0, column=0)
        for i, c in enumerate(self.check_box3):
            c.grid(row=1 + i, column=0, sticky=tk.W)
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
        for i, check in enumerate(self.checkBoxes4):
            check.grid(row=1 + i, sticky=tk.W)

        self.back_button4.grid(row=4 + len(self.checkBoxLabels4), column=0)
        self.next_button4.grid(row=4 + len(self.checkBoxLabels4), column=2)
        self.upperLabel4.grid(row=0, column=0, columnspan=3)

        def callback(*arg):
            if all(setting.get() == 0 for setting in self.settings):
                self.next_button4.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button4.config(state=tk.NORMAL, command=self.next_window)

        for setting in self.settings:
            setting.trace('w', callback)

    def window5(self):
        self.upperLabel5.grid(row=0, column=0, columnspan=2)
        self.lowerLabel5.grid(row=1, column=0, columnspan=2, rowspan=2)
        self.lowerLabel5.config(foreground='gray')

        self.dirLabel5.grid(row=3, column=0, columnspan=10, sticky=tk.W)
        self.dirLabel5.configure(text='Directory of Cura files: ' + self.cura_dir.get())

        self.profileLabel5.grid(row=4, columnspan=10, sticky=tk.W)
        self.profileLabel5.configure(text='Profiles: ' + ', '.join(
            [self.profiles[i] for i in range(len(self.profiles)) if self.profiles_check[i].get() == 1]))

        self.settingsLabel5.grid(row=5, columnspan=10, sticky=tk.W)
        self.settingsLabel5.configure(text='Settings: ' + ', '.join(
            [self.checkBoxLabels4[i] for i in range(len(self.settings)) if self.settings[i].get() == 1]))

        self.back_button5.grid(row=6, column=0)
        self.exit_button5.grid(row=6, column=1)

    def window6(self):
        self.upperLabel6.grid(row=1)
        if self.end_message == '':
            self.end_message = 'No profiles were modified.'
        self.upperLabel6.config(text=self.end_message)
        self.close_button6.grid(row=0)


def main():
    root = tk.Tk()
    root.title("Cura Profile Modifier")
    Window(root)
    root.mainloop()


main()
