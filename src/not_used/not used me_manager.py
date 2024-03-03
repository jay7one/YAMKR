import time
import threading
from pynput.mouse import Listener as MouseListener
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Listener as KeyboardListener, Key
from pynput.keyboard import Controller as KeyboardController
from macros.macro_event import EventType, MacroEvent
from macro_event_recorder import MacroEventRecorder

class MacroEventManager(MacroEventRecorder):
    def __init__(self):
        self.macro_events = []
        self.last_event_time = None
        self.ctrl_left_pressed = False
        self.ctrl_right_pressed = False
        self.stop_event = threading.Event()


    def record_macro(self):
        self.last_event_time = time.time_ns()  # Start recording time
        self.macro_events = []

        with MouseListener(on_click=self.on_click) as mouse_listener, \
             KeyboardListener(on_press=self.on_key_press) as keyboard_listener:
            mouse_listener.join()
            keyboard_listener.join()
        return self.macro_events

    def on_click(self, x, y, button, pressed):
        event_type = EventType.CLICK_DOWN if pressed else EventType.CLICK_UP
        self.add_event(event_type, (x, y))

    def on_key_press(self, key):
        print(f"{key = }")
        if key == Key.ctrl_l:   self.ctrl_left_pressed = True
        elif key == Key.ctrl_r: self.ctrl_right_pressed = True

        if self.ctrl_left_pressed and self.ctrl_right_pressed:  # Stop recording if both Ctrl keys are pressed
            self.is_recording = False
            return False

        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)

        self.add_event(EventType.KEY_DOWN, key_char)

    def add_event(self, event_type, event_value):
        if not self.is_recording:
            return

        current_time = time.time_ns()

        if self.last_event_time is None:
            delay_ms = 0
        else:
            delay_ns = current_time - self.last_event_time
            delay_ms = delay_ns / 1_000_000  # Convert delay to milliseconds
            self.macro_events.append(MacroEvent(EventType.DELAY, delay_ms))

        self.last_event_time = current_time
        self.macro_events.append(MacroEvent(event_type, event_value))

    def play_macro(self, key_interval=0, mouse_interval=0, release_delay=0):

        keyboard = KeyboardController()
        mouse = MouseController()

        last_event_type = None

        for event in self.macro_events:

            if event.event_type == EventType.DELAY:
                if last_event_type in (EventType.KEY_UP, EventType.CLICK_UP) :
                    if release_delay > 0:
                        time.sleep(release_delay)
                    else:
                        time.sleep(event.event_value / 1000)  # Convert delay to seconds
                else:
                    if last_event_type == EventType.KEY_DOWN:
                        if key_interval > 0:
                            time.sleep(key_interval)

                    elif last_event_type == EventType.CLICK_DOWN:
                        if mouse_interval > 0:
                            time.sleep(mouse_interval)
                continue

            last_event_type = event.event_type

            if event.event_type == EventType.KEY_DOWN:
                keyboard.press(event.event_value)

            elif event.event_type == EventType.KEY_UP:
                keyboard.release(event.event_value)

            elif event.event_type == EventType.CLICK_DOWN:
                mouse.press(Button.left)

            elif event.event_type == EventType.CLICK_UP:
                mouse.release(Button.left)


# Example usage:
if __name__ == "__main__":
    manager = MacroEventManager()
    print("Recording macro. Press ctrls to stop.")
    macro_events = manager.record_macro()
    print("Macro recorded.")
    #manager.play_macro(macro_events)
    print(f"{macro_events =}")
