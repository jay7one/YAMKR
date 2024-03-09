import tkinter as tk

class NewMacroDialog:
    @classmethod
    def create_macro(cls, parent_window):
        cls.result_name = None
        cls.result_hotkey = None

        dialog = tk.Toplevel(parent_window)
        dialog.title("New Macro")

        # Center the dialog on the screen
        window_width = dialog.winfo_reqwidth()
        window_height = dialog.winfo_reqheight()
        position_right = int(dialog.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(dialog.winfo_screenheight() / 2 - window_height / 2)
        dialog.geometry(f"+{position_right}+{position_down}")

        macro_name_label = tk.Label(dialog, text="Macro Name:")
        macro_name_label.grid(row=0, column=0, padx=5, pady=5)

        macro_name_entry = tk.Entry(dialog, validate="key", validatecommand=(dialog.register(cls._validate_entry), "%P"))
        macro_name_entry.grid(row=0, column=1, padx=5, pady=5)

        hotkey_label = tk.Label(dialog, text="Hotkey (optional, F1-F12):")
        hotkey_label.grid(row=1, column=0, padx=5, pady=5)

        hotkey_entry = tk.Entry(dialog, validate="key", validatecommand=(dialog.register(cls._validate_hotkey), "%P", "%S"))
        hotkey_entry.grid(row=1, column=1, padx=5, pady=5)

        ok_button = tk.Button(dialog, text="OK", command=lambda: cls._return(dialog, macro_name_entry.get(), hotkey_entry.get()))
        ok_button.grid(row=2, column=0, padx=5, pady=5)

        cancel_button = tk.Button(dialog, text="Cancel", command=dialog.destroy)
        cancel_button.grid(row=2, column=1, padx=5, pady=5)

        dialog.transient(parent_window)
        dialog.grab_set()

        # Make the dialog modal
        dialog.wait_window(dialog)

        return cls.result_name, cls.result_hotkey

    @classmethod
    def _validate_entry(cls, input_text):
        return input_text.replace("_", "").isalnum() or input_text == ""

    @classmethod
    def _validate_hotkey(cls, input_text, changed_text):
        print(f"valid:{input_text=}")
        if input_text in ["","F"]:
            return True

        if not changed_text.isdigit():
            return False

        fnum = int(input_text[1:])

        if 1 <= fnum <= 12:
            return True

        return False


    @classmethod
    def _return(cls, dialog, entered_macro_name, entered_hotkey):
        cls.result_name = entered_macro_name
        cls.result_hotkey = entered_hotkey
        dialog.destroy()

# Example usage:
if __name__ == "__main__" :
    root = tk.Tk()
    macro_name, hotkey = NewMacroDialog.create_macro(root)
    print("Macro Name:", macro_name)
    print("Hotkey:", hotkey)
