from tkinter import *
import collections
import communicationInterface
import widgets

class Terminal():
    # Global variables allow access from anywhere in the program
    # not the best practice, but it made it easier than writing functions with unwieldly parameter lists

    widgets = {}
    
    labels = []
    num_remember = 100

    # A deque (double-ended queue) allows the program to display 
    # the most recent (and most relevant) output from the processor
    # When the size of the deque exceeds num_remember, it deletes the oldest entry
    de = collections.deque([], maxlen=num_remember)
    
    def __init__(self, tabs, tabIndex):
        self.widgets['Terminal Tab'] = tabs[tabIndex]

        # Enable vertical scroll bar
        self.widgets['Terminal Output Generic Frame'] = Frame(self.widgets['Terminal Tab'])
        self.widgets['Terminal Output Generic Frame'].pack(fill=BOTH, expand=YES)

        self.widgets['Canvas'] = Canvas(self.widgets['Terminal Output Generic Frame'], borderwidth=0, highlightthickness=0)
        self.widgets['Canvas'].pack(side='left', fill='both', expand=True)

        vsb = Scrollbar(self.widgets['Terminal Output Generic Frame'], orient='vertical',
                        command=self.widgets['Canvas'].yview)
        vsb.pack(side='right', fill='y')

        self.widgets['Canvas'].configure(yscrollcommand=vsb.set)
        
        # Create and display a Terminal Output Frame 
        self.widgets['Terminal Output'] = Frame(self.widgets['Canvas'])
        self.widgets['Terminal Output'].pack(fill=BOTH, expand=YES)

        self.widgets['Canvas'].create_window((4, 4), window=self.widgets['Terminal Output'], anchor='nw')
        self.widgets['Terminal Output'].bind('<Configure>', self.onFrameConfigure)

        for i in range(self.num_remember):
            lb = Label(self.widgets['Terminal Output'], width=100, anchor='w')
            self.labels.append(lb)

        # Create and display a Terminal Input Text box
        self.widgets['Terminal Input'] = Text(self.widgets['Terminal Tab'], bg='ghost white',
                                              borderwidth=1, relief=SUNKEN)
        self.widgets['Terminal Input'].pack(fill=BOTH, expand=YES)

        # Bind the <Return> key to the Terminal Input Text box
        # On <Return>, call print_to_terminal()
        self.widgets['Terminal Input'].\
            bind('<Return>', lambda e: communicationInterface.custom_write(self.widgets['Terminal Tab'],
                                                                           self.widgets['Terminal Input'],
                                                                           self.widgets['Terminal Input'].get('1.0', END)))

    def print_to_terminal(self, msg, in_out):
        if msg == None:
            return

        serial_dir = ">> "
        if in_out == 'out':
            serial_dir = "<< "
            serial_dir = serial_dir.encode()

        # msg is a binary string with each line terminated by '\r\n'
        # splitlines() is used to prevent these carriage returns and newlines
        # from appearing in the terminal, by making each line in entry
        # an item in a list; each item in the list is added to the deque, de
        for line in msg.splitlines():
            final_line = serial_dir + line
            self.de.append(final_line)

        # Display each item in de according to its position within de

        for i in range(len(self.de)):
            line = self.de[i]
            widgets.edit_message(self.labels[i], None, -1, line)
            self.labels[i].grid(row=i, column=0)
            
        self.widgets['Canvas'].yview_moveto(1)
    
    def onFrameConfigure(self, event):
        self.widgets['Canvas'].configure(scrollregion=self.widgets['Canvas'].bbox('all'))

