from tkinter import *
import winsound
import re
import binary_display
import communicationInterface
import widgets
import tempFile
import subwindow
import tooltip


class Rows():
    widget_dict = {}
    widget_name_list = ['Row Number',
                        'isActive',
                        'Register Name',
                        'Register Address',
                        'Hex Value',
                        'Binary Display',
                        'Message']

    address_sv = []
    value_sv = []

    total_rows = 0
    total_cols = 0
    headerRow = []

    msg_dict = {'er: No Value': 'Please enter a value',
                'er: Invalid hex': 'Hex digits are numbers (0-9) and lowercase or uppercase characters (a-f)/(A-F)',
                'er: Invalid value': 'Values are at most 2 digits long',
                'er: Invalid header row': 'Your CSV file should have the header row:\n'
                                           '"Register Name,Address,Value,Description"\n'
                }

    has_created_temp_file = False

    name_dict = {}
    description_dict = {}

    def __init__(self, frame, default_row_num, header_row):
        """
        1. Make a class variable so entire class can access the frame
        2. Make a copy of the header_row
        3. Initialize a widget dictionary
        4. Create a header row
        5. Create the initial rows
        :param frame:
        :param default_row_num:
        :param header_row:
        """
        self.widget_dict['Register Control Frame'] = frame

        for col in header_row:
            self.headerRow.append(col)

        # Initialize widget-dict:
        # It is a dictionary whose values are lists
        # whose index corresponds to (row number - 1)
        for widget_name in self.widget_name_list:
            self.widget_dict[widget_name] = []

        # Create header row
        self.create_headerRow(frame, header_row)

        # Create initial rows
        for i in range(default_row_num):
            create_row(frame, header_row)

    # Fill tab
    def create_headerRow(self, tab, header_row):
        """
        1. Create the Labels
        2. Create the Read/Write buttons
        :param tab:
        :param header_row:
        :return:
        """
        # Create Labels
        for col in header_row:
            i = header_row.index(col)
            if(col == 'Active'):
                Button(tab, text=header_row[i], command=lambda: toggleSelect()).grid(row=0, column=i)
                continue
            Label(tab, text=header_row[i]).grid(row=0, column=i)
        # Create read/write buttons
        self.create_read_write(tab, len(header_row))

    @staticmethod
    def create_read_write(tab, col):
        read = Button(tab, text="Read", command=lambda: enter_input('read'))
        read.grid(row=0, column=col, padx=5)
        write = Button(tab, text="Write", command=lambda: enter_input('write'))
        write.grid(row=0, column=col + 1)


def create_row(tab, header_row):
    """
    1. Differentiate between row number (starts from 1) and row index (starts from 0)
    2. Create all the widgets that comprise a row
    3. Add these widgets to the widget dictionary
    :param tab: The Register tab
    :param header_row: The header row
    """
    tr = Rows.total_rows
    tr_1 = tr + 1

    row_num_label = create_display_row_num_label(tab, tr_1, header_row)
    is_active_checkbutton = create_display_isActive_Checkbutton(tab, tr_1, header_row)
    reg_name = Label(tab, text='', width=15, wraplength=100)
    register_address_entry = create_display_register_address_entry(tab, tr_1, header_row)
    hex_entry = create_display_hex_value_entry(tab, tr_1, header_row)
    binary_display_chbt = create_display_binary_input(tab, tr_1, header_row)
    message = Label(tab, text='', width=20, wraplength=150)

    Rows.widget_dict['Row Number'].append(row_num_label)
    Rows.widget_dict['isActive'].append(is_active_checkbutton)
    Rows.widget_dict['Register Name'].append(reg_name)
    Rows.widget_dict['Register Address'].append(register_address_entry)
    Rows.widget_dict['Hex Value'].append(hex_entry)
    Rows.widget_dict['Binary Display'].append(binary_display_chbt)
    Rows.widget_dict['Message'].append(message)

    Rows.total_rows += 1


def create0x(tab):
    hex_syntax = '0x'
    hex_syntax_label = Label(tab, text=hex_syntax)
    return hex_syntax_label


