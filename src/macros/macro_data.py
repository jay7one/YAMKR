from dataclasses import dataclass

# TODO: this should be better structured and variables renamed
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

    global_release_interval : int = 500
    global_release_interval_on : bool = False
    global_repeat: int = 1
