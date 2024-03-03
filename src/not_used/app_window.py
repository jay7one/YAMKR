from tkinter import Tk
class AppWindow(Tk):
    def __init__(self, name, w:int, h:int):
        super().__init__()
        self.title(name)
        ws,hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x,y = int((ws / 2) - (w / 2)), int((hs / 2) - (h / 2))
        self.geometry(f'{w}x{h}+{x}+{y}')
        self.resizable(False, False)
