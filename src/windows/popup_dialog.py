import tkinter as tk
import unittest
from helpers.metaclasses import SingletonABCMeta
from windows.popup import Popup

class PopupDialog(metaclass=SingletonABCMeta):
    def __init__(self, parent, title, message):
        self.parent = parent
        self.title = title
        self.message = message
        self.result = None

        self.root = tk.Toplevel(parent)
        self.root.title(title)

        self.label = tk.Label(self.root, text=message, justify=tk.LEFT, padx=10, pady=10, wraplength=300)
        self.label.pack()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.ok_button = tk.Button(self.button_frame, text="OK", command=self.ok_action)
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel_action)
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
        self.ok_button.pack(side=tk.RIGHT, padx=5)

        # Center the dialog
        self.root.update_idletasks()
        Popup.geo_center(self.root,self.root.winfo_width(), self.root.winfo_height())

    def ok_action(self):
        self.result = True
        self.root.destroy()

    def cancel_action(self):
        self.result = False
        self.root.destroy()

    @classmethod
    def popup(cls, parent, title, message, cancel_button=False):
        dialog = cls(parent, title, message)
        if not cancel_button:
            dialog.cancel_button.pack_forget()  # Hide the cancel button if not required
        parent.wait_window(dialog.root)
        return dialog.result

# Test case class
class TestPopupDialog(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()

    def tearDown(self):
        self.root.update()
        self.root.destroy()
        PopupDialog._instances.clear()      # pylint: disable=protected-access

    def test_popup_with_cancel(self):
        result = PopupDialog.popup(self.root, "Popup", "This is a multi-line message.\nClick OK to continue.", cancel_button=True)
        self.assertTrue(result)

    def test_popup_without_cancel(self):
        result = PopupDialog.popup(self.root, "Popup", "This is a multi-line message.\nClick OK to continue.")
        self.assertTrue(result)

# Run the test cases
if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
