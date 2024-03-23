from abc import abstractmethod
import tkinter as tk
from macros.macro import Macro
from page.PyMouseMacro import PyMouseMacro
from app_data.app_settings import AppSettings
from app_data.macro_manager import MacroManager
from app_bridge.event_widget import EventWidget

class AppBridgeBase:
    root=None
    pymacros_toplevel, pymacros_win = None,None
    app_bridge = None


    def __init__(self) -> None:
        self.main_win:PyMouseMacro = None
        self.app_settings:AppSettings = None
        self.macro_manager:MacroManager = None
        self.selected_macro:Macro = None
        self.menu_setting_vars = {}
        self.main_geo = None
        self.last_evt_clicked:EventWidget = None

    def sbar_msg(self,msg) -> None:
        self.main_win.lb_status_bar['text'] = msg

    @abstractmethod
    def set_delay_upd_bt(self):pass

    @abstractmethod
    def get_macro_names(self, refresh=False):pass

    @abstractmethod
    def load_macro_list(self, refresh=False):
        pass

    @abstractmethod
    def macro_select(self,macro_name:str):
        pass

    @abstractmethod
    def setup_events(self):
        pass

    @abstractmethod
    def select_load_macro(self, macro_name:str):
        pass

    @abstractmethod
    def get_prev_macro(self, macro_name:str):
        pass

    @abstractmethod
    def center_win(self, win):
        pass

    @abstractmethod
    def btn_bold_on_modify(self, modified):
        pass

    @abstractmethod
    def save_selected_macro(self):
        pass

    @abstractmethod
    def check_for_hotkey(self, event:tk.Event):
        pass

if __name__ == '__main__':
    gs = "300x200+100+50"
    x, y, width, height = AppBridgeBase.get_geo(gs)
    print(f"x: {x}, y: {y}, width: {width}, height: {height}")
