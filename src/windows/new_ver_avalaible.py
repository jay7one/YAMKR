from tkinter import Frame, Label, Button, TOP, BOTTOM, LEFT
from webbrowser import open as OpenUrl
from windows.popup import Popup

class NewVerAvailable(Popup):
    def __init__(self, parent, version):
        super().__init__("New Version Available!", 300, 250, parent)
        if parent: parent.prevent_record = True
        Label(self, text=f"New Version {version} available!").pack(side=TOP)
        Label(self, text="Click the button to open releases page on GitHub").pack(side=TOP)
        buttonArea = Frame(self)
        Button(buttonArea, text="Click here to view",
               command=lambda: OpenUrl("https://github.com/jay7one/PyMouseMacro/releases")).pack(side=LEFT, pady=10)
        Button(buttonArea, text="Close", command=self.destroy).pack(side=LEFT, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        if parent: parent.prevent_record = False

if __name__ == "__main__":
    NewVerAvailable(None, "NewVerNumber")
