import tkinter as tk

class HotKeyHelper:

    @classmethod
    def add_hotkey(cls, win_root, hotkey_label:tk.Label, add_hotkey_button:tk.Button, hotkey_callback):
        add_hotkey_button.config(relief=tk.SUNKEN)
        add_hotkey_button.configure(state='disabled')
        cls.hotkey_callback = hotkey_callback
        win_root.bind('<Key>', lambda event: cls.on_key_press(event, win_root, hotkey_label, add_hotkey_button))

    @classmethod
    def on_key_press(cls, event, root, hotkey_label, add_hotkey_button):

        print(f"Debug internal hk key press :{event=}")

        if event.keysym.startswith('F') and event.keysym[1:].isdigit() and event.keysym != 'F10':
            hotkey = event.keysym
            cls.set_hotkey(root,add_hotkey_button, hotkey_label, f"{hotkey}")
            return False
        elif event.keysym == 'Escape':
            cls.set_hotkey(root,add_hotkey_button, hotkey_label, "")
            return False
        return True

    @classmethod
    def set_hotkey(cls,root,add_hotkey_button, hotkey_label, txt):
        cls.unbind_hotkey(root,add_hotkey_button)
        hotkey_label.configure(text=txt)
        cls.hotkey_callback()

    @classmethod
    def unbind_hotkey(cls,root,add_hotkey_button):
        root.unbind('<Key>')
        add_hotkey_button.configure(state='normal')
        add_hotkey_button.config(relief=tk.RAISED)
