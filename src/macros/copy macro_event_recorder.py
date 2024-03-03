import threading
import time
from pynput.keyboard import Controller as KeyboardController, Listener as KeyboardListener, Key
from pynput.mouse import Controller as MouseController, Button
from macros.macro_event import MacroEvent, EventType
from macros.macro_event_recorder import MacroEventRecorder

class MacroEventManager(MacroEventRecorder):
    def __init__(self):
        super().__init__()
        self.keyboard_controller = KeyboardController()
        self.mouse_controller = MouseController()
        self.playback_kb_listener = None

    def play_macro(self, macro_events):
        for event in macro_events:
            if self.stop_event.is_set():
                break

            if event.event_type == EventType.KEY_DOWN:
                self.keyboard_controller.press(event.event_value)
            elif event.event_type == EventType.KEY_UP:
                self.keyboard_controller.release(event.event_value)
            elif event.event_type == EventType.CLICK_DOWN:
                button, x, y = event.event_value
                self.mouse_controller.position = (x, y)
                self.mouse_controller.press(button)
            elif event.event_type == EventType.CLICK_UP:
                button, x, y = event.event_value
                self.mouse_controller.position = (x, y)
                self.mouse_controller.release(button)
            elif event.event_type == EventType.DELAY:
                time.sleep(event.event_value / 1000)  # Convert milliseconds to seconds

    def stop_playback(self):
        super().stop_recording()

    def start_listening(self):
        self.playback_kb_listener = KeyboardListener(on_press=self.on_key_press)
        self.playback_kb_listener.start()

    def on_key_press(self, key):
        if key == Key.ctrl_l and not self.stop_event.is_set():
            self.stop_playback()

# Example usage:
if __name__ == "__main__":
    # Create an instance of MacroEventManager
    manager = MacroEventManager()

    # Start recording
    manager.start_listening()

    # Stop recording when Ctrl + End is pressed
    manager.record_macro()

    # Playback recorded macro
    manager.play_macro(manager.macro_events)
