from abc import abstractmethod
from app_bridge_helpers.tkinter_helper import TkinterHelper
from macros.macro import Macro
from page.PyMouseMacro import PyMouseMacro
from app_data.app_settings import AppSettings
from app_data.macro_manager import MacroManager

class AppBridgeBase(TkinterHelper):
    root=None
    pymacros_toplevel, pymacros_win = None,None
    app_bridge = None

    def __init__(self) -> None:
        self.main_win:PyMouseMacro = None
        self.app_settings:AppSettings = None
        self.macro_manager:MacroManager = None
        self.selected_macro:Macro = None
        self.menu_setting_vars = {}

    def sbar_msg(self,msg) -> None:
        self.main_win.lb_status_bar['text'] = msg

    @abstractmethod
    def get_macro_names(self, refresh=False):pass

    @abstractmethod
    def load_macro_list(self, refresh=False):
        print("Fn : load_macro_list not overrriden")

    @abstractmethod
    def macro_select(self,macro_name:str):
        print("Fn : macro_select not overrriden")

    @abstractmethod
    def setup_events(self):
        print("Fn : setup_events not overrriden")

    @abstractmethod
    def select_load_macro(self, macro_name:str):
        print("Fn : select_load_macro not overrriden")
