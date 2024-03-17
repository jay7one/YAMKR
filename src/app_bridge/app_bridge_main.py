import tkinter as tk

from page.PyMouseMacro import PyMouseMacro
from app_data.macro_manager import MacroManager
from app_data.app_settings import AppSettings
from macros import Macro
from app_bridge.event_widget import EventWidget
from app_bridge.button_commands import ButtonCommands
from app_bridge.menu_commands import MenuCommands
from windows.tkinter_helper import TkinterHelper as tkh
from helpers.version import Version

# TODO: Full list below:
# test hot key listener for F1-12 playback


# TODO: Low priority items
# Fonts and sizes in settings - low priority - may not do
# Work out way to suppress errors when mouse scrolling, window enter events are setting callback
# control-c/v for copy/paste
# Maybe have option in sub_macro to say abs/rel offsets used
# Convert Page to normal file ? - when ready , will needs to change call backs

# DONE
# Copy paste events - adjusting offsets
# Centre dialog boxes in macro window not screen centre
# Allow functions keys to be preseed when adding macro
# pressing enter on entry field should be click ok event
# Paste should be like record, have buttons in red.

class AppBridgeMain(ButtonCommands, MenuCommands):

    def __init__(self, main_win:PyMouseMacro) -> None:
        super().__init__()

        self.main_win = main_win

        self.app_settings = AppSettings()
        self.macro_manager = MacroManager()

        self.app_settings.set_version(Version.get_from_file())
        if self.app_settings.check_for_upd_enabled():
            if not Version.check_version():
                self.sbar_msg(f"New Version Available: {Version.github_version}")
            else:
                self.sbar_msg(f"Version:{Version.file_version}")

        self.add_callbacks(main_win)
        self.load_macro_list()

        self.selected_macro:Macro = None

        self.additional_settings()
        self.setup_button_icons()

        tkh.set_tab_order(self.main_win.top)

        self.main_win.frame_macro_evt_buttons.lift()
        self.main_win.lframe_macro_settings.lift()
        self.main_win.slbox_macro_list.lift()
        self.main_win.frame_macro_list_buttons.lift()

        self.main_geo = self.app_settings.get_main_geo()
        tkh.set_window_geo(self.root,self.main_geo)
        tkh.set_main_geo(self.main_win.top)

        self.menu_setting_vars['min_on_play'] = tk.BooleanVar()
        self.menu_setting_vars['min_on_record'] = tk.BooleanVar()


        self.root.resizable(0,0)
        self.root.deiconify()

        sl_size = len(self.macro_manager.get_macro_list())

        if sl_size > 0:
            self.main_win.slbox_macro_list.index(0)
            self.main_win.slbox_macro_list.select_set(0) #This only sets focus on the first item.
            self.main_win.slbox_macro_list.event_generate("<<ListboxSelect>>")

    def additional_settings(self):
        self.main_win.slbox_macro_list.configure(selectforeground="darkblue")
        self.main_win.slbox_macro_list.configure(selectbackground="lightcyan")

    def setup_button_icons(self):

        #font="-family {DejaVu Sans} -size 10"
        bt_font = r"-family {Lucid Console} -size "
        bt_size = 12
        btns = {
            'folder'  : (self.main_win.btn_folder,      '\U0001F4C2', 15, '... Open file explorer where macro resides '    ),
            'refresh' : (self.main_win.btn_refresh,     '\u27F3'    , 12,  '... Refresh macro list '  ),
            'rename'  : (self.main_win.btn_rename,      '\U0000270E', 16,  '... Rename selected macro'  ),
            'delete'  : (self.main_win.btn_del_macro,   '\U0000274C', 9,  '... Delete selected macro'  ),
            'add'     : (self.main_win.btn_add_macro,   '\U00002795', 9,  '... Create new macro'  ),

        }
        bt:tk.Button
        for _,v in btns.items():
            bt, txt, fsize, hover_t = v
            bt.config(text=txt)
            bt.config(font=bt_font + str(fsize) )
            bt.bind("<Enter>", lambda btn=bt, ht=hover_t    : self.set_button_sbar(None,ht) )
            bt.bind("<Leave>", lambda btn=bt, ht=''         : self.set_button_sbar(None,ht) )

    def set_button_sbar(self, _, txt):self.sbar_msg(txt)

    def load_macro_list(self, refresh=False):
        self.main_win.slbox_macro_list.delete(0,tk.END)
        cur_selection = None

        for idx, macro_name in enumerate(self.macro_manager.get_macro_names(refresh)):
            #print(f"Adding {macro_name}")
            self.main_win.slbox_macro_list.insert(idx,macro_name)
            if self.selected_macro and self.selected_macro.name == macro_name:
                cur_selection = macro_name

        if cur_selection:
            self.select_load_macro(cur_selection)
        else:
            self.selected_macro = None

    def get_macro_names(self, refresh=False):
        return self.macro_manager.get_macro_names(refresh)

    def config_event(self,event):   # pylint: disable=unused-argument
        if event.widget is self.root:
            self.app_settings.set_geo_settings(tkh.get_window_geo(self.root))
            self.main_geo = self.app_settings.get_main_geo()
            tkh.set_main_geo(self.main_win.top)

    def check_for_hotkey(self, event:tk.Event):
        hotkey = event.keysym
        if hotkey[0] == "F":
            macro_name = self.macro_manager.find_hotkey_macro(hotkey)
            if macro_name:
                self.select_load_macro(macro_name)
                self.main_win.btn_play.invoke()

        #print(f"debug {(event.keycode, event.keysym, event.char)=}")

    def add_callbacks(self,main_win:PyMouseMacro):

        main_win.slbox_macro_list.bind("<<ListboxSelect>>", self.macro_list_callback)
        self.root.bind("<Configure>",self.config_event)
        self.root.bind("<Key>", self.check_for_hotkey )

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
        self.main_win.btn_rename.           config(command=lambda b=self.main_win.btn_rename            :self.btn_cmd_rename(b))

        self.main_win.btn_play.config(command=self.btn_cmd_play)

        self.main_win.btn_refresh.config(command=self.btn_cmd_refresh)
        self.main_win.btn_folder.config(command=self.btn_cmd_folder)

        self.main_win.btn_record.config(command=self.btn_cmd_record)
        self.main_win.btn_save.config(command=self.btn_cmd_save)
        self.main_win.btn_clear.config(command=self.btn_cmd_clear)
        self.main_win.btn_restore.config(command=self.btn_cmd_restore)

        self.main_win.btn_repeat.config(command=self.btn_cmd_repeat)

        self.setup_numeric_entry()

        tkh.set_entry_text(self.main_win.entry_repeat,"1")

    def setup_numeric_entry(self):
        entry_widgets = [
            self.main_win.entry_rel_delay,
            self.main_win.entry_m_press_intv,
            self.main_win.entry_k_press_intv,
            self.main_win.entry_repeat
            ]

        for ew in entry_widgets:
            val_num_cmd = ew.register(tkh.validate_number)
            ew.config(validate="key", validatecommand=(val_num_cmd, '%P'))

        vcmd = self.main_win.entry_repeat.register(self.validate_repeat_callback)
        self.main_win.entry_repeat.config(validate='focusout', validatecommand=(vcmd, '%P'))


    def macro_list_callback(self, event):
        selection = event.widget.curselection()
        if not selection: return
        index = selection[0]
        macro_name =  event.widget.get(index)
        self.select_load_macro(macro_name)

    def select_load_macro(self, macro_name):
        self.selected_macro = self.macro_manager.load_macro(macro_name)
        self.update_macro_screen()
        self.sbar_msg(f"Loaded macro: {self.selected_macro.name}")

    def get_prev_macro(self, macro_name:str):
        listbox = self.main_win.slbox_macro_list
        items = listbox.get(0, tk.END)
        index = items.index(macro_name)

        if len(items) == 1:
            return None, None
        if index == 0:
            return listbox.get(index+1), 0

        return listbox.get(index-1), index - 1

    def sub_player(self,macro_name):
        sub_macro = self.macro_manager.load_macro(macro_name)
        self.sbar_msg(f"Loaded macro: {macro_name}")
        return sub_macro.events, sub_macro

    def update_macro_screen(self):

        macro = self.selected_macro

        self.btn_cmd_key_intv_state(self.main_win.btn_key_press_intv)
        self.btn_cmd_rel_delayState(self.main_win.btn_post_rel_intv)

        self.entry_toggle(self.main_win.entry_m_press_intv, True)
        self.entry_toggle(self.main_win.entry_k_press_intv, True)
        self.entry_toggle(self.main_win.entry_rel_delay, True)

        self.main_win.lb_hotkey_text['text'] = macro.hotkey

        tkh.set_entry_text(self.main_win.entry_repeat, macro.global_repeat)

        tkh.set_entry_text(self.main_win.entry_k_press_intv, f"{macro.global_keypress_interval}")
        tkh.set_entry_text(self.main_win.entry_m_press_intv, f"{macro.global_mousepress_interval}")
        tkh.set_entry_text(self.main_win.entry_rel_delay, f"{macro.global_release_interval}")

        tkh.button_toggle(self.main_win.btn_move_mouse,  macro.global_mouse_movement)

        self.btn_cmd_mouse_intv_state(self.main_win.btn_mouse_press_intv)
        self.btn_cmd_key_intv_state(self.main_win.btn_key_press_intv)
        self.btn_cmd_rel_delayState(self.main_win.btn_post_rel_intv)
        self.btn_cmd_repeatState()

        self.set_mouse_offset(macro)
        self.setup_events()

    def mouse_offset(self):
        txtstr = self.main_win.label_offset['text']
        parts = txtstr[1:len(txtstr)-1].split(",")
        return int(parts[0]), int(parts[1])

    def save_selected_macro(self):
        macro = self.selected_macro
        macro.hotkey = self.main_win.lb_hotkey_text['text']
        macro.global_repeat = int(self.main_win.entry_repeat.get())
        macro.global_keypress_interval = tkh.get_entry_int(self.main_win.entry_k_press_intv)
        macro.global_mousepress_interval = tkh.get_entry_int(self.main_win.entry_m_press_intv)
        macro.global_mouse_movement = tkh.button_state(self.main_win.btn_move_mouse)
        macro.global_mousepress_interval_on = tkh.button_state(self.main_win.btn_mouse_press_intv)
        macro.global_keypress_interval_on = tkh.button_state(self.main_win.btn_key_press_intv)
        macro.global_release_interval_on = tkh.button_state(self.main_win.btn_post_rel_intv)
        macro.global_mouse_offset_x , macro.global_mouse_offset_y = self.mouse_offset()
        self.macro_manager.save_macro(macro)
        self.sbar_msg(f"Saved macro: {self.selected_macro.name}")

    def setup_events(self):

        self.clear_evt_labels()
        if not self.selected_macro.events :
            return

        inner_frame = self.main_win.swin_events_f

        #button = {}
        #for i in range(12):
        #    button[i] = tk.Button(inner_frame, text='VButton'+str(i))
        #    button[i].grid(sticky='w')
        #self.events_drawn()


        #max_label_length = 15 # max(len(evt.abv) for evt in self.selected_macro.events)
        #max_label_width = max_label_length * 8  # Adjust this multiplier based on font size and character width
        #canvas_width = canvas.winfo_width()
        #num_columns = max(1, canvas_width // max_label_width)
        num_columns= 4
        # num_rows = math.ceil(len(label_list) / num_columns)
        label:tk.Label = None
        for i, evt in enumerate(self.selected_macro.events):
            row = i // num_columns
            col = i % num_columns
            #string = f"{string}"
            # print(f"label text :{string=}")
            #lfont = "Apple Color Emoji"
            #lfont = "Noto Color Emoji"
            lfont = "Lucid Console"
            #label = EventWidget(self.main_win.swin_events, evt, justify='left',font=(lfont, 12) )
            label = EventWidget(inner_frame, evt, justify='left',font=(lfont, 10) )

            label.grid(row=row, column=col, sticky="w", padx=5, pady=5)
            #
            # label.grid(sticky="w")

        label.wait_visibility()
        self.events_drawn()

    def events_drawn(self):
        inner_frame:tk.Canvas = self.main_win.swin_events_f
        bbox = inner_frame.bbox()
        self.main_win.swin_events.config(scrollregion=bbox)


    def macro_select(self,macro_name:str):
        listbox = self.main_win.slbox_macro_list
        items = listbox.get(0, tk.END)
        try:
            index = items.index(macro_name)
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(index)
            listbox.see(index)  # Ensure the selected item is visible
            self.select_load_macro(macro_name)
        except ValueError:
            print(f"Value Error in selecting macro: {macro_name}")

    def get_text(self,entry_field):
        #return entry_field.get("1.0",'end-1c')
        return entry_field.get()

    def validate_repeat_callback(self,*args) -> bool:       # pylint: disable=unused-argument
        e = self.main_win.entry_repeat
        p_str = self.get_text(e)
        if p_str == "" or p_str == "0":
            tkh.set_entry_text(e,"1")
        return True


    @classmethod
    def main(cls):
        '''Main entry point for the application.'''

        cls.root = tk.Tk()
        cls.root.withdraw()

        cls.root.protocol( 'WM_DELETE_WINDOW' , cls.root.destroy)

        cls.pymacros_toplevel = cls.root #tk.Toplevel(cls.root)   #
        cls.pymacros_win = PyMouseMacro(cls.pymacros_toplevel)

        cls.pymacros_toplevel.update()

        cls.app_bridge = AppBridgeMain(cls.pymacros_win)
        cls.root.mainloop()

if __name__ == '__main__':
    AppBridgeMain.main()
