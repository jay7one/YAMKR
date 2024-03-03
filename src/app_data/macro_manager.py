import os
import shutil
import glob
import json
import unittest
from app_data.settings import Settings
from macros.macro import Macro

class MacroManager(Settings):
    CONTENT="macros"
    def __init__(self, initial_values=None):
        super().__init__("Macros", False, initial_values)
        self.macros_path = os.path.join(self.dir_path, MacroManager.CONTENT )
        if not os.path.isdir(self.macros_path):
            os.mkdir(self.macros_path)
        self.update_macro_list()

    def update_macro_list(self):
        macro_list = self.get_macro_list()
        for k,v in macro_list.items():
            self.change_settings(MacroManager.CONTENT, option=k, new_value=v)

    def get_macro_list(self):
        mac_files = dict()
        for root, _, _ in os.walk(self.macros_path):
            for file in glob.glob(os.path.join(root, '*' + Macro.EXTENTION)):
                filename = os.path.splitext(os.path.basename(file))[0]
                mac_files[filename] = file
        return mac_files

    def initial_settings(self):
        return {MacroManager.CONTENT: {} }

    def remove_macro(self, macro_name):
        settings = self.get_config()
        macro_path = settings[MacroManager.CONTENT][macro_name]
        del settings[MacroManager.CONTENT][macro_name]
        os.remove(macro_path)
        self.save_settings(json.dumps(settings, indent=4))

    def rename_macro(self, macro:Macro , new_name):
        settings = self.get_config()

        macro_path = settings[MacroManager.CONTENT][macro.name]
        del settings[MacroManager.CONTENT][macro.name]
        macro.name = new_name
        new_path = os.path.join(self.macros_path, new_name + Macro.EXTENTION)
        os.rename(macro_path, new_path)
        settings[MacroManager.CONTENT][new_name] = new_path
        self.save_settings(json.dumps(settings, indent=4))

    def save_macro(self, macro:Macro):
        settings = self.get_config()
        print(f"Saveing actual macro :{self.macros_path}|{macro}")
        file_path = macro.save(self.macros_path)
        settings[MacroManager.CONTENT][macro.name] = file_path
        self.change_settings(MacroManager.CONTENT, option=macro.name, new_value = file_path)

    def clear_macro(self,macro:Macro ):
        macro.clear()

    def get_macros(self):
        return self.get_setting(MacroManager.CONTENT)

    def get_macro_names(self):
        return sorted(self.get_setting(MacroManager.CONTENT).keys())

    def load_macro(self, name):
        return Macro.from_file(self.get_setting(MacroManager.CONTENT,[name]))

    def clear_macros(self):
        self.reset_settings()
        if os.path.exists(self.macros_path):
            shutil.rmtree(self.macros_path)
        os.mkdir(self.macros_path)
        self.update_macro_list()

class TestMacroSave(unittest.TestCase):
    def setUp(self):

        self.json_data = '''
        {
            "name": "MyMacro",
            "events": [
                {"event_type": "key_down", "event_value": "A"},
                {"event_type": "delay", "event_value": "200"},
                {"event_type": "key_up", "event_value": "A"},
                {"event_type": "delay", "event_value": "200"},
                {"event_type": "click_down", "event_value": "left"},
                {"event_type": "delay", "event_value": "200"},
                {"event_type": "click_up", "event_value": "left"}
            ],
            "global_keypress_interval": 50,
            "global_mousepress_interval": 20,
            "global_keypress_interval_on": true,
            "global_mousepress_interval_on": false,
            "hotkey": "Ctrl+Alt+M",
            "global_mouse_offset_x": 0,
            "global_mouse_offset_y": 0
        }
        '''

    def test01_save(self):
        macro_instance = Macro.from_json(self.json_data)
        macro_manger = MacroManager()
        macro_manger.clear_macros()

        macro_manger.save_macro(macro_instance)
        macro_manger.rename_macro(macro_instance, "MyMac2")
        macro_manger.remove_macro("MyMac2")

        content = macro_manger.get_config()[MacroManager.CONTENT]

        print()
        self.assertEqual(content,{})


    def test02_load(self):
        macro_instance = Macro.from_json(self.json_data)
        macro_manger = MacroManager()
        macro_manger.clear_macros()

        macro_manger.save_macro(macro_instance)
        print(f"Macro saved: {macro_instance}")
        macro_name = 'MyMacro'
        loaded_macro = macro_manger.load_macro(macro_name)
        print(f"Macro list: {macro_manger.get_macro_list()}")
        self.assertEqual(loaded_macro.name, macro_name)

if __name__ == "__main__":
    unittest.main()
