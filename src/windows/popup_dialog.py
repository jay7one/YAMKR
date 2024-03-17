import tkinter as tk
from windows.tkinter_helper import TkinterHelper

class PopupDialog:
    @classmethod
    def popup(cls, parent_window, title, message, enable_cancel=False):
        cls.result = False


        txt_font_ht = 18
        button_ht = 80
        border_ht = 10

        line_count = cls.calculate_num_lines(message,26)
        window_height = (txt_font_ht * line_count) + button_ht + border_ht

        dialog = tk.Toplevel(parent_window)
        dialog.title(title)

        TkinterHelper.centre_dialog(dialog,dialog.winfo_reqwidth(), window_height )

        label = tk.Label(dialog, text=message, justify=tk.CENTER, padx=10, pady=5, wraplength=210, height=line_count,anchor="n")
        label.pack(pady=5,padx=10)

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

    @staticmethod
    def calculate_num_lines(string, window_width):
        lines = string.split('\n')
        num_lines = 0

        for line in lines:
            num_lines += (len(line) // window_width) + 1
            if len(line) % window_width == 0:
                num_lines -= 1

        return num_lines


# Example usage:
if __name__ == "__main__" :
    root = tk.Tk()
    result_back = PopupDialog.create_macro(root, "Test", "Message text\nsecond line",False)
    print(f"Rs: {result_back=}" )
    result_back = PopupDialog.create_macro(root, "Test", "Message text\nsecond line",True)
    print(f"Rs: {result_back=}" )
