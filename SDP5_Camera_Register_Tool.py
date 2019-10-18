from tkinter import *
from tkinter import ttk
import login
import nbtb
import menu
import communicationInterface
import hdmi
import registers
import terminal


class Application(Frame):
 
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
    
        # Create login window
        login_window = login.Login(root)
        
        # Create Notebook and Tabs
        tab_names = ['Communication Interface Configuration', 'HDMI Configuration', 'Register Control', 'Terminal']
        nb = ttk.Notebook(root)
        nb.pack(expand=1, fill=BOTH)
        tabs = nbtb.create_tabs(nb, tab_names)
        
        # Create Menu Bar
        menu.Menubar(root)
        
        # Fill Terminal Tab
        ter = terminal.Terminal(tabs, tab_names.index('Terminal'))
     
        # Fill Driver Configuration Tab
        dri = communicationInterface.CommunicationInterface(nb, tabs, tab_names, ter)

        # Fill HDMI Configuration Tab
        hdmi.HDMI(nb, tabs, tab_names.index('HDMI Configuration'), ter)

        # Fill Register Control Tab
        registers.Registers(tabs, tab_names.index('Register Control'))

    @staticmethod
    def on_exit(root_window):
        # Close the open serial port
        communicationInterface.on_exit()

        # Destroy the root window
        root_window.destroy()


# Width (w) and Height (h) of root window        
w = 840
h = 500        

# Create, name, and define size of root window
root = Tk()
root.title('SDP5 Camera Register Tool')
rSize = str(w) + 'x' + str(h)
root.geometry(rSize)

# Create an Application object 
app = Application(master=root)
root.protocol('WM_DELETE_WINDOW', lambda: app.on_exit(root))

# Infinite loop that waits for events until window is closed
app.mainloop()
