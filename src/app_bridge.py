#import sys
#import math
import tkinter as tk

import inspect

from page.PyMouseMacro import PyMouseMacros,TLDialog
from app_data.macro_manager import MacroManager
from macros import Macro
from macros.macro import MacroEvent #,EventType
from helpers.mouse_click import MouseClick
from helpers.hot_key import HotKey
from windows.tab_order_manager import TabOrderManager

class AppBridge:
    root=None
    pymacros_toplevel, pymacros_win = None,None
    dialog_toplevel, dialog_win = None,None
    app_bridge = None

    def __init__(self, main_win:PyMouseMacros, dialog_win:TLDialog) -> None:

        self.main_win = main_win
        self.dialog_win = dialog_win
        self.macro_manager = MacroManager()

        self.add_callbacks(main_win)
        self.load_macro_list()

        self.selected_macro:Macro = None

        self.additional_settings()

        TabOrderManager.set_tab_order(self.main_win.top)

        self.main_win.FrameMacroEvtButtons.lift()
        self.main_win.LFrameMacroSettings.lift()
        self.main_win.SLBoxMacroList.lift()
        self.main_win.FrameMacroListButtons.lift()

    def additional_settings(self):
        self.main_win.SLBoxMacroList.configure(selectforeground="darkblue")
        self.main_win.SLBoxMacroList.configure(selectbackground="lightcyan")

    def load_macro_list(self):
        for idx, macro in enumerate(self.macro_manager.get_macro_names()):
            self.main_win.SLBoxMacroList.insert(idx,macro)

    def load_events_by_name(self,macro_name):
        self.selected_macro = self.macro_manager.load_macro(macro_name)
        self.load_events()

    def load_events(self):
        self.BtCmdClear()
        for e in self.selected_macro.events:
            print(f"Event:{e}")


    def add_callbacks(self,main_win:PyMouseMacros):
        main_win.SLBoxMacroList.bind("<<ListboxSelect>>", self.macro_list_callback)

        # Macro settings buttons
        self.main_win.BtnMoveMouse.     config(command=lambda b=self.main_win.BtnMoveMouse   :self.BtCmdMoveMouse(b))
        self.main_win.BtnOffset.        config(command=lambda b=self.main_win.BtnOffset      :self.BtCmdMouseOffset(b))
        self.main_win.BtnKPressIntv.    config(command=lambda b=self.main_win.BtnKPressIntv  :self.BtCmdKeyIntv(b))
        self.main_win.BtnMPressIntv.    config(command=lambda b=self.main_win.BtnMPressIntv  :self.BtCmdMouseIntv(b))
        self.main_win.BtnPostRelIntv.   config(command=lambda b=self.main_win.BtnPostRelIntv :self.BtCmdRelDelay(b))
        self.main_win.BtnHotKeyAdd.     config(command=lambda b=self.main_win.BtnHotKeyAdd   :self.BtCmdHotkeyAdd(b))
        self.main_win.BtnHotKeyDel.     config(command=lambda b=self.main_win.BtnHotKeyDel   :self.BtCmdHotkeyDel(b))
        self.main_win.BtnAddMacro.      config(command=lambda b=self.main_win.BtnAddMacro    :self.BtCmdMacroAdd(b))
        self.main_win.BtnDelMacro.      config(command=lambda b=self.main_win.BtnDelMacro    :self.BtCmdMacroDel(b))

        self.main_win.BtnPlay.config(command=self.BtCmdPlay)

        self.main_win.BtnRefresh.config(command=self.BtCmdRefresh)
        self.main_win.BtnFolder.config(command=self.BtCmdFolder)

        self.main_win.BtnRecord.config(command=self.BtCmdRecord)
        self.main_win.BtnSave.config(command=self.BtCmdSave)
        self.main_win.BtnClear.config(command=self.BtCmdClear)
        self.main_win.BtnRestore.config(command=self.BtCmdRestore)

        self.main_win.BtnRepeat.config(command=self.BtCmdRepeat)

        self.setup_numeric_entry()

        self.set_entry_text(self.main_win.EntryRepeat,"1")

    def setup_numeric_entry(self):
        entry_widgets = [
            self.main_win.EntryRelDelay,
            self.main_win.EntryMPressIntv,
            self.main_win.EntryKPressIntv,
            self.main_win.EntryRepeat
            ]

        for ew in entry_widgets:
            vcmd = ew.register(self.validate_number)
            ew.config(validate="key", validatecommand=(vcmd, '%P'))

        vcmd = self.main_win.EntryRepeat.register(self.validate_repeat_callback)
        self.main_win.EntryRepeat.config(validate='focusout', validatecommand=(vcmd, '%P'))


    def macro_list_callback(self, event):
        selection = event.widget.curselection()
        if not selection: return
        index = selection[0]
        macro_name =  event.widget.get(index)
        self.main_win.SWinEvents.delete("all")
        self.selected_macro = self.macro_manager.load_macro(macro_name)
        self.update_macro_screen()

    def update_macro_screen(self):

        macro = self.selected_macro

        self.main_win.LbHotKeyText['text'] = macro.hotkey

        self.set_entry_text(self.main_win.EntryRepeat, macro.global_repeat)
        self.set_entry_text(self.main_win.EntryKPressIntv, str(macro.global_keypress_interval))
        self.set_entry_text(self.main_win.EntryMPressIntv, str(macro.global_mousepress_interval))


        self.button_toggle(self.main_win.BtnMoveMouse,  macro.global_mouse_movement)

        self.BtCmdMouseIntvState(self.main_win.BtnMPressIntv)
        self.BtCmdKeyIntvState(self.main_win.BtnKPressIntv)
        self.BtCmdRelDelayState(self.main_win.BtnPostRelIntv)
        self.BtCmdRepeatState()

        self.set_mouse_offset(macro)
        self.setup_events(macro.events)

    def set_mouse_offset(self, macro):
        offset_text = f"{macro.global_mouse_offset_x,macro.global_mouse_offset_y}"
        self.main_win.LabelOffset.configure(text=offset_text, anchor="center")

    def setup_events(self,macro_events:list[MacroEvent]):
        label_list = []
        for e in macro_events:
            abv_txt = e.abv()
            #print(f"abv :{(e.event_type,e.event_value)=} = {abv_txt=}")
            label_list.append(abv_txt)

        canvas = self.main_win.SWinEvents

        self.clear_evt_labels()

        max_label_length = max(len(string) for string in label_list)
        max_label_width = max_label_length * 8  # Adjust this multiplier based on font size and character width
        canvas_width = canvas.winfo_width()
        num_columns = max(1, canvas_width // max_label_width)
        num_columns=6
        # num_rows = math.ceil(len(label_list) / num_columns)

        for i, string in enumerate(label_list):
            row = i // num_columns
            col = i % num_columns
            string = f"{string}"
            # print(f"label text :{string=}")
            label = tk.Label(canvas, text=string, justify='center',font=("Arial", 8) )
            label.grid(row=row, column=col, sticky="w", padx=5, pady=5)


    def button_down(self, button):          button.config(relief=tk.SUNKEN)
    def button_up(self, button):            button.config(relief=tk.RAISED)
    def button_toggle(self, button, down):  button.config(relief=tk.SUNKEN if down else tk.RAISED)

    def entry_toggle(self, entry:tk.Entry, enable):
        new_state = 'normal' if enable else 'disabled'
        entry.config(state=new_state)

    def clear_evt_labels(self):
        #self.main_win.SWinEvents.delete("all")
        for l in self.main_win.SWinEvents.children.values():
            l.grid_forget()

    def BtCmdClear(self):
        if not self.selected_macro:
            return
        self.clear_evt_labels()
        self.macro_manager.clear_macro(self.selected_macro)

    def BtCmdKeyIntv(self,button):
        if self.selected_macro is None: return
        self.selected_macro.global_keypress_interval_on = not self.selected_macro.global_keypress_interval_on
        self.BtCmdKeyIntvState(button)

    def BtCmdKeyIntvState(self,button):
        self.button_toggle(button,self.selected_macro.global_keypress_interval_on)
        self.entry_toggle(self.main_win.EntryKPressIntv, self.selected_macro.global_keypress_interval_on)

    def BtCmdMouseIntv(self,button):
        if self.selected_macro is None: return
        self.selected_macro.global_mousepress_interval_on = not self.selected_macro.global_mousepress_interval_on
        self.BtCmdMouseIntvState(button)

    def BtCmdMouseIntvState(self,button):
        self.button_toggle(button,self.selected_macro.global_mousepress_interval_on)
        self.entry_toggle(self.main_win.EntryMPressIntv, self.selected_macro.global_mousepress_interval_on)

    def BtCmdRelDelay(self,button):
        if self.selected_macro is None: return
        self.selected_macro.global_release_interval_on = not self.selected_macro.global_release_interval_on
        self.BtCmdRelDelayState(button)

    def BtCmdRelDelayState(self,button):
        self.button_toggle(button,self.selected_macro.global_release_interval_on)
        self.entry_toggle(self.main_win.EntryRelDelay, self.selected_macro.global_release_interval_on)

    def BtCmdRepeat(self,*args):
        if self.selected_macro is None: return
        self.selected_macro.global_repeat += 1
        self.BtCmdRepeatState()

    def BtCmdRepeatState(self):
        if self.selected_macro is None: return
        if self.selected_macro.global_repeat < 1 :
            self.selected_macro.global_repeat = 1
        self.set_entry_text(self.main_win.EntryRepeat,self.selected_macro.global_repeat)

    def BtCmdMouseOffset(self,button):
        if self.selected_macro is None: return
        self.button_down(button)
        self.selected_macro.global_mouse_offset_x,self.selected_macro.global_mouse_offset_y = MouseClick.get_next_click()
        self.button_up(button)
        self.set_mouse_offset(self.selected_macro)

    def BtCmdMoveMouse(self,button):
        if self.selected_macro is None: return
        self.selected_macro.global_mouse_movement = not self.selected_macro.global_mouse_movement
        self.button_toggle(button,self.selected_macro.global_mouse_movement)

    def BtCmdHotkeyDel(self,*args):
        if self.selected_macro is None: return
        self.selected_macro.assign_hotkey("")
        self.main_win.LbHotKeyText['text']=""

    # TODO: Buttons

    def BtCmdHotkeyAdd(self,button):
        if self.selected_macro is None: return
        HotKey.add_hotkey(
            self.root,
            self.main_win.LbHotKeyText,
            self.main_win.BtnHotKeyAdd,
            self.set_hotkey_callback
            )

    def set_hotkey_callback(self):
        new_hotkey = self.main_win.LbHotKeyText['text']
        if new_hotkey == "":
            new_hotkey = self.selected_macro.hotkey
        else:
            self.selected_macro.hotkey = new_hotkey

        self.main_win.LbHotKeyText['text'] = self.selected_macro.hotkey

    def BtCmdMacroAdd(self,*args):      print(f"fn called:{inspect.currentframe().f_code.co_name} {args=}")
    def BtCmdMacroDel(self,*args):      print(f"fn called:{inspect.currentframe().f_code.co_name} {args=}")
    def BtCmdFolder(self,*args):        print(f"fn called:{inspect.currentframe().f_code.co_name} {args=}")
    def BtCmdRefresh(self,*args):       print(f"fn called:{inspect.currentframe().f_code.co_name} {args=}")

    def BtCmdPlay(self,*args):          print(f"fn called:{inspect.currentframe().f_code.co_name} {args=}")
    def BtCmdRestore(self,*args):       print(f"fn called:{inspect.currentframe().f_code.co_name} {args=}")
    def BtCmdSave(self,*args):          print(f"fn called:{inspect.currentframe().f_code.co_name} {args=}")
    def BtCmdRecord(self,*args):
        # TODO: Disable frame and renable after recording
        print(f"fn called:{inspect.currentframe().f_code.co_name} {args=}")

    def get_text(self,entry_field):
        #return entry_field.get("1.0",'end-1c')
        return entry_field.get()

    def validate_repeat_callback(self,*args) -> bool:
        e = self.main_win.EntryRepeat
        p_str = self.get_text(e)
        if p_str == "" or p_str == "0":
            self.set_entry_text(e,"1")
        return True

    def validate_number(self,P) -> bool:
        #print(f"Validate {P=}")
        p_str = str(P)
        return p_str == '' or str.isdigit(p_str)

    def set_entry_text(self, tk_entry:tk.Entry,text):
        tk_entry.delete(0,tk.END)
        tk_entry.insert(0,text)
        return

    @classmethod
    def main(cls):
        '''Main entry point for the application.'''

        cls.root = tk.Tk()
        cls.root.protocol( 'WM_DELETE_WINDOW' , cls.root.destroy)

        cls.pymacros_toplevel = cls.root
        cls.pymacros_win = PyMouseMacros(cls.pymacros_toplevel)

        cls.dialog_toplevel = tk.Toplevel(cls.root)
        cls.dialog_win = TLDialog(cls.dialog_toplevel)
        cls.dialog_toplevel.withdraw()

        cls.pymacros_toplevel.update()

        cls.app_bridge = AppBridge(cls.pymacros_win,cls.dialog_win)
        cls.root.mainloop()

if __name__ == '__main__':
    AppBridge.main()
