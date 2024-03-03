from tkinter import Toplevel
from sys import platform

class Popup(Toplevel):
    def __init__(self, name, w, h, parent):
        super().__init__(parent)
        self.title(name)
        self.resizable(False, False)
        if platform == "win32":
            self.attributes("-toolwindow", 1)
        else:
            self.attributes("-topmost", 1)
        self.grab_set()
        Popup.geo_center(self,w,h)

    @classmethod
    def geo_center(cls,root,w,h):
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = int( (ws / 2) - (w / 2))
        y = int( (hs / 2) - (h / 2))
        root.geometry(f'{w}x{h}+{x}+{y}')