def create_display_isActive_Checkbutton(tab, row_num, header_row):
    """
    1. Create variable that save state of Checkbutton
    2. Create and display Checkbutton
    :param tab: The Register tab
    :param row_num: The row number (because of the header_row, the row_num matches where the row will be displayed
    :param header_row: The header row
    :return: The variable that saves the state
    """
    var = IntVar(value=1)
    chbt = Checkbutton(tab, variable=var)
    chbt.grid(row=row_num, column=header_row.index('Active'))
    return var


def is_completely_filled():
    """
    :return: True, if all the isActive checkbuttons are selected
            False, otherwise
    """
    isCompletelyfilled = True
    for i in range(Rows.total_rows):
        if Rows.widget_dict['isActive'][i].get() == 0:
            isCompletelyfilled = False
            break
    return isCompletelyfilled


def selectAll():
    for i in range(Rows.total_rows):
        Rows.widget_dict['isActive'][i].set(1)


def selectOne(row_num):
    Rows.widget_dict['isActive'][row_num-1].set(1)


def deselectAll():
    for i in range(Rows.total_rows):
        Rows.widget_dict['isActive'][i].set(0)


def toggleSelect():
    if is_completely_filled():
        deselectAll()
    else:
        selectAll()


# Display Register Index
def create_display_row_num_label(tab, row_num, header_row):
    """
    1. Adjust the size of the label based on the number of digits
    2. Create and display a Label
    3. Future functionality?
    :param tab: The Register tab
    :param row_num: The row number (because of the header_row, the row_num matches where the row will be displayed
    :param header_row: The header row
    :return: the row_num_label widget
    """
    # Normally, the space for index number should be 1
    w = 1

    # If the index number exceeds 9, it should be big enough for 2 digits
    if row_num > 9:
        w = 2

    # Create and display a Label
    row_num_label = Label(tab, text=row_num, width=w)
    row_num_label.grid(row=row_num, column=header_row.index(" "))

    return row_num_label


def create_display_register_address_entry(tab, row_num, header_row):
    """
    1. Create and display an Entry
    2. If this is the first Register Address Entry, place the cursor in the box
    :param tab: The Register tab
    :param row_num: The row number (because of the header_row, the row_num matches where the row will be displayed
    :param header_row: The header row
    :return: The entry widget
    """
    # Create and display a Name Frame
    name_frame = Frame(tab)
    name_frame.grid(row=row_num, column=header_row.index('Address'))

    # Create and display the "0x" before the entry
    hex_syntax = create0x(name_frame)
    hex_syntax.grid(row=0, column=0)

    # When the address is changed, it infers that the user would like to read/write from it
    # (so the program makes that row Active)
    Rows.address_sv.append(StringVar())
    Rows.address_sv[row_num-1].trace_add('write', lambda name, index, mode : selectOne(row_num))

    # Create and display an Entry
    r_entry = Entry(name_frame, width=10, text=Rows.address_sv[row_num-1])
    r_entry.grid(row=0, column=1, padx=5)

    r_entry.bind('<Return>', lambda e: update_name_description(row_num-1))

    # If this is the first Register Address Entry,
    # place the cursor in the box
    if row_num == 1:
        r_entry.focus_set()

    return r_entry


def create_display_hex_value_entry(tab, row_num, header_row):
    """
    1. Create and display an Entry
    :param tab: The Register tab
    :param row_num: The row number (because of the header_row, the row_num matches where the row will be displayed
    :param header_row: The header row
    :return: Hex Value entry
    """
    # Create and display a Hex Value Frame
    hex_val_frame = Frame(tab)
    hex_val_frame.grid(row=row_num, column=header_row.index("Value"))

    # Create and display '0x' before the entry
    hex_syntax = create0x(hex_val_frame)
    hex_syntax.grid(row=0, column=0)

    # When the address is changed, it infers that the user would like to read/write from it
    # (so the program makes that row Active)
    # When the value is changed, also change the binary display to reflect it.
    Rows.value_sv.append(StringVar())

    # Create and display an Entry
    hex_val_entry = Entry(hex_val_frame, width=5, text=Rows.value_sv[row_num-1])
    hex_val_entry.grid(row=0, column=1, padx=5)

    Rows.value_sv[row_num - 1].trace_add('write',
                                         lambda name, index, mode: change_register_value(row_num, hex_val_entry))

    return hex_val_entry


