import tkinter as tk
from macros.macro_event import MacroEvent, EventType

class EventWidget(tk.Label):
    ICON_SIZE = 32

    ICONS1 = {
        EventType.KEY_UP: ("⌨️", "\u2191"),  # Keyboard and up arrow
        EventType.KEY_DOWN: ("⌨️", "⬇️"),  # Keyboard and down arrow
        EventType.CLICK_UP: ("🖱️", "⬆️"),  # Mouse and up arrow
        EventType.CLICK_DOWN: ("🖱️", "⬇️"),  # Mouse and down arrow
        EventType.DELAY: ("\u23F1", "")  # Stopwatch
    }

    kb_icon = "\U0001F5A9"
    ICONS = {
        EventType.KEY_UP: ("", "\u2191"),  # Keyboard and up arrow
        EventType.KEY_DOWN: ("", "\u2193"),  # Keyboard and down arrow
        EventType.CLICK_UP: ("\U0001F5B1", "\u2191"),  # Mouse and up arrow
        EventType.CLICK_DOWN: ("\U0001F5B1", "\u2193"),  # Mouse and down arrow
        EventType.DELAY: ("\u23F1", "")  # Stopwatch
    }

    def __init__(self, parent, event, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, )
        self.event = event
        self.draw()

    def draw(self):
        if self.event.event_type in self.ICONS:
            icon1, icon2 = self.ICONS[self.event.event_type]
            text = f"{icon1}{icon2}"
            if self.event.event_value:
                text += f": {self.event.event_value}"
            if icon2 == "":
                text += "ms"
            text = text.ljust(12)
            #print(f"Debug:{text=}")
            self.config(text=text,anchor=tk.W, relief='raised')

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()

    test_events = [
        MacroEvent(EventType.KEY_DOWN, "a"),
        MacroEvent(EventType.KEY_UP, "a"),
        MacroEvent(EventType.DELAY, 1000),
        MacroEvent(EventType.CLICK_DOWN, ("left",100, 200)),
        MacroEvent(EventType.CLICK_UP, ("left",100, 200))
    ]

    for e in test_events:
        widget = EventWidget(root, e)
        widget.pack(anchor=tk.W, padx=5, pady=5)

    root.mainloop()
