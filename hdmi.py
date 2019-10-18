from tkinter import *
import serial
import widgets
import terminal
import communicationInterface

class HDMI():
    widgets = {}

    # Camera Options
    camera = ['Camera']

    # Camera Drop Down
    camera_options = ['FLC', 'DFC']

    msg_dict = {'er: No camera': 'Please select either FLC or DFC'}
    
    def __init__(self, nb, tabs, tabIndex, ter):
        self.widgets['Notebook'] = nb

        self.widgets['Terminal'] = ter

        self.widgets['HDMI Tab'] = tabs[tabIndex]

        self.widgets['Spacer Frame'] = Frame(self.widgets['HDMI Tab'], borderwidth=10)
        self.widgets['Spacer Frame'].grid(row=0, column=0)

        # Create, display, and label Camera Option Frame
        self.widgets['Camera Frame'] = widgets.create_display_label_ridged_frames(self.widgets['Spacer Frame'], 0, 0, 1, self.camera, 2)

        # Create Camera Selection Radio Buttons
        self.camera_sel = IntVar(self.widgets['HDMI Tab'])
        self.camera_sel.set(-1)
        for i in range(len(self.camera_options)):
            widgets.create_display_radiobuttons(self.widgets['Camera Frame'], self.camera_options[i], self.camera_sel, 1, i, i)

        # Create and display 'HDMI on' Button
        self.widgets['hdmion Button'] = Button(self.widgets['Spacer Frame'],
                                               text='Apply',
                                               padx=5,
                                               command=lambda:
                                               hdmi(self.camera_sel.get()))
        self.widgets['hdmion Button'].grid(row=1, column=0)

        self.widgets['Message'] = Label(self.widgets['Spacer Frame'], width=30, wraplength=250)

def hdmi(camType):
    row_index = 0
    column_index = 1

    # Notify user if camera was not selected
    if camType == -1:
        widgets.edit_message(HDMI.widgets['Message'], HDMI.msg_dict, 'er: No camera')
        HDMI.widgets['Message'].grid(row=row_index, column=column_index)
    else:
        cmd = communicationInterface.hdmion_cmd(camType)
        msg = communicationInterface.write_to_processor(HDMI.widgets['Spacer Frame'], cmd, False)
        
        # Write msg to the HDMI Configuration tab
        widgets.edit_message(HDMI.widgets['Message'], HDMI.msg_dict, msg_code=-1, custom_message=msg)
        HDMI.widgets['Message'].grid(row=row_index, column=column_index)
    
    
