import tkinter as tk
from tkinter import ttk

class TabOrdering():
    class WidgetInfo:      # pylint: disable=too-few-public-methods
        def __init__(self, widget, abs_x, abs_y):
            self.widget = widget
            self.abs_x = abs_x
            self.abs_y = abs_y

    @classmethod
    def find_all_widgets(cls, parent, widgets, parent_abs_x=0, parent_abs_y=0):
        CLUSTERING=6
        parent_abs_x = int ( parent_abs_x/CLUSTERING)
        parent_abs_y = int ( parent_abs_y/CLUSTERING)

        for widget in parent.winfo_children():
            if isinstance(widget, (tk.Frame, tk.Canvas, tk.Toplevel, tk.LabelFrame, ttk.Frame)):
                cls.find_all_widgets(widget, widgets, parent_abs_x + widget.winfo_x(), parent_abs_y + widget.winfo_y())
            elif isinstance(widget, (tk.Button, tk.Entry, ttk.Button, ttk.Entry)):
                widgets.append(cls.WidgetInfo(widget,
                                          parent_abs_x + int(widget.winfo_x() / CLUSTERING),
                                          parent_abs_y + int(widget.winfo_y() / CLUSTERING)
                                          )
                )

    @classmethod
    def set_tab_order(cls, parent):
        widgets = []
        cls.find_all_widgets(parent, widgets)

        widgets.sort(key=lambda w: (w.abs_y, w.abs_x))

        for widget_info in widgets:
            if widget_info.widget.winfo_x() >= 0:
                widget_info.widget.lift()
