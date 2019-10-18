from tkinter import *


def create_tabs(nb, tab_names):
    """
    1. Take a list of tab_names and create corresponding tabs
    :param nb: A Notebook widget
    :param tab_names: A list of tab names
    :return: A list of the tab widgets created
    """
    tabs = []
    for tab_name in tab_names:
        tab = create_tab(nb, tab_name)
        tabs.append(tab)
    return tabs


def create_tab(nb, tab_name):
    """
    1. Create a tab (Frame) in nb
    :param nb: A Notebook widget
    :param tab_name: A list of tab names
    :return: A frame representing the tab
    """
    t = Frame(nb)
    nb.add(t, text=tab_name)
    return t



