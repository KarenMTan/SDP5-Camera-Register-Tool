from tkinter import *
import subwindow
import widgets
import menu


class Login():
    widgets = {}
    msg_dict = {'er: Incorrect Password': 'Incorrect Password'}
    password = ['enG']

    # Width (w) and Height (h) of login window
    title = 'Login'
    w = 300
    h = 125

    def __init__(self, root):
        """
            1. Hide the root window
            2. Draw the login window
            3. Close the entire application when login window is closed
            4. Lock the rest of the program until the correct password is given
            5. Add widgets to the login window
            :param root: The root window
        """
        root.withdraw()

        self.widgets['Login Window'] = subwindow.draw_subwindow(root, self.w, self.h, self.title)

        self.widgets['Login Window'].protocol('WM_DELETE_WINDOW', lambda: subwindow.on_exit(root))

        self.widgets['Login Window'].grab_set()

        self.create_widgets(root)

    def create_widgets(self, root):
        """
        1. Create and display a Frame for the widgets
        2. Create and display a password prompt Label
        3. Create and display an input Frame
        4. Create and display a password Entry
        5. Create and display an enter Button
        6. Bind <Return> key to enter Button
        7. Create a message Label
        :param root: The Login window
        """

        self.widgets['Main Frame'] = Frame(self.widgets['Login Window'], borderwidth=20)
        self.widgets['Main Frame'].pack(expand=YES, fill=BOTH)

        Label(self.widgets['Main Frame'], text='Enter password:').pack(side=TOP, expand=YES)

        self.widgets['Input Frame'] = Frame(self.widgets['Main Frame'])
        self.widgets['Input Frame'].pack(side=TOP, expand=YES, fill=BOTH)

        self.widgets['Password Entry'] = Entry(self.widgets['Input Frame'], show="*")
        self.widgets['Password Entry'].focus_set()  # place cursor in entry
        self.widgets['Password Entry'].pack(side=LEFT, expand=YES)

        self.widgets['Enter Button'] = Button(self.widgets['Input Frame'], text="Enter",
                                              command=lambda: self.verify_password_input(root))
        self.widgets['Enter Button'].pack(side=RIGHT, expand=YES)

        self.widgets['Login Window'].bind("<Return>", lambda e: self.widgets['Enter Button'].invoke())

        self.widgets['Message'] = Label(self.widgets['Main Frame'], width=50, wraplength=300)

    def verify_password_input(self, root):
        """
        1. Get the user input from the Password Entry
        2. If user input matches password:
            a. Close Login window and open main application
            b. Ask user for Workspace location
        3. Else:
           a. Display "Incorrect Password"
            b. Clear the Password entry box
        :param root: The Login window
        """

        ui = self.widgets['Password Entry'].get()

        if ui == self.password[0]:
            self.widgets['Login Window'].destroy()
            root.deiconify()
            menu.define_workspace(root)
        else:
            widgets.edit_message(self.widgets['Message'], self.msg_dict, 'er: Incorrect Password')
            self.widgets['Message'].pack(side=TOP, fill=X)
            self.widgets['Password Entry'].delete(0, END)
