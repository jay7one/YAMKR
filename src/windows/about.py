from tkinter import Frame, Label, Button, TOP, BOTTOM, LEFT
from webbrowser import open as OpenUrl
from windows.popup import Popup
from helpers.version import Version

class About(Popup):
    def __init__(self, parent):
        super().__init__("About PyMouseMacros", 300, 250, parent)
        if parent: parent.prevent_record = True
        Label(self, text=f"\nPyMouseMacros\n\nMouse and Keyboard\nMacro Manager\n\nVersion:{Version.get_from_file()}").pack(side=TOP)
        buttonArea = Frame(self)
        Button(buttonArea, text="GitHub Repo",
               command=lambda: OpenUrl("https://github.com/jay7one/PyMouseMacros")).pack(side=LEFT, pady=10, padx=10)
        Button(buttonArea, text="ReadMe",
               command=lambda: OpenUrl("https://github.com/jay7one/PyMouseMacros/blob/main/README.md")).pack(side=LEFT, pady=10, padx=10)
        Button(buttonArea, text="Close", command=self.destroy).pack(side=LEFT, padx=10 )
        buttonArea.pack(side=BOTTOM, pady=10)

        self.focus_force()
        self.lift()

        self.wait_window()
        if parent: parent.prevent_record = False
