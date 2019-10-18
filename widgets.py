from tkinter import *


# Generic create message function maintains consistency between types of messages
# (blue -> processor output, red -> error)
def edit_message(message_label, msg_dict, msg_code, custom_message=None):
    if msg_dict == None and msg_code == -1:
        message_label.config(text=custom_message, justify=LEFT, padx=5)
    elif msg_code == -1:
        message_label.config(text=custom_message, justify=LEFT, padx=5, fg='blue')
    elif msg_code[0:3] == 'er:':
        message_label.config(text=msg_dict[msg_code], justify=LEFT, padx=5, fg='red')
    elif msg_code[0:5] == 'note:':
        message_label.config(text=msg_dict[msg_code], justify=LEFT, padx=5)


# Create, display, and label ridged frames; Return the frame
def create_display_label_ridged_frames(frame, row_index, column_index, column_span, option_name, label_span):
    ridged_f = Frame(frame, borderwidth=1, relief=RIDGE, padx=25, pady=25)
    ridged_f.grid(row=row_index, column=column_index, columnspan=column_span, padx=5, pady=5)
    Label(ridged_f, text=option_name, width=12, font='bold').grid(row=0, column=0, columnspan=label_span)
    return ridged_f


# Create a dropdown menu; Return the selection
def create_dropdown(frame, option_name, option_choices, command):
    Label(frame, text=option_name).grid()
    var = StringVar(frame)
    d = OptionMenu(frame, var, *option_choices, command=command)
    d.grid()
    return var


# Create an entry, return the entry
# (need a .get() function to get the value after the user has inputted value)
def create_entries(frame, option_name, default_text=''):
    Label(frame, text=option_name).grid()
    var = StringVar(frame)
    entry = Entry(frame, textvariable=var)
    entry.insert(END, default_text)
    entry.grid()
    return var


# Create and display radiobuttons
def create_display_radiobuttons(frame, option_name, shared_variable, row_index, column_index, value_name):
    rb = Radiobutton(frame, text=option_name, value=value_name, variable=shared_variable)
    rb.grid(row=row_index, column=column_index)
