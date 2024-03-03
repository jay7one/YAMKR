#import sys
import tkinter as tk

from page.PyMouseMacro import PyMouseMacros,TLDialog
from app_data.macro_manager import MacroManager
from macros import Macro

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

    def additional_settings(self):
        self.main_win.SLBoxMacroList.configure(selectforeground="darkblue")
        self.main_win.SLBoxMacroList.configure(selectbackground="lightcyan")

    def load_macro_list(self):
        for idx, macro in enumerate(self.macro_manager.get_macro_names()):
            self.main_win.SLBoxMacroList.insert(idx,macro)

    def macro_list_callback(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            print(f"text={data}")
        else:
            print("no selection")

        #load_macro

    def load_events_by_name(self,macro_name):
        self.selected_macro = self.macro_manager.load_macro(macro_name)
        self.load_events()

    def load_events(self):
        self.BtCmdClear()
        for e in self.selected_macro.events:
            print(f"Event:{e}")


    def add_callbacks(self,main_win:PyMouseMacros):
        main_win.SLBoxMacroList.bind("<<ListboxSelect>>", self.macro_list_callback)

        self.main_win.BtnMoveMouse.configure(command=self.BtCmdMoveMouse)
        self.main_win.BtnOffset.configure(command=self.BtCmdMouseOffset)
        self.main_win.BtnKPressIntv.configure(command=self.BtCmdKeyIntv)
        self.main_win.BtnMPressIntv.configure(command=self.BtCmdMouseIntv)
        self.main_win.BtnPostRelIntv.configure(command=self.BtCmdRelDelay)
        self.main_win.BtnHotKeyAdd.configure(command=self.BtCmdHotkeyAdd)
        self.main_win.BtnHotKeyDel.configure(command=self.BtCmdHotkeyDel)
        self.main_win.BtnAddMacro.configure(command=self.BtCmdMacroAdd)
        self.main_win.BtnDelMacro.configure(command=self.BtCmdMacroDel)

        self.main_win.BtnRefresh.configure(command=self.BtCmdRefresh)
        self.main_win.BtnFolder.configure(command=self.BtCmdFolder)

        self.main_win.BtnRecord.configure(command=self.BtCmdRecord)
        self.main_win.BtnSave.configure(command=self.BtCmdSave)
        self.main_win.BtnClear.configure(command=self.BtCmdClear)
        self.main_win.BtnRestore.configure(command=self.BtCmdRestore)

        self.main_win.BtnRepeat.configure(command=self.BtCmdRepeat)

        self.set_entry_text(self.main_win.EntryRepeat,"1")

        self.main_win.EntryRelDelay.configure(validatecommand=(self.validate_number, '%P'))
        self.main_win.EntryMPressIntv.configure(validatecommand=(self.validate_number, '%P'))
        self.main_win.EntryKPressIntv.configure(validatecommand=(self.validate_number, '%P'))

    def BtCmdClear(self):
        if not self.selected_macro:
            return

        self.macro_manager.clear_macro(self.selected_macro)

    def BtCmdHotkeyAdd(self,*args): pass
    def BtCmdHotkeyDel(self,*args): pass
    def BtCmdKeyIntv(self,*args): pass
    def BtCmdMacroAdd(self,*args): pass
    def BtCmdMacroDel(self,*args): pass
    def BtCmdFolder(self,*args): pass
    def BtCmdRefresh(self,*args): pass
    def BtCmdMouseIntv(self,*args): pass
    def BtCmdMouseOffset(self,*args): pass
    def BtCmdMoveMouse(self,*args): pass
    def BtCmdRecord(self,*args): pass
    def BtCmdRelDelay(self,*args): pass
    def BtCmdRestore(self,*args): pass
    def BtCmdSave(self,*args): pass
    def BtCmdRepeat(self,*args): pass

    def validate_number(self,P) -> bool:
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

        cls.app_bridge = AppBridge(cls.pymacros_win,cls.dialog_win)
        cls.root.mainloop()

if __name__ == '__main__':
    AppBridge.main()
