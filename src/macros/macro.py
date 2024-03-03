import os
from dataclasses import dataclass
import json
import unittest
from macros.macro_event import MacroEvent, EventType

@dataclass
class MacroData:
    name: str
    hotkey : str = ""

    global_keypress_interval : int = 20
    global_mousepress_interval : int = 20
    global_keypress_interval_on : bool = False
    global_mousepress_interval_on : bool = False
    global_mouse_offset_x : int = 0
    global_mouse_offset_y : int = 0
    global_mouse_movement : bool = False
    global_repeat = 1

class Macro(MacroData):
    EXTENTION = '.mac'

    def __init__(self, name, events, **kwargs):
        super().__init__(name=name)
        self.events:list[MacroEvent] = events
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_file(cls,file_path):
        with open(file_path, "r", encoding='utf-8') as macro_file:
            json_data = json.loads(macro_file.read())
        return cls.build_from_json(json_data)

    @classmethod
    def from_json(cls, json_str):
        return cls.build_from_json(json.loads(json_str))

    @classmethod
    def build_from_json(cls, json_data):
        name = json_data.get('name')
        events_data = json_data.get('events', [])
        global_data = {key: value for key, value in json_data.items() if key != 'name' and key != 'events'}

        events = []
        for event_data in events_data:
            event_type_str = event_data.get('event_type')
            event_type = EventType(event_type_str)
            event_value = event_data.get('event_value')
            events.append(MacroEvent(event_type, event_value))

        return cls(name, events, **global_data)

    def assign_hotkey(self,hotkey):
        self.hotkey = hotkey

    def add_event(self, event_type, event_value):
        self.events.append( MacroEvent(event_type,event_value))

    def to_dict(self):
        obj_dict = {
            "name": self.name,
            "events": [event.to_dict() for event in self.events],
            "hotkey": self.hotkey
        }

        for attr_name in dir(self):
            if attr_name.startswith('global_'):
                obj_dict[attr_name] = getattr(self, attr_name)

        return obj_dict

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=False, indent=2)

    def save(self, save_path):
        file_path=os.path.join(save_path, self.name + Macro.EXTENTION)
        with open(file_path, "w", encoding='utf-8') as macro_file:
            macro_file.write(self.to_json())
        return file_path

    def clear(self):
        self.events = []

class TestMacroConversion(unittest.TestCase):
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
            "global_mouse_offset_y": 0,
            "global_repeat": 1
        }
        '''

    def test_conversion(self):
        # Convert JSON data to Macro
        macro_instance = Macro.from_json(self.json_data)
        # Convert Macro back to JSON string
        converted_json_data1 = macro_instance.to_json()
        macro_instance = Macro.from_json(self.json_data)
        converted_json_data2 = macro_instance.to_json()
        # Compare original JSON string with converted JSON string
        self.assertEqual(json.loads(converted_json_data1), json.loads(converted_json_data2))

    def test_io(self):
        macro_instance = Macro.from_json(self.json_data)
        converted_json_data1 = macro_instance.to_json()
        macro_instance.save("")
        new_macro = Macro.from_file("MyMacro.mac")
        converted_json_data2 = new_macro.to_json()
        self.assertEqual(json.loads(converted_json_data1), json.loads(converted_json_data2))

if __name__ == "__main__":
    unittest.main()
