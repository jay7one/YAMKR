import tkinter as tk
from windows.popup import Popup

class PopupDialog:
    @classmethod
    def popup(cls, parent_window, title, message, enable_cancel=False):
        cls.result = False
        dialog = tk.Toplevel(parent_window)
        dialog.title(title)

        # Center the dialog on the screen
        window_width = dialog.winfo_reqwidth()
        window_height = dialog.winfo_reqheight()
        position_right = int(dialog.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(dialog.winfo_screenheight() / 2 - window_height / 2)
        dialog.geometry(f"+{position_right}+{position_down}")

        label = tk.Label(dialog, text=message, justify=tk.LEFT, padx=10, pady=10, wraplength=300)
        label.pack()

        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=5)

        ok_button = tk.Button(button_frame, text="OK", command=lambda: cls._return(dialog))
        ok_button.pack(side=tk.RIGHT, padx=5)
        if enable_cancel:
            cancel_button = tk.Button(button_frame, text="Cancel", command=dialog.destroy)
            cancel_button.pack(side=tk.RIGHT, padx=5)
            dialog.bind('<Escape>', lambda evt: dialog.destroy() )

        dialog.bind('<Return>', lambda evt: cls._return(dialog))

        # Center the dialog
        dialog.update_idletasks()
        Popup.geo_center(dialog,dialog.winfo_width(), dialog.winfo_height())

        dialog.transient(parent_window)
        dialog.grab_set()
        dialog.focus_force()

        ok_button.focus_set()

        # Make the dialog modal
        dialog.wait_window(dialog)

        return cls.result

    @classmethod
    def _return(cls, dialog):
        cls.result=True
        dialog.destroy()


# Example usage:
if __name__ == "__main__" :
    root = tk.Tk()
    result_back = PopupDialog.create_macro(root, "Test", "Message text\nsecond line",False)
    print(f"Rs: {result_back=}" )
    result_back = PopupDialog.create_macro(root, "Test", "Message text\nsecond line",True)
    print(f"Rs: {result_back=}" )
