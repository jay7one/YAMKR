import inspect
from abc import ABC, abstractmethod
import tkinter as tk

from app_bridge_helpers.app_bridge_base import AppBridgeBase

from macros.macro import MacroEvent, MACRO_EXT
from helpers.mouse_click import MouseClick
from helpers.hot_key import HotKey
from helpers.file_explorer import FileExplorer
from windows.new_macro_dialog import NewMacroDialog
from windows.popup_dialog import PopupDialog

class ButtonCommands(ABC, AppBridgeBase):

    def set_mouse_offset(self, macro):
        offset_text = f"{macro.global_mouse_offset_x,macro.global_mouse_offset_y}"
        self.main_win.label_offset.configure(text=offset_text, anchor="center")

    def entry_toggle(self, entry:tk.Entry, enable:bool):
        new_state = 'normal' if enable else 'disabled'
        entry.config(state=new_state)

    def clear_evt_labels(self):
        #self.main_win.swin_events.delete("all")
        for l in self.main_win.swin_events.children.values():
            l.grid_forget()

    def btn_cmd_clear(self):
        if not self.selected_macro:
            return
        self.clear_evt_labels()
        self.macro_manager.clear_macro(self.selected_macro)
        self.sbar_msg(f"Cleared events for macro: {self.selected_macro.name}")

    def btn_cmd_key_intv(self,button:tk.Button):
        if self.selected_macro is None: return
        self.selected_macro.global_keypress_interval_on = not self.selected_macro.global_keypress_interval_on
        self.btn_cmd_key_intv_state(button)

    def btn_cmd_key_intv_state(self,button:tk.Button):
        self.button_toggle(button,self.selected_macro.global_keypress_interval_on)
        self.entry_toggle(self.main_win.entry_k_press_intv, self.selected_macro.global_keypress_interval_on)

    def btn_cmd_mouse_intv(self,button:tk.Button):
        if self.selected_macro is None: return
        self.selected_macro.global_mousepress_interval_on = not self.selected_macro.global_mousepress_interval_on
        self.btn_cmd_mouse_intv_state(button)

    def btn_cmd_mouse_intv_state(self,button:tk.Button):
        self.button_toggle(button,self.selected_macro.global_mousepress_interval_on)
        self.entry_toggle(self.main_win.entry_m_press_intv, self.selected_macro.global_mousepress_interval_on)

    def btn_cmd_rel_delay(self,button:tk.Button):
        if self.selected_macro is None: return
        self.selected_macro.global_release_interval_on = not self.selected_macro.global_release_interval_on
        self.btn_cmd_rel_delayState(button)

    def btn_cmd_rel_delayState(self,button:tk.Button):
        self.button_toggle(button,self.selected_macro.global_release_interval_on)
        self.entry_toggle(self.main_win.entry_rel_delay, self.selected_macro.global_release_interval_on)

    # pylint: disable=unused-argument

    def btn_cmd_repeat(self,*args):
        if self.selected_macro is None: return
        self.selected_macro.global_repeat += 1
        self.btn_cmd_repeatState()

    def btn_cmd_repeatState(self):
        if self.selected_macro is None: return
        if self.selected_macro.global_repeat < 1 :
            self.selected_macro.global_repeat = 1
        self.set_entry_text(self.main_win.entry_repeat,self.selected_macro.global_repeat)

    def btn_cmd_mouse_offset(self,button:tk.Button):
        if self.selected_macro is None: return
        self.button_down(button)
        self.selected_macro.global_mouse_offset_x,self.selected_macro.global_mouse_offset_y = MouseClick.get_next_click()
        self.button_up(button)
        self.set_mouse_offset(self.selected_macro)

    def btn_cmd_move_mouse(self,button:tk.Button):
        if self.selected_macro is None: return
        self.selected_macro.global_mouse_movement = not self.selected_macro.global_mouse_movement
        self.button_toggle(button,self.selected_macro.global_mouse_movement)

    def btn_cmd_hotkey_del(self,*args):
        if self.selected_macro is None: return
        self.selected_macro.assign_hotkey("")
        self.main_win.lb_hotkey_text['text']=""

    def btn_cmd_hotkey_add(self,button:tk.Button):
        if self.selected_macro is None: return

        HotKey.add_hotkey(
            self.root,
            self.main_win.lb_hotkey_text,
            self.main_win.btn_hotkey_add,
            self.set_hotkey_callback
            )

    def set_hotkey_callback(self):
        new_hotkey = self.main_win.lb_hotkey_text['text']

        if new_hotkey == "":
            new_hotkey = self.selected_macro.hotkey
        else:
            self.selected_macro.hotkey = new_hotkey

        self.main_win.lb_hotkey_text['text'] = self.selected_macro.hotkey

    def btn_cmd_macro_add(self,*args):
        name, hotkey = NewMacroDialog.create_macro(self.root)
        if not name : return
        new_name = name
        #print(f"BtnAdd:{new_name=}")
        for i in range(1,999):
            if not self.macro_manager.macro_exists(new_name):
                break
            new_name = name + f"_{i}"

        self.macro_manager.new_macro(new_name,hotkey)
        self.load_macro_list()
        self.macro_select(new_name)

    def btn_cmd_macro_del(self,*args):
        if self.selected_macro is None:
            return
        confirmed = PopupDialog.popup(self.pymacros_toplevel,"Delete Macro",
                                   f"Confirm deletion of {self.selected_macro.name}.",enable_cancel=True)
        if confirmed:
            self.macro_manager.remove_macro(self.selected_macro.name)

        self.load_macro_list()

    def btn_cmd_folder(self,*args):
        name = None
        if self.selected_macro: name = self.selected_macro.name+MACRO_EXT
        FileExplorer.open(self.macro_manager.macros_path,name)

    def btn_cmd_refresh(self,*args):
        name = None if not self.selected_macro else self.selected_macro.name
        self.load_macro_list(refresh=True)
        if name: self.macro_select(name)

    def btn_cmd_restore(self,*args):
        if not self.selected_macro:
            return
        self.load_selected_macro(self.selected_macro.name)

    def btn_cmd_save(self,*args):
        if self.selected_macro:
            self.save_selected_macro()

    def btn_cmd_play(self,*args):
        print(f"fn called:{inspect.currentframe().f_code.co_name} {args=}")

    def btn_cmd_record(self,*args):

        if not self.selected_macro: return
        self.button_down(self.main_win.btn_record)

        if self.app_settings.get_min_on_record() :
            self.root.withdraw()

        self.selected_macro.record()

        if self.app_settings.get_min_on_record() :
            self.root.deiconify()

        self.setup_events(self.selected_macro.events)
        self.button_up(self.main_win.btn_record)


    @abstractmethod
    def load_macro_list(self, refresh=False):
        print("Fn : load_macro_list not overrriden")
    @abstractmethod
    def macro_select(self,macro_name:str):
        print("Fn : macro_select not overrriden")
    @abstractmethod
    def setup_events(self,macro_events:list[MacroEvent]):
        print("Fn : setup_events not overrriden")
    @abstractmethod
    def load_selected_macro(self, macro_name:str):
        print("Fn : load_selected_macro not overrriden")
