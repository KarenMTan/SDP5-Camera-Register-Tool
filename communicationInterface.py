from tkinter import *
import serial
import time
import widgets
import subwindow


class CommunicationInterface():
    # Tab Names
    tab_Names = []

    # Widgets Dictionary
    widgets = {}

    # Driver Options
    driver_options = ['Serial']

    # Serial dropdown
    serial_options = ['COM Port', 'Baud Rate']
    serial_option_settings = [['AutoSense', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8'],
                                                                                                [38400, 57600, 115200]]
    serial_selected = {}

    # Message dictionary
    msg_dict = {'note: AutoSense': 'If you have multiple ports connected to your computer, AutoSense may be inaccurate. '
                                 'Please refer to your Device Manager to select the correct COM Port.',
                'er: Baud Rate': 'Invalid Baud Rate',
                'er: COM Port': 'Invalid COM Port',
                'er: Port not open': 'Please ensure COM Port is correct or USB cable is connected to computer',
                'er: No power': 'Please ensure that device is powered or restart the processor. '
                                'Also ensure that the connection is connected to the processor.',
                'er: Communication interface not selected': 'Please select a communication interface.',
                'er: Invalid camera': 'Please select a camera.'}

    ser = serial.Serial()
    camName = str()

    cmd_dict = {'read': 'ovrd ',
                'write': 'ovwr ',
                'no response': ''}

    def __init__(self, nb, tabs, tab_names, ter):
        """
        1. Assign frequently referenced widgets into the widget dictionary
        2. Create, display, and label Driver Option Frames
        3. Place Serial drop down Menus into the Serial Frame
        4. Place USB options in the USB Frame
        5. Create and display Driver Selection Radio Buttons
        6. Create Apply Button
        7. Create message Label
        :param nb: The Notebook widget
        :param tabs: List of tab widgets
        :param tab_names: List of tab names
        :param ter: The terminal tab
        """
        self.widgets['Notebook'] = nb

        for tab_name in tab_names:
            self.tab_Names.append(tab_name)

        self.widgets['Terminal'] = ter

        self.widgets['Communication Interface Configuration Tab'] = \
            tabs[tab_names.index('Communication Interface Configuration')]

        self.widgets['Spacer Frame'] = Frame(self.widgets['Communication Interface Configuration Tab'], borderwidth=20)
        self.widgets['Spacer Frame'].pack(expand=YES, fill=BOTH)

        self.widgets['Communication Interface Option Frames'] = {}

        for option in self.driver_options:
            i = self.driver_options.index(option)
            self.widgets['Communication Interface Option Frames'][option] = \
                widgets.create_display_label_ridged_frames(frame=self.widgets['Spacer Frame'],
                                                           row_index=0, column_index=i,
                                                           column_span=1,
                                                           option_name=self.driver_options[i],
                                                           label_span=1)

        for selection in self.serial_options:
            i = self.serial_options.index(selection)
            self.serial_selected[selection] = \
                widgets.create_dropdown(frame=self.widgets['Communication Interface Option Frames']['Serial'],
                                        option_name=self.serial_options[i],
                                        option_choices=self.serial_option_settings[i],
                                        command=self.select_option)

        self.widgets['Apply Button'] = Button(self.widgets['Spacer Frame'],
                                              text='Apply',
                                              command=lambda: self.serial_driver())
        self.widgets['Apply Button'].grid(row=3, column=0, columnspan=len(self.driver_options))

        self.widgets['Message'] = Label(self.widgets['Spacer Frame'], width=50, wraplength=300)

    def select_option(self, event):
        """
        When the dropdown menu is selected, the previous message should disappear to make it clear that the displayed
        message is intended for the selected option.
        """
        self.reset_message()
        self.ifAutoSense()

    def reset_message(self):
        """
        Clear the message board
        """
        widgets.edit_message(self.widgets['Message'], None, -1, '')
        display_message()

    def ifAutoSense(self):
        """
        If AutoSense is selected, give the user a note about AutoSense.
        """
        if self.serial_selected['COM Port'].get() == 'AutoSense':
            widgets.edit_message(self.widgets['Message'], self.msg_dict, 'note: AutoSense')
            display_message()

    def serial_driver(self):
        """
        1. Notify the user if the COM Port has not been selected; If this is the case, then return
        2. Notify the user if the Baud Rate has not been selected; If this is the case, then return
        3. If AutoSense is selected, try all COM Ports until the correct port has been found.
        4. Else, open the selected serial port
        5. Write the 'Versionr/' command to processor
        :param frame: The main frame of the Communication Interface tab
        :param row_index: The row_index -> used to determine where the message should be printed
        :param column_index: The column_index -> used to determine where the message should be printed
        :param row_span: The number of rows the message spans
        """
        frame = self.widgets['Spacer Frame']

        if self.serial_selected['COM Port'].get() == '':
            widgets.edit_message(self.widgets['Message'], self.msg_dict, 'er: COM Port')
            display_message()
            return
        elif self.serial_selected['Baud Rate'].get() == '':
            widgets.edit_message(self.widgets['Message'], self.msg_dict, 'er: Baud Rate')
            display_message()
            return
        elif self.serial_selected['COM Port'].get() == 'AutoSense':
            for i in range(len(self.serial_option_settings[0])):
                version = ser_version(frame, self.serial_option_settings[0][i], self.serial_selected['Baud Rate'].get())
                if version:
                    self.serial_selected['COM Port'].set(self.serial_option_settings[0][i])
                    break

        ser_version(frame, self.serial_selected['COM Port'].get(), self.serial_selected['Baud Rate'].get())


def display_message():
    """
    Display the message
    """
    row_index = 0
    column_index = 2
    row_span = 2
    CommunicationInterface.widgets['Message'].grid(row=row_index, column=column_index, rowspan=row_span)


def ser_open(port, baud_rate):
    """
    1. If serial port is already open, return True
    2. If port is not open, notify user
    :param port: The port number
    :param baud_rate: The baud rate
    :return:
        1. True if serial port is open
        2. False if serial port is not open
    """

    if CommunicationInterface.ser.isOpen():
        return True

    try:
        CommunicationInterface.ser = serial.Serial(port, baud_rate, timeout=0.05)
    except serial.serialutil.SerialException:
        widgets.edit_message(CommunicationInterface.widgets['Message'], CommunicationInterface.msg_dict,
                             'er: Port not open')
        display_message()
        return False
    return True


def ser_version(frame, port, baud_rate):
    """
    1. Check if serial port is open
        a. If serial port is open, continue
        b. else, return
    2. Send 'Version/r' command to processor
    3. If empty response, notify the user that the SDP5 isn't powered and return
    4. If the 'Version' command was successful, send the 'diaglevel eng\r' command
    :param frame: The spacer frame
    :param port: The port number
    :param baud_rate: The baud rate
    """
    is_open = ser_open(port, baud_rate)
    if not is_open:
        return is_open

    ret = write_to_processor(frame, 'version')

    empty_response = ''
    if ret == empty_response.encode():
        widgets.edit_message(CommunicationInterface.widgets['Message'], CommunicationInterface.msg_dict, 'er: No power')
        display_message()
        return

    ver_res = 'Version'
    if ret[0:7] == ver_res.encode():
        ret += write_to_processor(frame, 'diaglevel eng')

    # Display output to 'Driver Configuration' tab
    widgets.edit_message(CommunicationInterface.widgets['Message'], CommunicationInterface.msg_dict, msg_code=-1,
                         custom_message=ret)
    display_message()
    return True


def hdmion_cmd(cam_type):
    """
    1. Write the 'hdmionr/' command according to the camera selection
    :param cam_type: Camera variable
    :return: hdmion <flc|dfc> r/
    """
    cmd = 'hdmion '
    if cam_type == 0:
        CommunicationInterface.camName = '0'
        cmd += 'flc'
    elif cam_type == 1:
        CommunicationInterface.camName = '1'
        cmd += 'dfc'
    return cmd


def to_from_register_cmd(action, reg_address, hex_val, has_prompted_for_camera):
    """
    1. Notify user if no camera was selected
        a. Send only 1 error message per 'Read'/'Write'
    2. Write the read/write register command according to camera type and register address
    :param action: Read/Write
    :param reg_address: The register address in that row
    :param hex_val: The hex value in that row
    :param has_prompted_for_camera: Boolean that checks if invalid camera message has been displayed
    :return: ovwr/ovrd ...r/
    """
    if CommunicationInterface.camName == '':
        if not has_prompted_for_camera:
            invalid_setup_message(CommunicationInterface.widgets['Communication Interface Configuration Tab'],
                                  'er: Invalid camera')
        return

    cmd = CommunicationInterface.cmd_dict[action]
    cmd += CommunicationInterface.camName + ', '
    cmd += reg_address
    if hex_val != '':
        cmd += ', ' + str(hex_val)

    return cmd


def to_from_register(tab, action,
                     reg_address, hex_val, has_prompted_for_comms, has_prompted_for_camera):
    """
    1. If the register address is blank, do nothing
    2. Get the cmd syntax
    3. Write to the processor and print to the terminal
    :param tab: The Register Control tab
    :param action: Read/Write
    :param reg_address: The Register Address
    :param hex_val: The hex value
    :param has_prompted_for_comms: Boolean that checks if communication interface not selected message has been displayed
    :param has_prompted_for_camera: Boolean that checks if invalid camera message has been displayed
    :return: Processor output
    """
    if reg_address == '':
        return

    cmd = to_from_register_cmd(action, reg_address, hex_val, has_prompted_for_camera)

    ret = write_to_processor(tab, cmd, has_prompted_for_comms, is_register=True)

    return ret


def custom_write(tab, entry, cmd):
    """
    1. Clear the entered text
    2. Write to the processor and print to the terminal
    :param tab: The terminal output frame
    :param entry: The terminal input frame
    :param cmd: The inputted command
    """

    entry.delete('1.0', END)

    print(cmd, type(cmd))

    CommunicationInterface.widgets['Terminal'].print_to_terminal(cmd, 'in')

    pong = 'pong'.encode()
    if cmd == 'ping\n':
        CommunicationInterface.widgets['Terminal'].print_to_terminal(pong, 'out')

    hdmion = 'usage: hdmion <0|1>'.encode()
    if cmd == 'hdmion\n':
        CommunicationInterface.widgets['Terminal'].print_to_terminal(hdmion, 'out')

    hdmion_cam = 'ACK'.encode()
    if cmd == 'hdmion 1\n':
        CommunicationInterface.widgets['Terminal'].print_to_terminal(hdmion_cam, 'out')

    # write_to_processor(tab, cmd)


def write_to_processor(tab, cmd, has_prompted_for_comms=True, is_register=False):
    """
    1. If there was no command, do nothing
    2. Print user commands to Terminal
    3. Add a carriage return
    4. Notify the user if driver has not been selected
    5. Wait before immediately reading from the processor
    6. Read from the processor
        a. Some commands return multiple lines, collect all outputted lines from the processor
        b. Add extra logic to prevent the newline from appearing in the register tab
    7. Print processor output to the terminal
    :param tab: Where the error message will be displayed
    :param cmd: The command --> will be teminated by a carriage return
    :param is_register: Boolean indicating whether or not this is a register command
    :return: Processor output
    """

    if cmd == None:
        return

    CommunicationInterface.widgets['Terminal'].print_to_terminal(cmd, 'in')

    cmd += '\r'

    try:
        CommunicationInterface.ser.write(cmd.encode())
    except serial.serialutil.SerialException:
        if(not has_prompted_for_comms):
            invalid_setup_message(tab, 'er: Communication interface not selected')
        return

    time.sleep(0.05)

    ret = CommunicationInterface.ser.readline()
    if not is_register:
        nxt = CommunicationInterface.ser.readline()
    elif is_register:
        reg = ret[:-2]
    while not is_register and nxt != CommunicationInterface.cmd_dict['no response'].encode():
        ret += nxt
        nxt = CommunicationInterface.ser.readline()

    CommunicationInterface.widgets['Terminal'].print_to_terminal(ret, 'out')
    if not is_register:
        return ret
    else:
        return reg


def on_exit():
    """"
    Close the port after the application has been closed
    """
    if CommunicationInterface.ser.is_open:
        CommunicationInterface.ser.close()


def invalid_setup_message(tab, error_code):
    """
    1. Create the subwindow and lock access to outside of the window until 'OK' is selected or window is closed
    2. Create widgets (frame, error message, button) to fill subwindow
    3. Send the user to the correct configuration tab depending on what type of error they generated
    :param tab:
    :param error_code:
    :return:
    """

    # Size of the error message box
    w = 250
    h = 90

    error_box = subwindow.draw_subwindow(tab, w, h, 'Error')
    error_box.grab_set()

    # Create a spacer frame 
    spacer_frame = Frame(error_box, borderwidth=15)
    spacer_frame.pack(side=TOP, expand=YES, fill=BOTH)
    # Create an error message based on the error_code
    error_message = Label(spacer_frame, width=150, wraplength=300)
    error_message.pack()
    widgets.edit_message(error_message, CommunicationInterface.msg_dict, error_code)

    # Additional spacer frame
    spacer_frame2 = Frame(spacer_frame, borderwidth=3)
    spacer_frame2.pack()

    # Create OK button that closes the error box
    ok = Button(spacer_frame2, text='OK', width=7, command=lambda: error_box.destroy())
    ok.pack()

    tab_num = -1
    if error_code == 'er: Communication interface not selected':
        tab_num = CommunicationInterface.tab_Names.index('Communication Interface Configuration')
    if error_code == 'er: Invalid camera':
        tab_num = CommunicationInterface.tab_Names.index('HDMI Configuration')
        CommunicationInterface.has_prompted_for_camera = True
    CommunicationInterface.widgets['Notebook'].select(tab_num)
