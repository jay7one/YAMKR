import tkinter as tk
from app_bridge_helpers.tkinter_helper import TkinterHelper

class MacroDialog:
    btn_ok = None
    entry_name = None

    class FnKeyEntry(tk.Entry):
        def __init__(self, master, *args, **kwargs):
            super().__init__(master, *args, **kwargs)
            self.bind('<Key>', self.on_key_press)

        def on_key_press(self, event):
            if len(event.keysym) > 1 and event.keysym[0] == 'F':
                print(f"Debug {event.keysym=}, {event.char=}")
                self.delete(0,tk.END)
                self.insert(0,event.keysym)
                self.update()
                return "break"


    @classmethod
    def show(cls, parent_window, title="New Macro", macro_name="", macro_hotkey=""):
        cls.result_name = macro_name
        cls.result_hotkey = macro_hotkey

        dialog = tk.Toplevel(parent_window)
        dialog.title(title)

        dialog.withdraw()

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
        cls.entry_name = macro_name_entry

        hotkey_label = tk.Label(dialog, text="Hotkey (optional, F1-F12):")
        hotkey_label.grid(row=1, column=0, padx=5, pady=5)


        ok_button = tk.Button(dialog, text="OK", command=lambda: cls._return(dialog, macro_name_entry.get(), hotkey_entry.get()))
        ok_button.grid(row=2, column=0, padx=5, pady=5)
        cls.btn_ok = ok_button

        cls.btn_ok.config(state='disabled')

        hotkey_entry = cls.FnKeyEntry(dialog, validate="key", validatecommand=(dialog.register(cls._validate_hotkey), "%P", "%S"))
        hotkey_entry.grid(row=1, column=1, padx=5, pady=5)

        cancel_button = tk.Button(dialog, text="Cancel", command=dialog.destroy)
        cancel_button.grid(row=2, column=1, padx=5, pady=5)

        TkinterHelper.set_entry_text(macro_name_entry,cls.result_name )
        TkinterHelper.set_entry_text(hotkey_entry,cls.result_hotkey )

        dialog.bind('<Escape>', lambda evt: dialog.destroy() )
        dialog.bind('<Return>', lambda evt: cls._return(dialog, macro_name_entry.get(), hotkey_entry.get()))
        dialog.update()
        TkinterHelper.centre_dialog(dialog)
        dialog.deiconify()

        dialog.transient(parent_window)
        dialog.grab_set()
        dialog.focus_force()
        macro_name_entry.focus()

        # Make the dialog modal
        dialog.wait_window(dialog)

        return cls.result_name, cls.result_hotkey

    @classmethod
    def _validate_entry(cls, input_text):
        valid = input_text.replace("_", "").isalnum() or input_text == ""

        but_ok_on = input_text.replace("_", "").isalnum()

        cls.btn_ok.config(state='normal' if but_ok_on else 'disabled')
        return valid

    @classmethod
    def _validate_hotkey(cls, input_text, changed_text):
        print(f"Debug valid calleed: {(input_text, changed_text, cls.entry_name.get())=}")

        txt_len = len(changed_text)

        cls.btn_ok.config(state='disabled')

        default_state = 'normal' if len(cls.entry_name.get()) > 0 else 'disabled'

        if txt_len > 1 and changed_text[0] == "F" :
            if txt_len == 1:
                return True
            if 1 <= int(changed_text[1:]) <= 12:
                cls.btn_ok.config(state=default_state)
                return True
            return False

        if input_text in ["","F"]:
            cls.btn_ok.config(state=default_state)
            return True
        if not changed_text.isdigit():
            return False
        fnum = int(input_text[1:])
        if 1 <= fnum <= 12:
            cls.btn_ok.config(state=default_state)
            return True
        return False

    @classmethod
    def _return(cls, dialog, entered_macro_name, entered_hotkey):
        if len(entered_macro_name) == 0 : return
        cls.result_name = entered_macro_name
        cls.result_hotkey = entered_hotkey
        dialog.destroy()

# Example usage:
if __name__ == "__main__" :
    root = tk.Tk()
    m_name, hotkey = MacroDialog.show(root)
    print("Macro Name:", m_name)
    print("Hotkey:", hotkey)
