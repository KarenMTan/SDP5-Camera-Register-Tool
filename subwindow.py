from tkinter import *

# Draw a subwindow of size width (w) and height (h)
# Name the subwindow (title)
def draw_subwindow(root, w, h, title):
    subwindow = Toplevel(root)
    subwindow.title(title)
    geo = str(w) + 'x' + str(h)
    subwindow.geometry(geo)
    return subwindow

# Destroy the root window on exit
def on_exit(root):
    root.destroy()
    