def change_register_value(row_num, hex_val_entry):
    row_index = row_num - 1
    hex_val = hex_val_entry.get()

    if Rows.widget_dict['Message'][row_index].cget('text') == Rows.msg_dict['er: Invalid value']:
        # Clear the previous message
        widgets.edit_message(Rows.widget_dict['Message'][row_index], None, -1, '')
        Rows.widget_dict['Message'][row_index].grid(row=row_num, column=Rows.headerRow.index('Message'))

    # Make the row active
    selectOne(row_num)
    try:
        # Change the binary display to reflect the updated value
        if not hex_val:
            Rows.chbxs.display_hex_to_binary(row_index, '0')
        else:
            Rows.chbxs.display_hex_to_binary(row_index, hex_val)
    except IndexError:
        # Warn the user when the value exceeds 2 digits
        widgets.edit_message(Rows.widget_dict['Message'][row_index], Rows.msg_dict, 'er: Invalid value')
        Rows.widget_dict['Message'][row_index].grid(row=row_num, column=Rows.headerRow.index('Message'))


def create_display_binary_input(tab, row_num, header_row):
    """
    1. Create and display a frame
    2. Create a row of CheckBoxes and place them within the frame
    :param tab: The Register tab
    :param row_num: The row number (because of the header_row, the row_num matches where the row will be displayed
    :param header_row: The header row
    :return: The checkbox widgets
    """
    # Create and display a frame
    bin_frame = Frame(tab)
    bin_frame.grid(row=row_num,
                   column=header_row.index("Binary Display\n7      6       5       4             3       2       1       0"))


    # Create a row of CheckBoxes
    Rows.chbxs = binary_display.CheckBoxes(bin_frame, row_num-1)
    return Rows.chbxs


def beep(f1, f2):
    """
    Create a two-toned beep
    :param f1: The frequency (pitch) of the first tone
    :param f2: The frequency (pitch) of the second tone
    """
    # Set Duration
    d1 = 110
    d2 = 120
    winsound.Beep(f1, d1)
    winsound.Beep(f2, d2)

def enter_input(action):
    """
    1. Get the Register Address and Hex Value of the row
        a. If isActive is false, clear the message
        b. If there is no register address, clear the value and message
        c. If the inputted hex digits aren't valid, create an error message to notify the user
        d. If the user chose 'Write' and didn't input a hex value, create an error message to notify them
        e. else write read/write command to the processor and create a message of the outputted value
    2. Write these addresses and values to the processor
    3. Save all rows in a temporary file
    :param action: Read/Write
    """
    ret = None
    has_prompted_for_comms = False;
    has_prompted_for_camera = False
    for i in range(Rows.total_rows):
        # if the user selects not isActive, clear the remaining message and continue
        if Rows.widget_dict['isActive'][i].get() == 0:
            widgets.edit_message(Rows.widget_dict['Message'][i], Rows.msg_dict, -1, '')
            continue

        # Get the inputted register address
        register_address = Rows.widget_dict['Register Address'][i].get()

        # Get the inputted hex value
        hex_val = Rows.widget_dict['Hex Value'][i].get()

        # If there is no inputted register address, clear anything in the value entry
        if register_address == '':
            Rows.widget_dict['Hex Value'][i].delete(0, END)
            Rows.widget_dict['Binary Display'][i].display_hex_to_binary(i, '0')
            widgets.edit_message(Rows.widget_dict['Message'][i], Rows.msg_dict, -1, '')

        # If the inputted hex digits aren't valid,
        # create an error message to notify the user

        # If the user chose 'Write' and didn't input a hex value,
        # create an error message to notify them

        # else write read/write command to the processor
        # and create a message of the outputted value
        elif action == 'write' and hex_val == '' and register_address != '':
            widgets.edit_message(Rows.widget_dict['Message'][i], Rows.msg_dict, 'er: No Value')
        elif not is_valid_hex(register_address) and not is_valid_hex(hex_val):
            widgets.edit_message(Rows.widget_dict['Message'][i], Rows.msg_dict, 'er: Invalid hex')
        else:
            ret = communicationInterface.to_from_register(Rows.widget_dict['Register Control Frame'], action, register_address,
                                                          hex_val, has_prompted_for_comms, has_prompted_for_camera)
            has_prompted_for_comms = True
            has_prompted_for_camera = True

            # If the user inputted a valid address and hit 'Read', display the updated value in the Hex Value box
            if ret != None and action == 'read':
                updated_hex_val = str(ret)[-3:-1]
                Rows.widget_dict['Hex Value'][i].delete(0, END)
                Rows.widget_dict['Hex Value'][i].insert(0, updated_hex_val)
            # elif ret != None and action == 'write':
            #     updated_hex_val = Rows.widget_dict['Hex Value'][i].get()
            #     Rows.widget_dict['Binary Display'][i].display_hex_to_binary(i, updated_hex_val)

            update_name_description(i)
            widgets.edit_message(Rows.widget_dict['Message'][i], Rows.msg_dict, -1, ret)

        # Display the message
        Rows.widget_dict['Message'][i].grid(row=i + 1, column=Rows.headerRow.index('Message'))

    if action == 'read':
        beep(466, 587)
    elif action == 'write':
        beep(587, 466)

    # Save progress into a temporary file
    if ret != None and not Rows.has_created_temp_file:
        Rows.tp = tempFile.Temp(Rows.widget_dict['Register Control Frame'])
        Rows.has_created_temp_file = True
    try:
        Rows.tp.save_to_temp(extract_row_value())
    except AttributeError:
        return


