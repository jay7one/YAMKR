from abc import ABC
import copy
import tkinter as tk
from app_bridge.app_bridge_base import AppBridgeBase
from helpers.version import Version
from windows.about import About
from windows.macro_merger import MacroMerger

class MenuCommands(ABC, AppBridgeBase):
    MENU_MIN_PLAY   = 'Minimize on Play'
    MENU_MIN_REC    = 'Minimize on Record'
    MENU_CHK_UPD    = 'Check for Updates'
    MENU_ABOUT      = 'About'
    MENU_MERGE      = 'Merge ...'
    MENU_EVTS_COPY  = 'Copy Events'
    MENU_EVTS_PASTE = 'Paste Events'

    copied_events = None
    copied_offsets = None

    def menu_callback(self, var_tag, *args):
        set_on=None
        if args:
            bv:tk.BooleanVar = args[0]
            set_on = bv.get()

        if var_tag == self.MENU_MIN_PLAY:
            self.app_settings.set_min_on_play(set_on)
        elif var_tag == self.MENU_MIN_REC:
            self.app_settings.set_min_on_record(set_on)
        elif var_tag == self.MENU_CHK_UPD:
            self.app_settings.set_check_for_upd(set_on)
            if set_on and not Version.check_version():
                self.sbar_msg(f"New Version Available: {Version.github_version}")
                return
        elif var_tag == self.MENU_ABOUT:
            About(self.pymacros_toplevel)
            return
        elif var_tag == self.MENU_MERGE:
            macro_merger = MacroMerger(self.root)
            results = macro_merger.show(self.get_macro_names(),self.selected_macro.name)

            if results:
                self.selected_macro.events.extend(results)
                self.save_selected_macro()
                self.setup_events()
            return
        elif var_tag == self.MENU_EVTS_PASTE:
            if MenuCommands.copied_events:
                self.selected_macro.add_event_list(MenuCommands.copied_events, MenuCommands.copied_offsets)
                self.btn_bold_on_modify(True)
                self.setup_events()
                self.sbar_msg(f"{len(MenuCommands.copied_events)} Events Pasted.")
            return
        elif var_tag == self.MENU_EVTS_COPY:
            MenuCommands.copied_events = copy.deepcopy(self.selected_macro.events)
            MenuCommands.copied_offsets = (
                self.selected_macro.global_mouse_offset_x,
                self.selected_macro.global_mouse_offset_y
                )
            self.sbar_msg(f"{len(MenuCommands.copied_events)} Events Copied.")
            return
        else:
            return

        self.sbar_msg(f"'{var_tag}' switched {'On' if set_on else 'Off'}")

    def setup_menus(self):
        sub_menu:tk.Menu = None
        menu_defs = {
            # Label,  Var_Tag, fn
            self.MENU_MIN_PLAY:     ('min_on_play',     self.app_settings.get_min_on_play       , self.main_win.sub_menu12),
            self.MENU_MIN_REC:      ('min_on_record',   self.app_settings.get_min_on_record     , self.main_win.sub_menu12),
            self.MENU_CHK_UPD:      ('Check_update',    self.app_settings.check_for_upd_enabled , self.main_win.sub_menu12),

            self.MENU_EVTS_COPY:    (None,None , self.main_win.sub_menu1),
            self.MENU_EVTS_PASTE:   (None,None , self.main_win.sub_menu1),

            self.MENU_ABOUT:        (None,None , self.main_win.sub_menu123),
            self.MENU_MERGE:        (None,None, self.main_win.sub_menu)
        }

        for lbl, values in menu_defs.items():
            var_tag, init_value_fn, sub_menu = values
            menu_idx = sub_menu.index(lbl)

            if var_tag :
                self.menu_setting_vars[var_tag] = tk.BooleanVar()
                sub_menu.entryconfig(menu_idx,variable=self.menu_setting_vars[var_tag],  command=lambda v=self.menu_setting_vars[var_tag], lbl=lbl : self.menu_callback(lbl,v) )
                self.menu_setting_vars[var_tag].set( init_value_fn() )
            else:
                sub_menu.entryconfig(menu_idx, command=lambda  lbl=lbl : self.menu_callback(lbl))
