from enum import Enum

class EventType(Enum):
    KEY_UP = "key_up"
    KEY_DOWN = "key_down"
    CLICK_UP = "click_up"
    CLICK_DOWN = "click_down"
    DELAY = "delay"

    def __str__(self):
        return self.value

class MacroEvent:
    def __init__(self, event_type, event_value):
        if not isinstance(event_type, EventType):
            raise ValueError(f"Invalid event type: {event_type, event_value}")

        self.event_type = event_type
        self.event_value = event_value

    def to_dict(self):
        return {
            "event_type": str(self.event_type),
            "event_value": self.event_value
        }