class Keys:
    vk_nb = {
        "<96>": "0",
        "<97>": "1",
        "<98>": "2",
        "<99>": "3",
        "<100>": "4",
        "<101>": "5",
        "<102>": "6",
        "<103>": "7",
        "<104>": "8",
        "<105>": "9",
        "<65437>": "5",
        "<110>": ".",
    }

    @classmethod
    def get_key_pressed(cls,keyboard_listener, key):
        """
        Return right key. canonical() prevents from weird characters to show up with ctrl active, like ctrl + d,
        pynput will not print Key.ctrl and d, it will print Key.ctrl and a weird character
        """

        if "Key." in str(key):
            key_pressed = str(key)
        else:
            key_pressed_list = list(str(keyboard_listener.canonical(key)))
            if key_pressed_list[0] != "<":
                key_pressed_list[0] = ""
                key_pressed_list[-1] = ""
            key_pressed = "".join(key_pressed_list)

        return key_pressed
