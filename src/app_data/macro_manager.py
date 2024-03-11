import os
import shutil
import glob
import json
import unittest
from app_data.settings import Settings
from macros.macro import Macro, MACRO_EXT

class MacroManager(Settings):
    CONTENT="macros"

    def __init__(self, initial_values=None):
        super().__init__("Macros", False, initial_values)
        self.macros_path = os.path.join(self.dir_path, MacroManager.CONTENT )
        self.hotkey_list = {}
        if not os.path.isdir(self.macros_path):
            os.mkdir(self.macros_path)
        self.update_macro_list()

    def update_macro_list(self):
        macro_list = self.get_macro_list()
        self.reset_settings()
        for k,v in macro_list.items():
            self.change_settings(MacroManager.CONTENT, option=k, new_value=v)

    def find_hotkey_macro(self,hotkey:str) -> str:
        for key, value in self.hotkey_list.items():
            if key == hotkey: return value
        return None

    def update_hotkey_list(self, name:str, hotkey:str):
        if hotkey == "":    self.remove_hotkey(name)
        else:               self.hotkey_list[hotkey] = name

    def remove_hotkey(self,name:str):
        for key, value in self.hotkey_list.items():
            if value == name:
                del self.hotkey_list[key]
                return

    def macro_exists(self, macro_name:str) -> bool:
        return macro_name in self.get_setting(MacroManager.CONTENT).keys()

    def refresh_hotkey(self, macro_name:str) -> str:
        hotkey = Macro.get_hotkey(macro_name, self.macros_path)
        self.update_hotkey_list(macro_name, hotkey)
        return hotkey

    def get_macro_list(self) -> dict:
        mac_files = dict()
        for root, _, _ in os.walk(self.macros_path):
            for file in glob.glob(os.path.join(root, '*' + MACRO_EXT)):
                filename = os.path.splitext(os.path.basename(file))[0]
                mac_files[filename] = self.refresh_hotkey(filename)
                #print(f"Found {file=}")
        return mac_files

    def get_macro_fullpath(self, name:str) -> str:
        return os.path.join(self.dir_path, self.CONTENT, name + MACRO_EXT  )

    def initial_settings(self) -> dict:
        return {MacroManager.CONTENT: {} }

    def remove_macro(self, macro_name:str) -> None:
        settings = self.get_config()
        macro_path = self.get_macro_fullpath(macro_name)
        self.remove_hotkey(macro_name)
        del settings[MacroManager.CONTENT][macro_name]
        os.remove(macro_path)
        self.save_settings(json.dumps(settings, indent=4))

    def rename_macro(self, macro:Macro , new_name:str) -> None:
        settings = self.get_config()
        macro_path = self.get_macro_fullpath(macro.name)
        self.remove_hotkey(macro.name)
        del settings[MacroManager.CONTENT][macro.name]

        macro.name = new_name
        self.update_hotkey_list(macro.name,macro.hotkey)
        new_path = self.get_macro_fullpath(new_name)
        os.rename(macro_path, new_path)
        settings[MacroManager.CONTENT][new_name] = macro.hotkey
        self.save_settings(json.dumps(settings, indent=4))

    def new_macro(self,name:str,hotkey:str) -> Macro:
        new_mac = Macro(name,[])
        new_mac.hotkey = hotkey
        self.save_macro(new_mac)
        return new_mac

    def save_macro(self, macro:Macro):
        settings = self.get_config()
        self.update_hotkey_list(macro.name,macro.hotkey)
        #print(f"Saving actual macro :{self.macros_path}|{macro}")
        macro.save(self.macros_path)
        settings[MacroManager.CONTENT][macro.name] = macro.hotkey
        self.change_settings(MacroManager.CONTENT, option=macro.name, new_value = macro.hotkey)

    def clear_macro(self,macro:Macro ):
        macro.clear()

    def get_macros(self) -> dict:
        return self.get_setting(MacroManager.CONTENT)

    def get_macro_names(self, refresh=False) -> list[str]:
        if refresh:
            self.update_macro_list()
        return sorted(self.get_setting(MacroManager.CONTENT).keys(), key=str.casefold)

    def load_macro(self, name) -> Macro:
        macro = Macro.from_file(self.get_macro_fullpath(name))
        #print(f"Loaded Macro {name} events:{len(macro.events)}")
        return macro

    def clear_macros(self):         # used for testing
        self.reset_settings()
        if os.path.exists(self.macros_path):
            shutil.rmtree(self.macros_path)
        os.mkdir(self.macros_path)
        self.hotkey_list = {}
        self.update_macro_list()

class TestMacroSave(unittest.TestCase):
    def setUp(self):
        self.mac_name = "MyMacro"
        self.json_data = '''
        {
            "name": "MyMacro",
            "events": [
                {"event_type": "key_down", "event_value": "A"},
                {"event_type": "delay", "event_value": "200"},
                {"event_type": "key_up", "event_value": "A"},
                {"event_type": "delay", "event_value": "200"},
                {"event_type": "click_down", "event_value": "left, 20,20"},
                {"event_type": "delay", "event_value": "200"},
                {"event_type": "click_up", "event_value": "left, 20,20"}
            ],
            "global_keypress_interval": 50,
            "global_mousepress_interval": 20,
            "global_keypress_interval_on": true,
            "global_mousepress_interval_on": false,
            "hotkey": "F3",
            "global_mouse_offset_x": 0,
            "global_mouse_offset_y": 0,
            "global_repeat" : 1
        }
        '''

        self.macro_instance = Macro.from_json(self.json_data)
        self.macro_manger = MacroManager()
        self.macro_manger.clear_macros()
        self.macro_manger.save_macro(self.macro_instance)

    def test01_save(self):
        self.macro_manger.rename_macro(self.macro_instance, "MyMac2")
        self.macro_manger.remove_macro("MyMac2")
        content = self.macro_manger.get_config()[MacroManager.CONTENT]
        self.assertEqual(content,{})

    def test02_load(self):
        loaded_macro = self.macro_manger.load_macro(self.mac_name)
        #print(f"Macro list: {self.macro_manger.get_macro_list()}")
        self.assertEqual(loaded_macro.name, self.mac_name)

    def test03_hotkey(self):
        #print(f"HKList:{self.macro_manger.hotkey_list=}")
        self.assertEqual(self.macro_manger.find_hotkey_macro("F3"), self.mac_name)

    def test04_hotkey(self):
        self.assertEqual(self.macro_manger.find_hotkey_macro("NoMacro"), None)

    def test05_hotkey(self):
        self.macro_manger.update_hotkey_list(self.mac_name, "F4")
        self.assertEqual(self.macro_manger.find_hotkey_macro("F4"), self.mac_name)

    def test06_hotkey(self):
        mac_name1 = self.macro_manger.find_hotkey_macro("F3")
        self.macro_manger.remove_hotkey(self.mac_name)
        mac_name2 = self.macro_manger.find_hotkey_macro("F3")
        check = mac_name1 == self.mac_name and mac_name2 is None
        self.assertEqual(check,True)

    def test06_exists(self):
        self.assertEqual(self.macro_manger.macro_exists(self.mac_name), True)

    def test07_exists(self):
        self.assertEqual(self.macro_manger.macro_exists("MacroNone"), False)

if __name__ == "__main__":
    unittest.main()
