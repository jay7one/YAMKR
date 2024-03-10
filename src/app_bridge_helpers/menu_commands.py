from abc import ABC
import tkinter as tk
from app_bridge_helpers.app_bridge_base import AppBridgeBase

class MenuCommands(ABC, AppBridgeBase):

    def menu_callback(self, var_tag, *args):
        #print(f"debug cb {var_tag=}{args=}")
        set_on=None
        if args:
            bv:tk.BooleanVar = args[0]
            set_on = bv.get()

        if var_tag == 'On Play':
            self.app_settings.set_min_on_play(set_on)
        elif var_tag == 'On Record':
            self.app_settings.set_min_on_record(set_on)

        if var_tag[:3] == "On ":
            self.sbar_msg(f"Minimize {var_tag} set {'On' if set_on else 'Off'}")


    def setup_menus(self):
        menu_defs = {
            # Label,  Var_Tag, fn
            "On Play":      ('min_on_play',     self.app_settings.get_min_on_play       , self.main_win.sub_menu),
            "On Record":    ('min_on_record',   self.app_settings.get_min_on_record     , self.main_win.sub_menu)
        }
        for lbl, values in menu_defs.items():
            var_tag, init_value_fn, sub_menu = values
            menu_idx = sub_menu.index(lbl)

            if var_tag :
                self.menu_setting_vars[var_tag] = tk.BooleanVar()
                sub_menu.entryconfig(menu_idx,variable=self.menu_setting_vars[var_tag],  command=lambda v=self.menu_setting_vars[var_tag], lbl=lbl : self.menu_callback(lbl,v) )
                self.menu_setting_vars[var_tag].set( init_value_fn() )
            else:
                sub_menu.entryconfig(menu_idx,variable=self.menu_setting_vars[var_tag],  command=lambda  lbl=lbl : self.menu_callback(lbl))
