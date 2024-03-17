import tkinter as tk

class VerticalScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    :width:, :height:, :bg: are passed to the underlying Canvas
    :bg: and all other keyword arguments are passed to the inner Frame
    note that a widget layed out in this frame will have a self.master 3 layers deep,
    (outer Frame, Canvas, inner Frame) so
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.canvas.addtag_all("all")   # (added) for configuring width
        self.vsb['command'] = self.canvas.yview

        self.inner = tk.Frame(self.canvas, bg=bg)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(0, 0, window=self.inner, anchor='nw')     # changed - starts from (0, 0)
        self.canvas.bind("<Configure>", self._on_frame_configure)           # (changed) canvas bind instead of inner

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, _):
        _, _, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()                               # (added) to resize inner frame
        self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))
        self.canvas.itemconfigure("all", width=width)    # (added) to resize inner frame


    def _bind_mouse(self, _):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, _):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )

    def __str__(self):
        return str(self.outer)

#  **** SCROLL BAR TEST *****
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scrollbar Test")
    root.geometry('400x500')

    frame = VerticalScrolledFrame(root,
        width=300,
        borderwidth=2,
        relief=tk.SUNKEN,
        background="blue")  # changed for debug ("light gray" -> "blue")
    frame.pack(fill=tk.BOTH, expand=True) # fill window; changed to pack

    # wrapper added to demonstrate pack case
    wrapper = tk.Frame(frame, bg='green')
    wrapper.pack(expand=tk.YES, fill=tk.BOTH, side=tk.TOP)

    for i in range(30):
        # row added
        row = tk.Frame(wrapper)
        row.pack(expand=tk.NO, fill=tk.BOTH, side=tk.TOP)

        label = tk.Label(row, text="This is a label "+str(i))
        label.pack(expand=tk.YES, fill=tk.BOTH, side=tk.LEFT)   # grid changed to pack

        text = tk.Entry(row, textvariable="text")
        text.pack(expand=tk.YES, fill=tk.BOTH, side=tk.LEFT)   # grid changed to pack

    root.mainloop()
