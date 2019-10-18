from tkinter import *
import tkinter.filedialog as fd
import os
import csv
import registers
import subwindow
import tempFile
import webbrowser


class Menubar():
    widgets = {}

    workspace = None

    url = "https://wiki.corp.knorr-bremse.com/x/3_WpCg"

    info = "Author: Karen Tan\n\n" \
           "Published: September 6th, 2019\n\n" \
           "Thank you Bendix CVS's Irvine office for giving me\nthe opportunity to learn so much this summer!\n"

    template_header = ['Register Name', 'Address', 'Value', 'Description']

    def __init__(self, master):
        """
        1. Create a menu bar
        2. Create File drop down
        3. Create Edit drop down
        4. Create Help drop down
        5. Add drop downs to menu bar
        6. Display menu bar
        :param master: The root window
        """

        self.widgets['Menu Bar'] = Menu(master)

        self.widgets['File Drop Down'] = Menu(self.widgets['Menu Bar'], tearoff=0)
        self.widgets['File Drop Down'].add_command(label="Open...", command=lambda: self.op(master))
        self.widgets['File Drop Down'].add_command(label="Save As...", command=lambda: self.save_as(master))
        self.widgets['File Drop Down'].add_command(label="Select/Change Workspace",
                                                   command=lambda: define_workspace(master, self.workspace))
        self.widgets['File Drop Down'].add_command(label="Select Temporary File Location",
                                                   command=lambda: tempFile.define_temp_file_location(master))
        self.widgets['File Drop Down'].add_command(label="Create CSV Template",
                                                   command=lambda: self.template_csv(master))

        self.widgets['Edit Drop Down'] = Menu(self.widgets['Menu Bar'], tearoff=0)
        self.widgets['Edit Drop Down'].add_command(label="Add Row", command=registers.add_row)

        self.widgets['Help Drop Down'] = Menu(self.widgets['Menu Bar'], tearoff=0)
        self.widgets['Help Drop Down'].add_command(label="Open in browser...",
                                                   command=lambda aurl=self.url: self.OpenUrl(aurl))

        self.widgets['Info Drop Down'] = Menu(self.widgets['Menu Bar'], tearoff=0)
        self.widgets['Info Drop Down'].add_command(label="Details...", command=lambda: self.info_box(master))

        self.widgets['Menu Bar'].add_cascade(label="File", menu=self.widgets['File Drop Down'])
        self.widgets['Menu Bar'].add_cascade(label="Edit", menu=self.widgets['Edit Drop Down'])
        self.widgets['Menu Bar'].add_cascade(label="Help", menu=self.widgets['Help Drop Down'])
        self.widgets['Menu Bar'].add_cascade(label="Info", menu=self.widgets['Info Drop Down'])

        master.config(menu=self.widgets['Menu Bar'])

    # Open csv file with registers and values; display contents in register tab
    def op(self, root):
        """
        1. Open the workspace folder
        2. Ask user to select a file to open
        :param root: The root window
        """
        temp_file = fd.askopenfilename(parent=root, initialdir=self.workspace, title='Open',
                                       filetypes=[('CSV Files', '*.csv')])
        try:
            file = open(temp_file)
        except FileNotFoundError:
            pass
        try: 
            reader = csv.reader(file)
        except UnboundLocalError:
            return
        data = list(reader)
        registers.insert_row_value(data)
        file.close()

    # Save register tab in csv file
    def save_as(self, root):
        """
        1. Open workspace
        2. Ask user where to save file
        3. Write all rows in Register Tab to file
        4. Close file
        :param root: The root window
        """
        tempfile = fd.asksaveasfilename(parent=root, initialdir=self.workspace, title='Save As',
                                        filetypes=[('CSV Files', '*.csv')], defaultextension='*.csv')
        try: 
            file = open(tempfile, 'w', newline='')
        except FileNotFoundError:
            pass
        try: 
            writer = csv.writer(file)
        except UnboundLocalError:
            return

        register_file = registers.extract_row_value()
        for row in register_file:
            writer.writerow(row)
        file.close()

    def template_csv(self, root):
        template_location = fd.asksaveasfilename(parent=root, initialdir=self.workspace, title='Save As',
                                        filetypes=[('CSV Files', '*.csv')], defaultextension='*.csv')
        try:
            file = open(template_location, 'w', newline='')
        except FileNotFoundError:
            pass

        try:
            writer = csv.writer(file)
        except UnboundLocalError:
            return

        writer.writerow(self.template_header)
        file.close()

    def OpenUrl(self, url):
        webbrowser.open_new(url)

    # Create an info popup
    def info_box(self, root):
        """
        1. Draw the help_box subwindow
        2. Create and display the main frame
        3. Create and display information
        4. Create and display a Close button that destroys the subwindow
        :param root: The root window
        """
        info_window = subwindow.draw_subwindow(root, 350, 200, "Information")

        main_frame = Frame(info_window, borderwidth=30)
        main_frame.pack()

        Label(main_frame, text=self.info, width=45, wraplength=320, anchor=W, justify=LEFT).pack()

        Button(main_frame, text='Close', command=lambda: info_window.destroy()).pack()


def define_workspace(root, current_dir=None):
    """
    1. If there is no selected workspace:
        a. Ask user to select a workspace
    2. Ask user for workspace
    :param root:
    :param current_dir:
    :return:
    """
    if current_dir == None:
        current_dir = os.getcwd()
    Menu.workspace = fd.askdirectory(parent=root, initialdir=current_dir, title='Define Workspace:')
    

