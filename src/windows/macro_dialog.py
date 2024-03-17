import tkinter as tk
from windows.tkinter_helper import TkinterHelper as tkh

class MacroDialog:
    btn_ok = None
    entry_name = None
    entry_hotkey = None

    class FnKeyEntry(tk.Entry):
        def __init__(self, master, *args, **kwargs):
            super().__init__(master, *args, **kwargs)
            self.bind('<Key>', self.on_key_press)

        def on_key_press(self, event):
            if len(event.keysym) > 1 and event.keysym[0] == 'F':
                self.delete(0,tk.END)
                self.insert(0,event.keysym)
                self.update()
                return "break"
            return None


    @classmethod
    def show(cls, parent_window, title="New Macro", macro_name="", macro_hotkey=""):
        cls.result_name = macro_name
        cls.result_hotkey = macro_hotkey

        dialog = tk.Toplevel(parent_window)
        dialog.title(title)

        macro_name_label = tk.Label(dialog, text="Macro Name:")
        macro_name_label.grid(row=0, column=0, padx=5, pady=5)

        cls.entry_name = tk.Entry(dialog, validate="key", validatecommand=(dialog.register(cls._validate_entry), "%P"))
        cls.entry_name.grid(row=0, column=1, padx=5, pady=5)

        hotkey_label = tk.Label(dialog, text="Hotkey (optional, F1-F12):")
        hotkey_label.grid(row=1, column=0, padx=5, pady=5)


        cls.btn_ok = tk.Button(dialog, text="OK", command=lambda: cls._return(dialog, cls.entry_name.get(), cls.entry_hotkey.get()))
        cls.btn_ok.grid(row=2, column=0, padx=5, pady=5)

        cls.btn_ok.config(state='disabled')

        cls.entry_hotkey = cls.FnKeyEntry(dialog, validate="key", validatecommand=(dialog.register(cls._validate_hotkey), "%P", "%S"))
        cls.entry_hotkey.grid(row=1, column=1, padx=5, pady=5)

        cancel_button = tk.Button(dialog, text="Cancel", command=dialog.destroy)
        cancel_button.grid(row=2, column=1, padx=5, pady=5)

        tkh.set_entry_text(cls.entry_name,cls.result_name )
        tkh.set_entry_text(cls.entry_hotkey,cls.result_hotkey )

        dialog.bind('<Escape>', lambda evt: dialog.destroy() )
        dialog.bind('<Return>', lambda evt: cls._return(dialog, cls.entry_name.get(), cls.entry_hotkey.get()))

        tkh.centre_dialog(dialog, 365, 130)

        dialog.transient(parent_window)
        dialog.grab_set()
        dialog.focus_force()
        cls.entry_name.focus()

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
        cls.btn_ok.config(state='disabled')
        default_state = 'normal' if len(cls.entry_name.get()) > 0 else 'disabled'
        rv = cls._validate_hotkey_actual(input_text, changed_text)
        if cls.is_hotkey_txt(input_text):
            cls.btn_ok.config(state=default_state)
        return rv

    @classmethod
    def _validate_hotkey_actual(cls, input_text, changed_text):

        txt_len = len(input_text)
        changed_text = changed_text.upper()

        if len(changed_text) > 1 : # Function key pressed
            return changed_text[0] == 'F'

        if input_text.upper() == "F":
            return True

        if txt_len == 0 :
            return True
        if txt_len == 1 :
            if changed_text[0] == "F":
                return True
                #tkh.set_entry_text(cls.entry_hotkey,"F")
            return False

        if not changed_text.isdigit() or not cls.is_hotkey_txt(input_text):
            return False

        return True

    @staticmethod
    def is_hotkey_txt(txt):
        txt = txt.upper()
        if len(txt) < 2 : return False
        if txt[0] != "F": return False
        return 1 <= int(txt[1:]) <= 12


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