def is_valid_hex(hex_input):
    """
    Determine if the user inputted a valid hex_value
    :param hex_input: The hex_value that the user inputs
    :return:
        1. True if the hex_input is a valid hex number
        2. else, false
    """
    try:
        int(hex_input, 16)
    except ValueError:
        return False
    return True


def insert_row_value(csv_file):
    """
    Takes in a list of lists with values: ['register val','val'] or ['register val'] and inserts these values
    into the register GUI display
    :param csv_file:
    :return:
    """

    # Create regular expressions for the addresses and values (program expects hex values)
    reg_ad_regex = re.compile(r'(0x)?([0-9a-f]{1,4})', re.IGNORECASE)
    value_regex = re.compile(r'(0x)?([0-9a-f]{1,2})', re.IGNORECASE)

    # Create regular expressions for Header labels
    header_name_regex = re.compile(r'Register Name', re.IGNORECASE)
    header_ad_regex = re.compile(r'Address', re.IGNORECASE)
    header_value_regex = re.compile(r'Value', re.IGNORECASE)
    header_descript_regex = re.compile(r'Description', re.IGNORECASE)

    # Create an array of of header regexes;
    header_arr = [header_name_regex, header_ad_regex, header_value_regex, header_descript_regex]

    # Try to find the header along the top of the file; else the file is invalid
    try:
        header_name = header_name_regex.search(csv_file[0][header_arr.index(header_name_regex)])
        header_ad = header_ad_regex.search(csv_file[0][header_arr.index(header_ad_regex)])
        header_value = header_value_regex.search(csv_file[0][header_arr.index(header_value_regex)])
        header_descript = header_descript_regex.search(csv_file[0][header_arr.index(header_descript_regex)])
    except IndexError:
        invalid_csv_file()
        return

    for i in range(len(csv_file)):
        try:
            # Delete all values in the 'Register Address' and 'Hex Value' columns
            # Delete all messages from processor
            Rows.widget_dict['Register Address'][i].delete(0, END)
            Rows.widget_dict['Hex Value'][i].delete(0, END)
            Rows.widget_dict['Binary Display'][i].display_hex_to_binary(i, '0')
            widgets.edit_message(Rows.widget_dict['Message'][i], Rows.msg_dict, -1, '')
        except IndexError:
            # If additional rows need to be created, create them
            create_row(Rows.widget_dict['Register Control Frame'], Rows.headerRow)

        # Because of the header row, account for the difference in row index
        reg_index = i
        if header_name and header_ad and header_value and header_descript:
            reg_index = i - 1
            if i == 0:
                continue

        # Get the inputted register name (if there is one)
        inputted_register_name = csv_file[i][header_arr.index(header_name_regex)]
        Rows.widget_dict['Register Name'][reg_index].config(text=inputted_register_name, justify=LEFT, padx=5)
        Rows.widget_dict['Register Name'][reg_index].grid(row=i, column=Rows.headerRow.index('Name'))

        try:
            # Get the register address in the csv file
            register_address = reg_ad_regex.search(csv_file[i][header_arr.index(header_ad_regex)])
            # Insert that register address into the GUI row
            Rows.widget_dict['Register Address'][reg_index].insert(0, register_address.group(2))
        except AttributeError:
            widgets.edit_message(Rows.widget_dict['Message'][reg_index], Rows.msg_dict, 'er: Invalid hex')
            Rows.widget_dict['Message'][reg_index].grid(row=i, column=Rows.headerRow.index('Message'))
            continue

        add_name(register_address.group(2), inputted_register_name)

        # Values are optional
        # If there is a value, insert it into the GUI row
        if csv_file[i][header_arr.index(header_value_regex)]:
            try:
                value = value_regex.search(csv_file[i][header_arr.index(header_value_regex)])
                try:
                    Rows.widget_dict['Binary Display'][reg_index].display_hex_to_binary(reg_index, value.group(2))
                except AttributeError:
                    pass
                try:
                    Rows.widget_dict['Hex Value'][reg_index].insert(0, value.group(2))
                except AttributeError:
                    widgets.edit_message(Rows.widget_dict['Message'][reg_index], Rows.msg_dict, 'er: Invalid hex')
                    Rows.widget_dict['Message'][reg_index].grid(row=i, column=Rows.headerRow.index('Message'))
            except IndexError:
                pass

        # Descriptions are optional
        # register_descript = csv_file[i][header_arr.index(header_descript_regex)]
        # add_description(register_address.group(2), register_descript)
        # tooltip.Tooltip(Rows.widget_dict['Register Name'][reg_index], register_descript)
        try:
            register_descript = csv_file[i][header_arr.index(header_descript_regex)]
            add_description(register_address.group(2), register_descript)
            if register_descript:
                tooltip.Tooltip(Rows.widget_dict['Register Name'][reg_index], register_descript)
        except IndexError:
            pass


