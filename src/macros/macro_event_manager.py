import time
from pynput.keyboard import Controller as KeyboardController, Listener as KeyboardListener, Key
from pynput.mouse import Controller as MouseController
from macros.macro_event import MacroEvent, EventType
from macros.macro_event_recorder import MacroEventRecorder

class MacroEventManager(MacroEventRecorder):
    def __init__(self):
        super().__init__()
        self.keyboard_controller = KeyboardController()
        self.mouse_controller = MouseController()
        self.playback_kb_listener = None

    def play_macro(self, macro_events:list[MacroEvent],
                   key_press_release_interval=None,
                   click_press_release_interval=None,
                   key_release_press_delay=None,
                   repeat=1,
                   mouse_x_offset=0,
                   mouse_y_offset=0,
                   move_mouse=False
                   ):

        repeat_count = 0
        while repeat_count < repeat:
            repeat_count += 1
            for i, event in enumerate(macro_events):
                if self.stop_event.is_set():
                    break

                if event.event_type == EventType.KEY_DOWN:
                    self.keyboard_controller.press(event.event_value)
                    if key_press_release_interval:
                        time.sleep(key_press_release_interval / 1000)
                elif event.event_type == EventType.KEY_UP:
                    self.keyboard_controller.release(event.event_value)
                    if key_release_press_delay and i < len(macro_events) - 1 and macro_events[i + 1].event_type != EventType.DELAY:
                        time.sleep(key_release_press_delay / 1000)
                elif event.event_type == EventType.CLICK_DOWN:
                    button, x, y = event.event_value
                    if move_mouse:
                        self.mouse_controller.position = (x + mouse_x_offset, y + mouse_y_offset)
                    self.mouse_controller.press(button)
                    if click_press_release_interval:
                        time.sleep(click_press_release_interval / 1000)
                elif event.event_type == EventType.CLICK_UP:
                    button, x, y = event.event_value
                    if move_mouse:
                        self.mouse_controller.position = (x + mouse_x_offset, y + mouse_y_offset)
                    self.mouse_controller.release(button)
                    if click_press_release_interval:
                        time.sleep(click_press_release_interval / 1000)
                elif event.event_type == EventType.DELAY:
                    if not any([key_press_release_interval, click_press_release_interval, key_release_press_delay]):
                        time.sleep(event.event_value / 1000)  # Convert milliseconds to seconds
                    elif i > 0 and macro_events[i - 1].event_type in {EventType.KEY_UP, EventType.CLICK_UP}:
                        continue

        self.stop_event.set()  # Stop playback after all repetitions

    def stop_playback(self):
        self.stop_event.set()

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
    manager.play_macro(manager.macro_events, key_press_release_interval=100, click_press_release_interval=50, key_release_press_delay=50, repeat=3, mouse_x_offset=10, mouse_y_offset=10, move_mouse=True)  # Repeat the macro 3 times, with mouse movement and offsets
