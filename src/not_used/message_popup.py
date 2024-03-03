from tkinter import Frame, Label, Button, TOP,BOTTOM
from windows.popup_dialog import Popup

class MessagePopup(Popup):
    def __init__(self, parent, msg_text, msg_type="Warning",w=400,h=300):
        super().__init__(msg_type, w, h, parent)
        if parent: parent.prevent_record = True

        for label_line in iter(msg_text.splitlines()):
            Label(self,text=label_line.strip(), font=("Segoe UI", 10)).pack(side=TOP, pady=2)

        buttonArea = Frame(self)
        Button(buttonArea, text="OK", command=self.destroy).pack(side=BOTTOM, padx=10)
        buttonArea.pack(side=BOTTOM, pady=10)
        self.wait_window()
        if parent: parent.prevent_record = False

if __name__ == "__main__":
    not_windows = MessagePopup(None,'''
        test text
        on multiple lines
        end of message
        ''')
