import time
import threading

from pynput.keyboard import Controller as KeyboardController, Listener as KeyboardListener, Key
from pynput.mouse import Controller as MouseController
from macros.macro_event import MacroEvent, EventType
from macros.macro_event_recorder import MacroEventRecorder
from macros.macro_data import MacroData
from helpers.pynput_map import PynputMap

class MacroEventManager(MacroEventRecorder):
    def __init__(self):
        super().__init__()
        self.keyboard_controller = KeyboardController()
        self.mouse_controller = MouseController()
        self.playback_kb_listener = None
        self.stop_playback_event = threading.Event()

    def sleep_if(self, sleep_on, sleep_ms):
        if sleep_on: time.sleep(sleep_ms/1000)

    def play_macro(self, macro_events:list[MacroEvent], macro:MacroData):
        repeat_count = 0
        print("Starting playback")
        while repeat_count < macro.global_repeat:
            repeat_count += 1
            if self.stop_playback_event.is_set():
                break
            last_event = None

            for i,event in enumerate(macro_events):

                #print(f"{i=},{event.event_type=},{event.event_value}")
                if self.stop_playback_event.is_set():
                    break

                if event.event_type == EventType.KEY_DOWN:
                    self.keyboard_controller.press(PynputMap.map_key(event.event_value))
                    self.sleep_if(macro.global_keypress_interval_on,macro.global_keypress_interval)
                    last_event = event
                    continue

                if event.event_type == EventType.KEY_UP:
                    self.keyboard_controller.release(PynputMap.map_key(event.event_value))
                    self.sleep_if(macro.global_release_interval_on,macro.global_release_interval)
                    last_event = event
                    continue

                if event.event_type == EventType.CLICK_DOWN:
                    button, x, y = event.mouse_event_data()
                    self.mouse_controller.position = (x + macro.global_mouse_offset_x, y + macro.global_mouse_offset_y)
                    self.mouse_controller.press(PynputMap.map_btn(button))
                    self.sleep_if(macro.global_mousepress_interval_on,macro.global_mousepress_interval)
                    last_event = event
                    continue

                if event.event_type == EventType.CLICK_UP:
                    button, x, y = event.mouse_event_data()
                    self.mouse_controller.position = (x + macro.global_mouse_offset_x, y + macro.global_mouse_offset_y)
                    self.mouse_controller.release(PynputMap.map_btn(button))
                    self.sleep_if(macro.global_release_interval_on,macro.global_release_interval)
                    last_event = event
                    continue

                if event.event_type == EventType.DELAY:

                    if macro.global_mouse_movement:
                        next_event = macro_events[i + 1]
                        if ( next_event.event_type in [EventType.CLICK_UP,EventType.CLICK_DOWN] and
                             last_event.event_type in [EventType.CLICK_UP,EventType.CLICK_DOWN] ):
                            self.move_mouse_slowly(last_event, next_event, event.event_value)
                            continue

                    if  (
                            ( last_event.event_type == EventType.CLICK_DOWN and macro.global_mousepress_interval_on ) or
                            ( last_event.event_type == EventType.CLICK_UP   and macro.global_release_interval_on ) or
                            ( last_event.event_type == EventType.KEY_DOWN   and macro.global_keypress_interval_on ) or
                            ( last_event.event_type == EventType.KEY_UP     and macro.global_release_interval_on )
                        ):
                        continue

                    time.sleep(event.event_value / 1000)  # Convert milliseconds to seconds


        self.stop_playback_event.set()  # Stop playback after all repetitions

    def distance(self,x1, y1, x2, y2):
        return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

    def move_mouse_slowly(self, last_evt:MacroEvent, next_evt:MacroEvent, duration_ms):

        #print(f"Play slowly:{last_evt.mouse_event_data()}, { next_evt.mouse_event_data()}, {duration_ms=}")
        btn1, start_x, start_y = last_evt.mouse_event_data()
        btn2, target_x, target_y = next_evt.mouse_event_data()

        if btn1 != btn2:
            # Not supported having both left and right clicks
            return False

        # Calculate the distance between start and target positions
        distance_x = target_x - start_x
        distance_y = target_y - start_y
        total_distance = ((distance_x)**2 + (distance_y)**2) ** 0.5

        # If the total distance is less than or equal to 3 pixels, wait for the duration and return
        if total_distance <= 3:
            time.sleep(duration_ms / 1000)  # Convert duration to seconds
            self.mouse_controller.position = (target_x, target_y)
            return

        # Calculate the time interval between each step
        interval = duration_ms / (total_distance / 3)

        # Perform the smooth movement
        start_time = time.time()
        while time.time() - start_time < duration_ms / 1000:
            progress = (time.time() - start_time) / (duration_ms / 1000)
            new_x = start_x + distance_x * progress
            new_y = start_y + distance_y * progress
            self.mouse_controller.position = (new_x, new_y)
            time.sleep(interval / 1000)

        return True

    def stop_playback(self):
        self.stop_playback_event.set()

    def start_playback_listening(self):
        self.playback_kb_listener = KeyboardListener(on_press=self.on_playback_key_press)
        self.playback_kb_listener.start()

    def on_playback_key_press(self, key):
        if key == Key.ctrl_l and not self.stop_playback_event.is_set():
            self.stop_playback()

# Example usage:
if __name__ == "__main__":
    import helpers.screen_setup # pylint: disable=unused-import

    # Create an instance of MacroEventManager
    manager = MacroEventManager()

    print("Start recording")
    # Stop recording when Ctrl + End is pressed
    evts=manager.record_macro((0,0))
    print("Stopped recording, sleep 2 secs then playback")

    time.sleep(2)

    #manager.print_events(evts)
    manager.print_events(manager.macro_events)
    # Start recording
    manager.start_playback_listening()

    macro_data = MacroData(
        name = "MacroTestPlayback",
        hotkey = "",
        global_keypress_interval = 20,
        global_mousepress_interval = 20,
        global_keypress_interval_on = False,
        global_mousepress_interval_on = False,
        global_mouse_offset_x = 0,
        global_mouse_offset_y = 0,
        global_mouse_movement = True,

        global_release_interval = 500,
        global_release_interval_on = False,
        global_repeat = 1
    )

    # Playback recorded macro
    manager.play_macro( manager.macro_events, macro_data)  # Repeat the macro 3 times, with mouse movement and offsets
