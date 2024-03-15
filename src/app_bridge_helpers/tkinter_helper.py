import tkinter as tk
from app_bridge_helpers.tab_ordering import TabOrdering

class TkinterHelper(TabOrdering):
    main_win_geo:tuple[int,int,int,int] = (0,0,0,0)
    @classmethod
    def set_main_geo(cls, win_tl:tk.Toplevel, geo_str:str):
        win_tl_geo = win_tl.geometry()
        cls.main_win_geo = cls.get_geo(win_tl_geo)


    @staticmethod
    def get_geo(geometry_str):
        width_height, gx, gy = geometry_str.split("+")
        w, h = map(int, width_height.split("x"))
        gx, gy = map(int, [gx,gy])
        return gx, gy, w, h

    @classmethod
    def centre_dialog(cls, dialog:tk.Toplevel, tl_w=0, tl_h=0):

        mw_x, mw_y, mw_w, mw_h = cls.main_win_geo

        if mw_w == 0:
            print("main window geo not stored yet")

        #ws = root.winfo_screenwidth()
        #hs = root.winfo_screenheight()

        if tl_w <= 1:
            try:
                tl_h, tl_w = dialog.winfo_height(),dialog.winfo_width()
            except: # pylint: disable=bare-except
                tl_h, tl_w = dialog.winfo_reqheight() , dialog.winfo_reqwidth()

        x = mw_x + (mw_w//2) - (tl_w // 2)
        y = mw_y + (mw_h//2) - (tl_h // 2)

        #print(f"Geo: {tl_w}x{tl_h}+{x}+{y}")
        dialog.geometry(f'{tl_w}x{tl_h}+{x}+{y}')

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

    @staticmethod
    def clear_frame(frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    @staticmethod
    def unbind_mousewheel(widget):
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')

        children = widget.winfo_children()
        if len(children) > 0 :
            child = children[0]
            child.unbind_all('<MouseWheel>')
            child.unbind_all('<Shift-MouseWheel>')
            #def non_fn(e,child): pass
            #child.bind_all('<MouseWheel>', lambda e: non_fn(e, child))
            #child.bind_all('<Shift-MouseWheel>', lambda e: non_fn(e, child))




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
