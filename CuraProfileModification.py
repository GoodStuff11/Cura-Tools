import tkinter as tk
from tkinter import ttk
import os
import pathlib


class Window(tk.Frame):
    i = 0
    VARIABLES = []

    def __init__(self, master):
        # making use of the tk.Frame object
        tk.Frame.__init__(self, master)
        master.title("Cura Profile Modifier")

        # get address of cura and the latest cura version you have
        self.cura_address = str(pathlib.Path.home()).replace('\\', '/') + '/AppData/Roaming/cura'
        versions = os.walk(self.cura_address).__next__()[1]
        for v in versions[::-1]:
            if not os.path.exists(self.cura_address + '/' + v + '/cura.cfg'):
                versions.remove(v)

        self.windows = [self.window0, self.window1, self.window2, self.window3, self.window4, self.window5]
        self.windows_skip = [1] * len(self.windows)
        self.config(padx=10, pady=10)
        self.grid(column=0, row=0)

        # define all widgets

        # window 0

        self.upperLabel0 = ttk.Label(self,
                                     text='This program will ask for information so that it\n'
                                          ' can automatically manipulate the Cura files.')
        self.next_button0 = ttk.Button(self, text='Next', command=self.next_window)

        # window 1
        self.upperLabel1 = ttk.Label(self, text='Select a Cura version to import to.')
        self.radiobuttons1 = []
        self.radiobuttons_var1 = tk.StringVar()
        self.radiobuttons_var1.set(versions[-1])
        for v in versions:
            temp = ttk.Radiobutton(self, text=v, value=v, variable=self.radiobuttons_var1)
            self.radiobuttons1.append(temp)

        self.cura_dir = self.cura_address + '/' + self.radiobuttons_var1.get()
        self.cura_profile_dir = self.cura_dir + self.profile_folder(self.cura_dir)

        self.next_button1 = ttk.Button(self, text='Next', command=self.next_window)
        if len(versions) == 1:
            self.windows_skip[1] = 0

        # window2
        self.profiles = []  # list of names of profiles
        self.profiles_check = []  # profile checkbox variables IntVar()
        self.new_profiles = []  # profile entry variables StringVar()

        self.VARIABLES += self.profiles
        self.upperLabel2 = ttk.Label(self,
                                     text='Check the profiles which you want to be modified')
        self.back_button2 = ttk.Button(self, text='Back', command=self.last_window)
        self.next_button2 = ttk.Button(self, text='Next', command=self.ignore, state=tk.DISABLED)
        self.check_box2 = []
        # window 3

        self.upperLabel3 = ttk.Label(self, text='Check in the settings you want to reset.')
        self.checkBoxLabels3 = ['Retraction distance', 'Retraction speed', 'Print temperature', 'Fan speed']
        self.checkBoxLabels32 = ['retraction_amount', 'retraction_speed', 'material_print_temperature',
                                 'cool_fan_speed']
        self.settings = [tk.IntVar() for i in self.checkBoxLabels3]
        self.VARIABLES += self.settings
        self.checkBoxes3 = [tk.Checkbutton(self, text=self.checkBoxLabels3[i], variable=self.settings[i]) for i in
                            range(len(self.checkBoxLabels3))]
        self.back_button3 = ttk.Button(self, text='Back', command=self.last_window)
        self.next_button3 = ttk.Button(self, text='Next', command=self.ignore,
                                       state=tk.DISABLED)  # command will be added with a condition

        # window4
        self.upperLabel4 = ttk.Label(self, text='Is all of this correct?')
        self.lowerLabel4 = ttk.Label(self,
                                     text='Note that the changes will be displayed in the console\n'
                                          'you may revert back using Cura as needed.')
        self.dirLabel4 = ttk.Label(self)
        self.profileLabel4 = ttk.Label(self)
        self.settingsLabel4 = ttk.Label(self)
        self.back_button4 = ttk.Button(self, text='Back', command=self.last_window)
        self.exit_button4 = ttk.Button(self, text='Modify Files', command=self.run)

        # window5
        self.upperLabel5 = ttk.Label(self)
        self.close_button5 = ttk.Button(self, text='Close', command=self.master.destroy)
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
                        for j in range(len(self.checkBoxLabels32)):
                            if self.settings[j].get() == 1:
                                for l in lines:
                                    if self.checkBoxLabels32[j] in l:
                                        # only display what has been changed
                                        if not changed:
                                            self.end_message += profiles + ':\n'
                                        self.end_message += 'CHANGED\t' + self.checkBoxLabels3[j] + ' : ' + \
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

    @staticmethod
    def profile_folder(address):
        address = address.replace('\\', '/')
        if os.path.exists(address + '/quality_changes'):
            return '/quality_changes'
        else:
            return '/quality'

    def window0(self):
        self.next_button0.grid(row=2, columnspan=3)
        self.upperLabel0.grid(row=0, column=0, columnspan=3)

    def window1(self):
        self.next_button1.grid(row=len(self.radiobuttons1) + 1, column=0, sticky=tk.E)
        self.upperLabel1.grid(row=0, column=0)
        for i in range(len(self.radiobuttons1)):
            self.radiobuttons1[i].grid(row=i + 1, column=0, sticky=tk.W)

        def callback(*arg):
            self.cura_dir = self.cura_address + '/' + self.radiobuttons_var1.get()
            self.cura_profile_dir = self.cura_dir + self.profile_folder(self.cura_dir)

            if len(self.profiles_check) != 0:
                self.check_box2 = []

                self.new_profiles = []
                self.profiles_check = []
                self.profiles = []

        self.radiobuttons_var1.trace('w', callback)

    def window2(self):
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
                self.check_box2.append(check)

        self.upperLabel2.grid(row=0, column=0)
        for i, c in enumerate(self.check_box2):
            c.grid(row=1 + i, column=0, sticky=tk.W)
        self.back_button2.grid(row=1 + len(self.profiles), column=0, sticky=tk.W)
        self.next_button2.grid(row=1 + len(self.profiles), column=0, sticky=tk.E)

        def callback(*arg):
            if all(i.get() == 0 for i in self.profiles_check):
                self.next_button2.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button2.config(state=tk.NORMAL, command=self.next_window)

        for i in self.profiles_check:
            i.trace('w', callback)

    def window3(self):
        for i, check in enumerate(self.checkBoxes3):
            check.grid(row=1 + i, sticky=tk.W)

        self.back_button3.grid(row=4 + len(self.checkBoxLabels3), column=0)
        self.next_button3.grid(row=4 + len(self.checkBoxLabels3), column=2)
        self.upperLabel3.grid(row=0, column=0, columnspan=3)

        def callback(*arg):
            if all(setting.get() == 0 for setting in self.settings):
                self.next_button3.config(state=tk.DISABLED, command=self.ignore)
            else:
                self.next_button3.config(state=tk.NORMAL, command=self.next_window)

        for setting in self.settings:
            setting.trace('w', callback)

    def window4(self):
        self.upperLabel4.grid(row=0, column=0, columnspan=2)
        self.lowerLabel4.grid(row=1, column=0, columnspan=2, rowspan=2)
        self.lowerLabel4.config(foreground='gray')

        self.dirLabel4.grid(row=3, column=0, columnspan=10, sticky=tk.W)
        self.dirLabel4.configure(text='Directory of Cura files: ' + self.cura_dir)

        self.profileLabel4.grid(row=4, columnspan=10, sticky=tk.W)
        self.profileLabel4.configure(text='Profiles: ' + ', '.join(
            [self.profiles[i] for i in range(len(self.profiles)) if self.profiles_check[i].get() == 1]))

        self.settingsLabel4.grid(row=5, columnspan=10, sticky=tk.W)
        self.settingsLabel4.configure(text='Settings: ' + ', '.join(
            [self.checkBoxLabels3[i] for i in range(len(self.settings)) if self.settings[i].get() == 1]))

        self.back_button4.grid(row=6, column=0)
        self.exit_button4.grid(row=6, column=1)

    def window5(self):
        self.upperLabel5.grid(row=1)
        if self.end_message == '':
            self.end_message = 'No profiles were modified.'
        self.upperLabel5.config(text=self.end_message)
        self.close_button5.grid(row=0)


def main():
    root = tk.Tk()
    Window(root)
    root.mainloop()


main()
