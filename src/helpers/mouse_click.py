from abc import ABC
from typing import Tuple
from pynput.mouse import Listener as MouseListener

class MouseClick(ABC):
    next_click:Tuple[int, int]

    @staticmethod
    def on_click(x:int, y:int, _, pressed):
        if pressed:
            MouseClick.next_click = (x, y)
            return False  # Stop the listener
        return True

    @staticmethod
    def get_next_click()-> Tuple[int, int]:
        with MouseListener(on_click=MouseClick.on_click) as listener:
            listener.join()
        return MouseClick.next_click
