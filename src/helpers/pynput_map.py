from pynput.keyboard import Key
from pynput.mouse import Button

class PynputMap:

    buttonDictionary = {
        "Button.unknown":Button.unknown,
        "Button.left":Button.left,
        "Button.middle":Button.middle,
        "Button.right":Button.right,
        "Button.Left":Button.left,
        "Button.Middle":Button.middle,
        "Button.Right":Button.right,
        "Left":Button.left,
        "Middle":Button.middle,
        "Right":Button.right,
        "left":Button.left,
        "middle":Button.middle,
        "right":Button.right
        }

    keyDictionary = {
        "Key.alt":Key.alt,
        "Key.alt_l":Key.alt_l,
        "Key.alt_r":Key.alt_r,
        "Key.alt_gr":Key.alt_gr,
        "Key.backspace":Key.backspace,
        "Key.caps_lock":Key.caps_lock,
        "Key.cmd":Key.cmd,
        "Key.cmd_l":Key.cmd_l,
        "Key.cmd_r":Key.cmd_r,
        "Key.ctrl":Key.ctrl,
        "Key.ctrl_l":Key.ctrl_l,
        "Key.ctrl_r":Key.ctrl_r,
        "Key.delete":Key.delete,
        "Key.down":Key.down,
        "Key.end":Key.end,
        "Key.enter":Key.enter,
        "Key.esc":Key.esc,
        "Key.f1":Key.f1,
        "Key.f2":Key.f2,
        "Key.f3":Key.f3,
        "Key.f4":Key.f4,
        "Key.f5":Key.f5,
        "Key.f6":Key.f6,
        "Key.f7":Key.f7,
        "Key.f8":Key.f8,
        "Key.f9":Key.f9,
        "Key.f10":Key.f10,
        "Key.f11":Key.f11,
        "Key.f12":Key.f12,
        "Key.f13":Key.f13,
        "Key.f14":Key.f14,
        "Key.f15":Key.f15,
        "Key.f16":Key.f16,
        "Key.f17":Key.f17,
        "Key.f18":Key.f18,
        "Key.f19":Key.f19,
        "Key.f20":Key.f20,
        "Key.home":Key.home,
        "Key.left":Key.left,
        "Key.page_down":Key.page_down,
        "Key.page_up":Key.page_up,
        "Key.right":Key.right,
        "Key.shift":Key.shift,
        "Key.shift_l":Key.shift_l,
        "Key.shift_r":Key.shift_r,
        "Key.space":Key.space,
        "Key.tab":Key.tab,
        "Key.up":Key.up,
        "Key.media_play_pause":Key.media_play_pause,
        "Key.media_volume_mute":Key.media_volume_mute,
        "Key.media_volume_down":Key.media_volume_down,
        "Key.media_volume_up":Key.media_volume_up,
        "Key.media_previous":Key.media_previous,
        "Key.media_next":Key.media_next,
        "Key.insert":Key.insert,
        "Key.menu":Key.menu,
        "Key.num_lock":Key.num_lock,
        "Key.pause":Key.pause,
        "Key.print_screen":Key.print_screen,
        "Key.scroll_lock":Key.scroll_lock}

    @classmethod
    def map_key(cls,txt):
        for k, v in  cls.keyDictionary.items():
            if k == txt: return v
        return txt

    @classmethod
    def map_btn(cls,txt):
        for k, v in  cls.buttonDictionary.items():
            if k == txt: return v
        return txt