def add_name(address, name):
    Rows.name_dict[address] = name


def add_description(address, descript):
    Rows.description_dict[address] = descript


def update_name_description(row_index):
    ad = str.lower(str(Rows.widget_dict['Register Address'][row_index].get()))

    try:
        matching_name = Rows.name_dict[ad]
        matching_descript = Rows.description_dict[ad]
    except KeyError:
        return

    # Delete previous name
    Rows.widget_dict['Register Name'][row_index].config(text='')
    Rows.widget_dict['Register Name'][row_index].grid(row=row_index+1, column=Rows.headerRow.index('Name'))

    # Fill in with new name
    Rows.widget_dict['Register Name'][row_index].config(text=matching_name, justify=LEFT, padx=5)
    Rows.widget_dict['Register Name'][row_index].grid(row=row_index+1, column=Rows.headerRow.index('Name'))

    if matching_descript:
        tooltip.Tooltip(Rows.widget_dict['Register Name'][row_index], matching_descript)


def extract_row_value():
    """
    Extract all rows in the register tab into lists
    :return: A list of rows (which are lists of fields)
    """
    extract = [['Register Name', 'Address', 'Value', 'Description']]
    for i in range(Rows.total_rows):
        row = []
        name = Rows.widget_dict['Register Name'][i].cget('text')
        register_address = Rows.widget_dict['Register Address'][i].get()
        hex_val = Rows.widget_dict['Hex Value'][i].get()

        if register_address == '':
            continue
        row.append(name)
        row.append('0x' + register_address)
        row.append('0x' + hex_val)
        try:
            row.append(Rows.description_dict[register_address])
        except KeyError:
            pass

        extract.append(row)
    return extract


def invalid_csv_file():
    error = subwindow.draw_subwindow(Rows.widget_dict['Register Control Frame'], 300, 120, 'Please Include Header Row')
    spacer_frame = Frame(error, borderwidth=20)
    spacer_frame.pack()
    Label(spacer_frame, text=Rows.msg_dict['er: Invalid header row']).pack()
    ok = Button(spacer_frame, text='OK', width=7, command=lambda: error.destroy())
    ok.pack()
    error.grab_set()