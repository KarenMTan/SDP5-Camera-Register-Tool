from tkinter import *
import rows


class Registers():
    default_row_num = 5
    headerRow = [" ", 'Active', 'Name', "Address", "Value",
                "Binary Display\n7      6       5       4             3       2       1       0", "Message"]

    widget_dict = {}

    def __init__(self, tabs, tab_index):
        """
        1. Create a canvas and vertical scroll bar to allow vertical scrolling
        2. Create the body of the Register Control tab
        :param tabs: A list of Frame widgets
        :param tab_index: The index of the register tab
        """
        reg_tab = tabs[tab_index]

        # Create a canvas to allow vertical scrolling
        canvas = Canvas(reg_tab, borderwidth=0, highlightthickness=0)
        canvas.pack(side='left', fill='both', expand=True)

        vsb = Scrollbar(reg_tab, orient='vertical', command=canvas.yview)
        vsb.pack(side='right', fill='y')

        canvas.configure(yscrollcommand=vsb.set)
        canvas.bind_all('<MouseWheel>', lambda e: onMouseWheel(e, canvas))

        self.widget_dict['Register Control Frame'] = Frame(canvas)
        canvas.create_window((4, 4), window=self.widget_dict['Register Control Frame'], anchor='nw')
        self.widget_dict['Register Control Frame'].bind('<Configure>',
                                                        lambda event, canvas=canvas: onFrameConfigure(canvas))

        # Initialize rows
        row = rows.Rows(self.widget_dict['Register Control Frame'], self.default_row_num, self.headerRow)


def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox('all'))


def onMouseWheel(e, canvas):
    """
    Allow scrolling with the mouse
    """
    canvas.yview_scroll(-1 * (int(e.delta / 120)), 'units')


def add_row():
    """
    Add a single row
    """
    rows.create_row(Registers.widget_dict['Register Control Frame'], Registers.headerRow)


def insert_row_value(csv_file):
    """
    Insert all row values from csv file into the register tab
    :param csv_file: The csv file
    """
    rows.insert_row_value(csv_file)


def extract_row_value():
    """
    Extract all row valuesl from register tab
    :return: A list of rows (which are lists of fields)
    """
    return rows.extract_row_value()
