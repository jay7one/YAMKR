import inspect
#import time
import tkinter as tk

from page.PyMouseMacro import PyMouseMacros,TLDialog
from app_data.macro_manager import MacroManager
from app_data.app_settings import AppSettings
from macros import Macro
from macros.macro import MacroEvent, MACRO_EXT#,EventType
from helpers.mouse_click import MouseClick
from helpers.hot_key import HotKey
from helpers.file_explorer import FileExplorer
from windows.new_macro_dialog import NewMacroDialog
from windows.popup_dialog import PopupDialog
from windows.tab_order_manager import TabOrderManager
from windows.event_widget import EventWidget
from windows.tkinter_helper import TkinterHelper

class AppBridge(TkinterHelper):
    root=None
    pymacros_toplevel, pymacros_win = None,None
    dialog_toplevel, dialog_win = None,None
    app_bridge = None

    menu_setting_vars = {}

    def __init__(self, main_win:PyMouseMacros, dialog_win:TLDialog) -> None:
        super().__init__()
        self.main_win = main_win
        self.dialog_win = dialog_win

        self.app_settings = AppSettings()
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

        saved_geo = self.app_settings.get_main_geo()
        print(f"debug {saved_geo=}")
        self.set_window_geo(self.root,saved_geo)
        #self.pymacros_toplevel.geometry(saved_geo)
        #self.root.geometry(saved_geo)

        self.root.resizable(0,0)
        self.root.deiconify()

        sl_size = len(self.macro_manager.get_macro_list())

        if sl_size > 0:
            self.main_win.SLBoxMacroList.index(0)
            self.main_win.SLBoxMacroList.select_set(0) #This only sets focus on the first item.
            self.main_win.SLBoxMacroList.event_generate("<<ListboxSelect>>")

        self.menu_setting_vars['min_on_play'] = tk.BooleanVar()
        self.menu_setting_vars['min_on_record'] = tk.BooleanVar()

    def additional_settings(self):
        self.main_win.SLBoxMacroList.configure(selectforeground="darkblue")
        self.main_win.SLBoxMacroList.configure(selectbackground="lightcyan")

    def load_macro_list(self, refresh=False):
        self.main_win.SLBoxMacroList.delete(0,tk.END)

        for idx, macro_name in enumerate(self.macro_manager.get_macro_names(refresh)):
            #print(f"Adding {macro_name}")
            self.main_win.SLBoxMacroList.insert(idx,macro_name)

    def config_event(self,event):   # pylint: disable=unused-argument
        self.app_settings.set_main_geo(self.get_window_geo(self.root))


    def get_menu_idx(self, lbl):
        menu_idx = self.main_win.menubar.index(lbl)
        return menu_idx

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


        # Menu settings button
        #self.menu_setting_vars['min_on_play'] = tk.BooleanVar(self.app_settings.get_min_on_play())
        #self.menu_setting_vars['min_on_record'] = tk.BooleanVar(self.app_settings.get_min_on_record())
        #self.main_win.menubar.add_command(label="On Play", variable=self.menu_setting_vars['min_on_play'], command=lambda min_on=self.menu_setting_vars['min_on_play'] : self.menu_min_play(min_on))
        #self.main_win.menubar.add_command(label="On Record", variable=self.menu_setting_vars['min_on_record'], command=lambda min_on=self.menu_setting_vars['min_on_record'] : self.menu_min_record(min_on))

    def add_callbacks(self,main_win:PyMouseMacros):

        main_win.SLBoxMacroList.bind("<<ListboxSelect>>", self.macro_list_callback)
        self.root.bind("<Configure>",self.config_event)


        self.setup_menus()

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
        self.load_selected_macro(macro_name)

    def load_selected_macro(self, macro_name):
        self.selected_macro = self.macro_manager.load_macro(macro_name)
        self.update_macro_screen()
        self.sbar_msg(f"Loaded macro: {self.selected_macro.name}")

    def set_entry_text(self, tk_entry:tk.Entry,text):
        tk_entry.delete(0,tk.END)
        tk_entry.insert(0,text)
        return

    def update_macro_screen(self):

        macro = self.selected_macro

        self.BtCmdKeyIntvState(self.main_win.BtnKPressIntv)
        self.BtCmdRelDelayState(self.main_win.BtnPostRelIntv)

        self.entry_toggle(self.main_win.EntryMPressIntv, True)
        self.entry_toggle(self.main_win.EntryKPressIntv, True)
        self.entry_toggle(self.main_win.EntryRelDelay, True)

        self.main_win.LbHotKeyText['text'] = macro.hotkey

        self.set_entry_text(self.main_win.EntryRepeat, macro.global_repeat)

        self.set_entry_text(self.main_win.EntryKPressIntv, f"{macro.global_keypress_interval}")
        self.set_entry_text(self.main_win.EntryMPressIntv, f"{macro.global_mousepress_interval}")
        self.set_entry_text(self.main_win.EntryRelDelay, f"{macro.global_release_interval}")

        self.button_toggle(self.main_win.BtnMoveMouse,  macro.global_mouse_movement)

        self.BtCmdMouseIntvState(self.main_win.BtnMPressIntv)
        self.BtCmdKeyIntvState(self.main_win.BtnKPressIntv)
        self.BtCmdRelDelayState(self.main_win.BtnPostRelIntv)
        self.BtCmdRepeatState()

        self.set_mouse_offset(macro)
        self.setup_events(macro.events)

    def get_entry_int(self, entry:tk.Entry):
        text = entry.get()
        print(f"Entry {text=}")
        if text == "" : return 0
        return int(text)

    def mouse_offset(self):
        txtstr = self.main_win.LabelOffset['text']
        parts = txtstr[1:len(txtstr)-1].split(",")
        return int(parts[0]), int(parts[1])

    def save_selected_macro(self):
        macro = self.selected_macro
        macro.hotkey = self.main_win.LbHotKeyText['text']
        macro.global_repeat = int(self.main_win.EntryRepeat.get())
        macro.global_keypress_interval = self.get_entry_int(self.main_win.EntryKPressIntv)
        macro.global_mousepress_interval = self.get_entry_int(self.main_win.EntryMPressIntv)
        macro.global_mouse_movement = self.button_state(self.main_win.BtnMoveMouse)
        macro.global_mousepress_interval_on = self.button_state(self.main_win.BtnMPressIntv)
        macro.global_keypress_interval_on = self.button_state(self.main_win.BtnKPressIntv)
        macro.global_release_interval_on = self.button_state(self.main_win.BtnPostRelIntv)
        macro.global_mouse_offset_x , macro.global_mouse_offset_y = self.mouse_offset()
        self.macro_manager.save_macro(macro)
        self.sbar_msg(f"Saved macro: {self.selected_macro.name}")

    def set_mouse_offset(self, macro):
        offset_text = f"{macro.global_mouse_offset_x,macro.global_mouse_offset_y}"
        self.main_win.LabelOffset.configure(text=offset_text, anchor="center")

    def setup_events(self,macro_events:list[MacroEvent]):   # pylint: disable=unused-argument

        self.clear_evt_labels()
        canvas = self.main_win.SWinEvents

        if not self.selected_macro.events :
            return

        #max_label_length = 15 # max(len(evt.abv) for evt in self.selected_macro.events)
        #max_label_width = max_label_length * 8  # Adjust this multiplier based on font size and character width
        #canvas_width = canvas.winfo_width()
        #num_columns = max(1, canvas_width // max_label_width)
        num_columns= 4
        # num_rows = math.ceil(len(label_list) / num_columns)

        for i, evt in enumerate(self.selected_macro.events):
            row = i // num_columns
            col = i % num_columns
            #string = f"{string}"
            # print(f"label text :{string=}")
            #lfont = "Apple Color Emoji"
            #lfont = "Noto Color Emoji"
            lfont = "Lucid Console"
            label = EventWidget(canvas, evt, justify='left',font=(lfont, 12) )

            label.grid(row=row, column=col, sticky="w", padx=5, pady=5)


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
        self.sbar_msg(f"Cleared events for macro: {self.selected_macro.name}")


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

    # pylint: disable=unused-argument

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



    def BtCmdMacroAdd(self,*args):
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

    def macro_select(self,value):
        listbox = self.main_win.SLBoxMacroList
        items = listbox.get(0, tk.END)
        try:
            index = items.index(value)
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(index)
            listbox.see(index)  # Ensure the selected item is visible
        except ValueError:
            return None


    def BtCmdMacroDel(self,*args):
        if self.selected_macro is None:
            return
        confirmed = PopupDialog.popup(self.pymacros_toplevel,"Delete Macro",
                                   f"Confirm deletion of {self.selected_macro.name}.",enable_cancel=True)
        if confirmed:
            self.macro_manager.remove_macro(self.selected_macro.name)

        self.load_macro_list()

    def BtCmdFolder(self,*args):
        name = None
        if self.selected_macro: name = self.selected_macro.name+MACRO_EXT
        FileExplorer.open(self.macro_manager.macros_path,name)

    def BtCmdRefresh(self,*args):
        name = None if not self.selected_macro else self.selected_macro.name
        self.load_macro_list(refresh=True)
        if name: self.macro_select(name)

    def BtCmdRestore(self,*args):
        if not self.selected_macro:
            return
        self.load_selected_macro(self.selected_macro.name)

    def BtCmdSave(self,*args):
        if self.selected_macro:
            self.save_selected_macro()

    # TODO: Buttons

    def BtCmdPlay(self,*args):
        print(f"fn called:{inspect.currentframe().f_code.co_name} {args=}")

    def BtCmdRecord(self,*args):

        if not self.selected_macro: return
        self.button_down(self.main_win.BtnRecord)
        print(f"EC bef:{len(self.selected_macro.events)=}")
        self.selected_macro.record()
        print(f"EC aft:{len(self.selected_macro.events)=}")

        print("Loading events")
        self.setup_events(self.selected_macro.events)
        self.button_up(self.main_win.BtnRecord)

        # TODO: Disable frame and renable after recording


    # TODO: Funcion Key listener

    def get_text(self,entry_field):
        #return entry_field.get("1.0",'end-1c')
        return entry_field.get()

    def validate_repeat_callback(self,*args) -> bool:
        e = self.main_win.EntryRepeat
        p_str = self.get_text(e)
        if p_str == "" or p_str == "0":
            self.set_entry_text(e,"1")
        return True

    def sbar_msg(self,msg):
        self.main_win.LbStatusBar['text'] = msg
        #print(f"debug:{msg=}")

    @classmethod
    def main(cls):
        '''Main entry point for the application.'''

        cls.root = tk.Tk()
        cls.root.withdraw()

        cls.root.protocol( 'WM_DELETE_WINDOW' , cls.root.destroy)

        cls.pymacros_toplevel = cls.root #tk.Toplevel(cls.root)   #
        cls.pymacros_win = PyMouseMacros(cls.pymacros_toplevel)

        cls.dialog_toplevel = tk.Toplevel(cls.root)
        cls.dialog_win = TLDialog(cls.dialog_toplevel)
        cls.dialog_toplevel.withdraw()

        cls.pymacros_toplevel.update()

        cls.app_bridge = AppBridge(cls.pymacros_win,cls.dialog_win)
        cls.root.mainloop()

if __name__ == '__main__':
    AppBridge.main()
