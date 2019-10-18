import tkinter.filedialog as fd
import csv
import menu


class Temp():
    initial_ask = True

    # Open a 'Browse' Window to select a CSV file location
    def __init__(self, root):
        define_temp_file_location(root)

    # Save the temporary file to selected temp file location
    def save_to_temp(self, row_values):
        try: 
            self.file = open(self.tempfile, 'w', newline='')
        except FileNotFoundError:
            return
        writer = csv.writer(self.file)
        for row in row_values:
            writer.writerow(row)
        self.file.close()


def define_temp_file_location(root):
    Temp.tempfile = fd.asksaveasfilename(parent=root,
                                         initialdir=menu.Menu.workspace,
                                         title='Save Your Session:',
                                         filetypes=[('CSV Files', '*.csv')],
                                         defaultextension='*.csv')
    try: 
        Temp.file = open(Temp.tempfile, 'w', newline='')
    except FileNotFoundError:
        pass
