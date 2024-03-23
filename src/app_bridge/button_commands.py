from abc import ABC, abstractmethod
import tkinter as tk

from app_bridge.app_bridge_base import AppBridgeBase

from macros.macro import MacroEvent, MACRO_EXT, EventType
from macros.macro_data import MacroData
from helpers.mouse_click import MouseClick
from helpers.file_explorer import FileExplorer
from helpers.hot_key_helper import HotKeyHelper
from windows.macro_dialog import MacroDialog
from windows.popup_dialog import PopupDialog
from windows.tkinter_helper import TkinterHelper as tkh

class ButtonCommands(ABC, AppBridgeBase):

    def set_mouse_offset(self, macro):
        offset_text = f"{macro.global_mouse_offset_x,macro.global_mouse_offset_y}"
        self.main_win.label_offset.configure(text=offset_text, anchor="center")

    def entry_toggle(self, entry:tk.Entry, enable:bool):
        new_state = 'normal' if enable else 'disabled'
        entry.config(state=new_state)

    def clear_evt_labels(self):
        self.last_evt_clicked = None
        self.set_delay_upd_bt()

        tkh.clear_frame(self.main_win.swin_events_f)

        #self.main_win.swin_events.delete("all")
        #for l in self.main_win.swin_events_f.children.values():
        #    l.grid_forget()


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
        tkh.button_toggle(button,self.selected_macro.global_keypress_interval_on)
        self.entry_toggle(self.main_win.entry_k_press_intv, self.selected_macro.global_keypress_interval_on)

    def btn_cmd_mouse_intv(self,button:tk.Button):
        if self.selected_macro is None: return
        self.selected_macro.global_mousepress_interval_on = not self.selected_macro.global_mousepress_interval_on
        self.btn_cmd_mouse_intv_state(button)

    def btn_cmd_mouse_intv_state(self,button:tk.Button):
        tkh.button_toggle(button,self.selected_macro.global_mousepress_interval_on)
        self.entry_toggle(self.main_win.entry_m_press_intv, self.selected_macro.global_mousepress_interval_on)

    def btn_cmd_rel_delay(self,button:tk.Button):
        if self.selected_macro is None: return
        self.selected_macro.global_release_interval_on = not self.selected_macro.global_release_interval_on
        self.btn_cmd_rel_delayState(button)

    def btn_cmd_rel_delayState(self,button:tk.Button):
        tkh.button_toggle(button,self.selected_macro.global_release_interval_on)
        self.entry_toggle(self.main_win.entry_rel_delay, self.selected_macro.global_release_interval_on)

    def btn_bold_on_modify(self, modified:bool):

        if self.app_settings.get_autosave():
            self.save_selected_macro()
            modified=False

        for btn in [self.main_win.btn_save, self.main_win.btn_restore]:
            if modified:
                btn.config(foreground='red')
            else:
                btn.config(foreground='black')


    # pylint: disable=unused-argument

    def btn_cmd_repeat(self,*args):
        if self.selected_macro is None: return
        self.selected_macro.global_repeat += 1
        self.btn_cmd_repeatState()

    def btn_cmd_repeatState(self):
        if self.selected_macro is None: return
        if self.selected_macro.global_repeat < 1 :
            self.selected_macro.global_repeat = 1
        tkh.set_entry_text(self.main_win.entry_repeat,self.selected_macro.global_repeat)

    def btn_cmd_mouse_offset(self,button:tk.Button):
        if self.selected_macro is None: return
        tkh.button_down(button)
        self.selected_macro.global_mouse_offset_x,self.selected_macro.global_mouse_offset_y = MouseClick.get_next_click()
        tkh.button_up(button)
        self.set_mouse_offset(self.selected_macro)

    def btn_cmd_move_mouse(self,button:tk.Button):
        if self.selected_macro is None: return
        self.selected_macro.global_mouse_movement = not self.selected_macro.global_mouse_movement
        tkh.button_toggle(button,self.selected_macro.global_mouse_movement)

    def btn_cmd_hotkey_del(self,*args):
        if self.selected_macro is None: return
        self.selected_macro.assign_hotkey("")
        self.main_win.lb_hotkey_text['text']=""
        self.btn_bold_on_modify(True)

    def btn_cmd_hotkey_add(self,button:tk.Button):
        if self.selected_macro is None: return

        HotKeyHelper.add_hotkey(
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
        self.root.bind("<Key>", self.check_for_hotkey )
        self.btn_bold_on_modify(True)

    def btn_cmd_macro_add(self,*args):
        name, hotkey = MacroDialog.show(self.root)
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
            prev_macro_name,idx = self.get_prev_macro(self.selected_macro.name)
            self.macro_manager.remove_macro(self.selected_macro.name)
            self.load_macro_list()
            if prev_macro_name:
                self.select_load_macro(prev_macro_name)
                #self.main_win.slbox_macro_list.index(idx)
                self.main_win.slbox_macro_list.see(idx)
                self.main_win.slbox_macro_list.select_set(idx) #This only sets focus on the first item.
                self.main_win.slbox_macro_list.event_generate("<<ListboxSelect>>")

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
        self.select_load_macro(self.selected_macro.name)

    def btn_cmd_save(self,*args):
        if self.selected_macro:
            self.save_selected_macro()
        self.btn_bold_on_modify(False)

    def btn_cmd_play(self,*args):
        if not self.selected_macro: return
        tkh.button_down(self.main_win.btn_play)

        if self.app_settings.get_min_on_play() :
            self.root.withdraw()

        self.selected_macro.play(self.sub_player)

        if self.app_settings.get_min_on_play() :
            self.root.deiconify()

        tkh.button_up(self.main_win.btn_play)

    @abstractmethod
    def sub_player(self,macro_name:str) -> tuple[MacroEvent, MacroData]:
        pass

    def btn_cmd_record(self,*args):
        if not self.selected_macro: return
        tkh.button_down(self.main_win.btn_record)

        if self.app_settings.get_min_on_record() :
            self.root.withdraw()

        self.selected_macro.record()

        if self.app_settings.get_min_on_record() :
            self.root.deiconify()

        self.setup_events()
        tkh.button_up(self.main_win.btn_record)
        self.btn_bold_on_modify(True)

    def btn_cmd_rename(self,*args):
        if not self.selected_macro: return
        new_name, _ = MacroDialog.show(self.root, "Rename Macro", self.selected_macro.name,self.selected_macro.hotkey)
        if not new_name : return
        self.macro_manager.rename_macro(self.selected_macro,new_name)
        self.load_macro_list()
        self.macro_select(new_name)

    def btn_cmd_delay_update(self,*args):
        if not self.selected_macro: return
        evt_val = tkh.get_entry_int(self.main_win.entry_delay_edit)
        if evt_val == 0 : return

        new_evt = self.last_evt_clicked
        if self.last_evt_clicked is None:
            new_evt = MacroEvent(EventType.DELAY, evt_val)
            self.selected_macro.add_event_list([new_evt])
            self.sbar_msg("Delay Event Added.")
            self.setup_events()
        else:
            self.last_evt_clicked.event.event_value = evt_val
            self.last_evt_clicked.draw()
            self.sbar_msg("Delay event updated.")

        self.btn_bold_on_modify(True)
