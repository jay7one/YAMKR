import tkinter as tk

class TkinterHelper:
    @staticmethod
    def get_window_position(window):
        """Get the position of the main window."""
        x_pos = window.winfo_x()
        y_pos = window.winfo_y()
        return (x_pos, y_pos)

    @staticmethod
    def set_window_position(window, x, y):
        """Set the position of the main window."""
        window.geometry(f"+{x}+{y}")

    @staticmethod
    def set_window_geo(window, geo):
        window.geometry(geo)

    @staticmethod
    def get_window_geo(window):
        geo_str = window.geometry()
        plus_index = geo_str.find('+')
        if plus_index == -1: return None
        positional_part = geo_str[plus_index:]
        return positional_part


    @staticmethod
    def lock_position_recursive(widget):
        try:
            if isinstance(widget, tk.Toplevel):
                x, y = widget.winfo_x(), widget.winfo_y()
                widget.geometry(f"+{x}+{y}")  # Set geometry to current position
            #else:
            #    print(f"Not doing {widget=}")
        except tk.TclError:
            print(f"Passing {widget=}")

        # Recursively lock position for sub-items
        for child in widget.winfo_children():
            TkinterHelper.lock_position_recursive(child)

    @staticmethod
    def lock_position(widget):
        TkinterHelper.lock_position_recursive(widget)

    @staticmethod
    def button_state(button:tk.Button):
        return button['relief'] == tk.SUNKEN

    @staticmethod
    def button_down(button):          button.config(relief=tk.SUNKEN)

    @staticmethod
    def button_up(button):            button.config(relief=tk.RAISED)

    @staticmethod
    def button_toggle(button, down):  button.config(relief=tk.SUNKEN if down else tk.RAISED)

    @staticmethod
    def get_entry_int(entry:tk.Entry):
        text = entry.get()
        if text == "" : return 0
        return int(text)

    @staticmethod
    def set_entry_text(tk_entry:tk.Entry,text):
        tk_entry.delete(0,tk.END)
        tk_entry.insert(0,text)
        return

    @staticmethod
    def validate_number(P) -> bool:
        #print(f"Validate {P=}")
        p_str = str(P)
        return p_str == '' or str.isdigit(p_str)

# Example usage
if __name__ == "__main__":
    root_window = tk.Tk()

    # Create a Toplevel window
    top_window = tk.Toplevel(root_window)
    top_window.title("Locked Toplevel")

    # Add some widgets
    label_widget = tk.Label(top_window, text="Locked Position!")
    label_widget.pack()
    button_widget = tk.Button(top_window, text="Click Me")
    button_widget.pack()

    # Lock the positions
    TkinterHelper.lock_position(top_window)

    root_window.mainloop()
