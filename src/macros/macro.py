import os
import json
import unittest
import time
from macros.macro_event import MacroEvent, EventType
from macros.macro_event_manager import MacroEventManager
from macros.macro_data import MacroData
MACRO_EXT = '.mac'

class Macro(MacroData, MacroEventManager):

    def __init__(self, name, events, **kwargs):
        MacroData.__init__(self,name=name)
        MacroEventManager.__init__(self)

        self.events:list[MacroEvent] = events
        #print(f"Macro events loaded:{len(self.events)}")
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_file(cls,file_path):
        with open(file_path, "r", encoding='utf-8') as macro_file:
            json_data = json.loads(macro_file.read())
        return cls.build_from_json(json_data)

    @classmethod
    def get_hotkey(cls,name,filepath):
        file_path=os.path.join(filepath, name + MACRO_EXT)
        macro = cls.from_file(file_path)
        return macro.hotkey

    @classmethod
    def from_name(cls,name, save_path):
        return cls.from_file(os.path.join(save_path, name + MACRO_EXT))

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
        file_path=os.path.join(save_path, self.name + MACRO_EXT)
        with open(file_path, "w", encoding='utf-8') as macro_file:
            macro_file.write(self.to_json())
        return file_path

    def clear(self):
        self.events = []

    def play(self):
        self.play_macro(self.events,self)

    def record(self):
        offsets = (self.global_mouse_offset_x, self.global_mouse_offset_y, )
        self.events.extend(self.record_macro(offsets))

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
                {"event_type": "click_down", "event_value": ["left", 10,10] },
                {"event_type": "delay", "event_value": "200"},
                {"event_type": "click_up", "event_value": ["left", 10,10] }
            ],
            "global_keypress_interval": 50,
            "global_mousepress_interval": 20,
            "global_keypress_interval_on": true,
            "global_mousepress_interval_on": false,
            "hotkey": "Ctrl+Alt+M",
            "global_mouse_offset_x": 0,
            "global_mouse_offset_y": 0,
            "global_release_interval" : 500,
            "global_release_interval_on" : false,
            "global_repeat": 1
        }
        '''

    def test01_record(self):
        print("Start recording events")
        macro_name = "MacroTest01"
        macro_instance = Macro(macro_name,[])
        macro_instance.record()
        macro_instance.save(".")
        new_macro = Macro.from_file(f"{macro_name}.mac")

        converted_json_data1 = macro_instance.to_json()
        converted_json_data2 = new_macro.to_json()

        self.assertEqual(json.loads(converted_json_data1), json.loads(converted_json_data2))

    def test02_conversion(self):
        # Convert JSON data to Macro
        macro_instance = Macro.from_json(self.json_data)
        # Convert Macro back to JSON string
        converted_json_data1 = macro_instance.to_json()
        macro_instance = Macro.from_json(self.json_data)
        converted_json_data2 = macro_instance.to_json()
        # Compare original JSON string with converted JSON string
        self.assertEqual(json.loads(converted_json_data1), json.loads(converted_json_data2))

    def test03_io(self):
        macro_instance = Macro.from_json(self.json_data)
        converted_json_data1 = macro_instance.to_json()
        macro_instance.save("")
        new_macro = Macro.from_file("MyMacro.mac")
        converted_json_data2 = new_macro.to_json()
        self.assertEqual(json.loads(converted_json_data1), json.loads(converted_json_data2))

    def test04_play(self):
        print("Start playback in 2 seconds")
        time.sleep(2)
        macro_name = "MacroTest01"
        macro_instance = Macro.from_name(macro_name,"")
        macro_instance.global_mouse_movement=True
        macro_instance.print_events(macro_instance.events)
        macro_instance.play()

        print(f"Macro:{macro_instance}")
        self.assertTrue(macro_instance.events)


if __name__ == "__main__":
    import helpers.screen_setup # pylint: disable=unused-import
    unittest.main()
