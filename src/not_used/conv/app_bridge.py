import inspect
#import time
import tkinter as tk

from page.PyMouseMacro import PyMouseMacro,TLDialog
from app_data.macro_manager import MacroManager
from app_data.app_settings import AppSettings
from macros import Macro
from macros.macro import MacroEvent, MACRO_EXT#,EventType
from helpers.mouse_click import MouseClick
from helpers.hot_key import HotKey
from helpers.file_explorer import FileExplorer
from windows.new_macro_dialog import NewMacroDialog
from windows.popup_dialog import PopupDialog
from app_bridge_helpers.tab_order_manager import TabOrderManager
from app_bridge_helpers.event_widget import EventWidget
from app_bridge_helpers.tkinter_helper import TkinterHelper

class AppBridge(TkinterHelper):
    root=None
    pymacros_toplevel, pymacros_win = None,None
    dialog_toplevel, dialog_win = None,None
    app_bridge = None

    menu_setting_vars = {}

    def __init__(self, main_win:PyMouseMacro, dialog_win:TLDialog) -> None:
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

        self.main_win.frame_macro_evt_buttons.lift()
        self.main_win.lframe_macro_settings.lift()
        self.main_win.slbox_macro_list.lift()
        self.main_win.frame_macro_list_buttons.lift()

        saved_geo = self.app_settings.get_main_geo()
        self.set_window_geo(self.root,saved_geo)


        self.root.resizable(0,0)
        self.root.deiconify()

        sl_size = len(self.macro_manager.get_macro_list())

        if sl_size > 0:
            self.main_win.slbox_macro_list.index(0)
            self.main_win.slbox_macro_list.select_set(0) #This only sets focus on the first item.
            self.main_win.slbox_macro_list.event_generate("<<ListboxSelect>>")

        self.menu_setting_vars['min_on_play'] = tk.BooleanVar()
        self.menu_setting_vars['min_on_record'] = tk.BooleanVar()

    def additional_settings(self):
        self.main_win.slbox_macro_list.configure(selectforeground="darkblue")
        self.main_win.slbox_macro_list.configure(selectbackground="lightcyan")

    def load_macro_list(self, refresh=False):
        self.main_win.slbox_macro_list.delete(0,tk.END)

        for idx, macro_name in enumerate(self.macro_manager.get_macro_names(refresh)):
            #print(f"Adding {macro_name}")
            self.main_win.slbox_macro_list.insert(idx,macro_name)

    def config_event(self,event):   # pylint: disable=unused-argument
        self.app_settings.set_main_geo(self.get_window_geo(self.root))

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

    def add_callbacks(self,main_win:PyMouseMacro):

        main_win.slbox_macro_list.bind("<<ListboxSelect>>", self.macro_list_callback)
        self.root.bind("<Configure>",self.config_event)


        self.setup_menus()

        # Macro settings buttons
        self.main_win.btn_move_mouse.       config(command=lambda b=self.main_win.btn_move_mouse        :self.btn_cmd_move_mouse(b))
        self.main_win.btn_offset.           config(command=lambda b=self.main_win.btn_offset            :self.btn_cmd_mouse_offset(b))
        self.main_win.btn_key_press_intv.   config(command=lambda b=self.main_win.btn_key_press_intv    :self.btn_cmd_key_intv(b))
        self.main_win.btn_mouse_press_intv. config(command=lambda b=self.main_win.btn_mouse_press_intv  :self.btn_cmd_mouse_intv(b))
        self.main_win.btn_post_rel_intv.    config(command=lambda b=self.main_win.btn_post_rel_intv     :self.btn_cmd_rel_delay(b))
        self.main_win.btn_hotkey_add.       config(command=lambda b=self.main_win.btn_hotkey_add        :self.btn_cmd_hotkey_add(b))
        self.main_win.btn_hotkey_del.       config(command=lambda b=self.main_win.btn_hotkey_del        :self.btn_cmd_hotkey_del(b))
        self.main_win.btn_add_macro.        config(command=lambda b=self.main_win.btn_add_macro         :self.btn_cmd_macro_add(b))
        self.main_win.btn_del_macro.        config(command=lambda b=self.main_win.btn_del_macro         :self.btn_cmd_macro_del(b))

        self.main_win.btn_play.config(command=self.btn_cmd_play)

        self.main_win.btn_refresh.config(command=self.btn_cmd_refresh)
        self.main_win.btn_folder.config(command=self.btn_cmd_folder)

        self.main_win.btn_record.config(command=self.btn_cmd_record)
        self.main_win.btn_save.config(command=self.btn_cmd_save)
        self.main_win.btn_clear.config(command=self.btn_cmd_clear)
        self.main_win.btn_restore.config(command=self.btn_cmd_restore)

        self.main_win.btn_repeat.config(command=self.btn_cmd_repeat)

        self.setup_numeric_entry()

        self.set_entry_text(self.main_win.entry_repeat,"1")

    def setup_numeric_entry(self):
        entry_widgets = [
            self.main_win.entry_rel_delay,
            self.main_win.entry_m_press_intv,
            self.main_win.entry_k_press_intv,
            self.main_win.entry_repeat
            ]

        for ew in entry_widgets:
            vcmd = ew.register(self.validate_number)
            ew.config(validate="key", validatecommand=(vcmd, '%P'))

        vcmd = self.main_win.entry_repeat.register(self.validate_repeat_callback)
        self.main_win.entry_repeat.config(validate='focusout', validatecommand=(vcmd, '%P'))


    def macro_list_callback(self, event):
        selection = event.widget.curselection()
        if not selection: return
        index = selection[0]
        macro_name =  event.widget.get(index)
        self.main_win.swin_events.delete("all")
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

        self.btn_cmd_key_intv_state(self.main_win.btn_key_press_intv)
        self.btn_cmd_rel_delayState(self.main_win.btn_post_rel_intv)

        self.entry_toggle(self.main_win.entry_m_press_intv, True)
        self.entry_toggle(self.main_win.entry_k_press_intv, True)
        self.entry_toggle(self.main_win.entry_rel_delay, True)

        self.main_win.lb_hotkey_text['text'] = macro.hotkey

        self.set_entry_text(self.main_win.entry_repeat, macro.global_repeat)

        self.set_entry_text(self.main_win.entry_k_press_intv, f"{macro.global_keypress_interval}")
        self.set_entry_text(self.main_win.entry_m_press_intv, f"{macro.global_mousepress_interval}")
        self.set_entry_text(self.main_win.entry_rel_delay, f"{macro.global_release_interval}")

        self.button_toggle(self.main_win.btn_move_mouse,  macro.global_mouse_movement)

        self.btn_cmd_mouse_intv_state(self.main_win.btn_mouse_press_intv)
        self.btn_cmd_key_intv_state(self.main_win.btn_key_press_intv)
        self.btn_cmd_rel_delayState(self.main_win.btn_post_rel_intv)
        self.btn_cmd_repeatState()

        self.set_mouse_offset(macro)
        self.setup_events(macro.events)

    def get_entry_int(self, entry:tk.Entry):
        text = entry.get()
        print(f"Entry {text=}")
        if text == "" : return 0
        return int(text)

    def mouse_offset(self):
        txtstr = self.main_win.label_offset['text']
        parts = txtstr[1:len(txtstr)-1].split(",")
        return int(parts[0]), int(parts[1])

    def save_selected_macro(self):
        macro = self.selected_macro
        macro.hotkey = self.main_win.lb_hotkey_text['text']
        macro.global_repeat = int(self.main_win.entry_repeat.get())
        macro.global_keypress_interval = self.get_entry_int(self.main_win.entry_k_press_intv)
        macro.global_mousepress_interval = self.get_entry_int(self.main_win.entry_m_press_intv)
        macro.global_mouse_movement = self.button_state(self.main_win.btn_move_mouse)
        macro.global_mousepress_interval_on = self.button_state(self.main_win.btn_mouse_press_intv)
        macro.global_keypress_interval_on = self.button_state(self.main_win.btn_key_press_intv)
        macro.global_release_interval_on = self.button_state(self.main_win.btn_post_rel_intv)
        macro.global_mouse_offset_x , macro.global_mouse_offset_y = self.mouse_offset()
        self.macro_manager.save_macro(macro)
        self.sbar_msg(f"Saved macro: {self.selected_macro.name}")

    def setup_events(self,macro_events:list[MacroEvent]):   # pylint: disable=unused-argument

        self.clear_evt_labels()
        canvas = self.main_win.swin_events

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

    def macro_select(self,value):
        listbox = self.main_win.slbox_macro_list
        items = listbox.get(0, tk.END)
        try:
            index = items.index(value)
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(index)
            listbox.see(index)  # Ensure the selected item is visible
        except ValueError:
            return None


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

    # TODO: Buttons

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

        # TODO: Disable frame and renable after recording


    # TODO: Funcion Key listener

    def get_text(self,entry_field):
        #return entry_field.get("1.0",'end-1c')
        return entry_field.get()

    def validate_repeat_callback(self,*args) -> bool:
        e = self.main_win.entry_repeat
        p_str = self.get_text(e)
        if p_str == "" or p_str == "0":
            self.set_entry_text(e,"1")
        return True

    def sbar_msg(self,msg):
        self.main_win.lb_status_bar['text'] = msg
        #print(f"debug:{msg=}")

    @classmethod
    def main(cls):
        '''Main entry point for the application.'''

        cls.root = tk.Tk()
        cls.root.withdraw()

        cls.root.protocol( 'WM_DELETE_WINDOW' , cls.root.destroy)

        cls.pymacros_toplevel = cls.root #tk.Toplevel(cls.root)   #
        cls.pymacros_win = PyMouseMacro(cls.pymacros_toplevel)

        cls.dialog_toplevel = tk.Toplevel(cls.root)
        cls.dialog_win = TLDialog(cls.dialog_toplevel)
        cls.dialog_toplevel.withdraw()

        cls.pymacros_toplevel.update()

        cls.app_bridge = AppBridge(cls.pymacros_win,cls.dialog_win)
        cls.root.mainloop()

if __name__ == '__main__':
    AppBridge.main()