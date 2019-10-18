from tkinter import *
import rows

class CheckBoxes(Checkbutton):
    # A 2D list of rows of binary displays in the Register Control tab
    value = []
    
    def __init__(self, master, row_index):
        Checkbutton.__init__(self, master)
        
        # Each Checkbutton has its individual value
        self.value += [[]]

        # Create 8 checkbuttons per row
        for i in range(8):
            self.value[row_index].append(IntVar())
            chbt = Checkbutton(master, variable=self.value[row_index][i], command=lambda:
                                                    self.display_binary_to_hex(row_index, self.value[row_index]))
            chbt.grid(row=0, column=i)
            if(i == 4):
                chbt.grid(padx=(20, 0))
    
    def display_hex_to_binary(self, row_index, hex_val):
        bi = self.convert_hex_to_bi(hex_val)

        if(bi == None):
            return

        for i in range(len(bi)):
            self.value[row_index][i].set(int(bi[i]))

    # Returns a 1 byte binary representation of the hex value
    def convert_hex_to_bi(self, hex_val):
        try:
            dec_val = int(hex_val, 16)
        except ValueError:
            return
        bi_val = bin(dec_val).replace('0b', '')

        remainder = 8 - len(bi_val)
        for i in range(remainder):
            bi_val = '0' + bi_val
        return bi_val

    # Convert array representing binary value of a row
    # into a decimal value, then a hex value
    # Delete the previous value
    # Insert new value into the corresponding entry
    def display_binary_to_hex(self, row_index, bi_val):
        bi_str = ''
        for thing in bi_val:
            bi_str += str(thing.get())
        
        dec_val = int(bi_str, 2)
        hex_val = hex(dec_val).replace('0x', '')
        rows.Rows.widget_dict['Hex Value'][row_index].delete(0, END)
        rows.Rows.widget_dict['Hex Value'][row_index].insert(0, hex_val.upper())
