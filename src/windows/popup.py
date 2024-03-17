from tkinter import Toplevel
from sys import platform
from windows.tkinter_helper import TkinterHelper

class Popup(Toplevel):
    def __init__(self, name, w, h, parent):
        super().__init__(parent)
        self.title(name)
        self.resizable(False, False)

        if platform == "win32":
            self.attributes("-toolwindow", 1)
        else:
            self.attributes("-topmost", 1)

        TkinterHelper.centre_dialog(self,w,h)

        self.grab_set()
