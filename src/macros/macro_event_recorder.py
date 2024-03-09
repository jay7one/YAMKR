import sys
import threading
import time

from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
from pynput.mouse import Button
from macros.macro_event import MacroEvent, EventType

# pylint: disable=attribute-defined-outside-init

class MacroEventRecorder:
    def __init__(self):
        self.macro_events = []
        self.prep_macro()

    def prep_macro(self):
        self.pressed_keys = set()
        self.offsets = 0,0
        self.last_event_time = None
        self.ctrl_pressed = False
        self.end_pressed = False
        self.stop_event = threading.Event()
        self.last_event_time = None
        self.keyboard_listener = None
        self.mouse_listener = None

    def record_macro(self, offsets):

        self.prep_macro()
        self.offsets = offsets

        self.keyboard_listener = KeyboardListener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.mouse_listener = MouseListener(on_click=self.on_mouse_click)
        self.keyboard_listener.start()
        self.mouse_listener.start()
        self.keyboard_listener.join()
        self.mouse_listener.stop()

        # Find the index of last Ctrl key press event
        last_ctrl_index = None
        for i, event in enumerate(reversed(self.macro_events)):
            if event.event_type == EventType.KEY_DOWN and event.event_value == 'Key.ctrl_l':
                last_ctrl_index = max(0,len(self.macro_events) - 2 - i)
                break

        if last_ctrl_index is not None:
            # Remove events from Ctrl down to End release
            del self.macro_events[last_ctrl_index:]

        return self.macro_events

    def add_delay_event(self):
        current_time = time.time()
        if self.last_event_time is not None:
            delay_ms = int((current_time - self.last_event_time) * 1000)
            self.macro_events.append(MacroEvent(EventType.DELAY, delay_ms))  # Convert delay to milliseconds
        self.last_event_time = current_time

    def on_mouse_click(self, x, y, button, pressed):
        self.add_delay_event()

        if button == Button.left:           event_value = "left"
        elif button == Button.right:        event_value = "right"
        elif button == Button.middle:       event_value = "middle"
        else: return

        ox,oy = self.offsets
        x -= ox
        y -= oy

        event_type = EventType.CLICK_DOWN if pressed else EventType.CLICK_UP
        self.macro_events.append(MacroEvent(event_type, (event_value, x, y)))

    def on_key_press(self, key):
        if key == Key.ctrl_l:
            self.ctrl_pressed = True
        elif key == Key.end:
            self.end_pressed = True

        if self.ctrl_pressed and self.end_pressed:
            self.stop_event.set()
            return False

        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)

        if key_char in self.pressed_keys:
            return True  # Keep the listener running

        self.add_delay_event()

        self.pressed_keys.add(key_char)
        self.macro_events.append(MacroEvent(EventType.KEY_DOWN, key_char))
        #print(f"Key pressed: {key_char}")
        return True

    def on_key_release(self, key):
        if key == Key.ctrl_l:   self.ctrl_pressed = False
        elif key == Key.end:    self.end_pressed = False

        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)

        self.pressed_keys.discard(key_char)
        self.clear_input_buffer()
        self.add_delay_event()
        self.macro_events.append(MacroEvent(EventType.KEY_UP, key_char))
        return True

    @classmethod
    def clear_input_buffer(cls):
        try:
            # For Windows
            import msvcrt       # pylint: disable=import-outside-toplevel
            while msvcrt.kbhit():
                msvcrt.getch()
        except ImportError:
            # For Unix
            import termios  # pylint: disable=import-outside-toplevel
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)

    @classmethod
    def print_events(cls,recorded_events):
        print("Recorded events:")
        for i, event in enumerate(recorded_events, 1):
            if event.event_type == EventType.DELAY:
                print(f"{i}. Delay: {event.event_value} ms")
            elif event.event_type == EventType.KEY_DOWN:
                print(f"{i}. Key down: {event.event_value}")
            elif event.event_type == EventType.KEY_UP:
                print(f"{i}. Key up: {event.event_value}")
            elif event.event_type == EventType.CLICK_DOWN:
                button, x, y = event.event_value
                print(f"{i}. Click down: Button={button}, X={x}, Y={y}")
            elif event.event_type == EventType.CLICK_UP:
                button, x, y = event.event_value
                print(f"{i}. Click up: Button={button}, X={x}, Y={y}")

# Example usage:
if __name__ == "__main__":
    recorder = MacroEventRecorder()
    print("Recording macro. Press 'Ctrl + End' to stop.")
    MacroEventRecorder.print_events(recorder.record_macro((0,0)))
