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

    def __str__(self):
        return f'{str(self.event_type)}:{self.event_value}'

    def data(self):
        if self.event_type in [EventType.KEY_UP, EventType.KEY_DOWN, EventType.DELAY]:
            return str(self.event_type) , self.event_value

        if self.event_type in [EventType.CLICK_UP, EventType.CLICK_DOWN]:
            return str(self.event_type), *self.event_value

    def mouse_event_data(self):
        if str(self.event_type)[0].upper() != "C":
            raise ValueError("Event Type is not a click up or down")

        parts = self.event_value
        btn = parts[0].strip()  # Extracting direction part
        x = int(parts[1])  # Converting x-coordinate to integer
        y = int(parts[2])  # Converting y-coordinate to integer
        return btn,x,y

    def abv(self):
        # print(f"abv :{(self.event_type,self.event_value)=}")
        if self.event_type == EventType.DELAY:
            return f"D:{self.event_value}"
        if self.event_type == EventType.KEY_UP:
            return f"KU:{self.event_value}"
        if self.event_type == EventType.KEY_DOWN:
            return f"KD:{self.event_value}"

        button, x, y = self.mouse_event_data()
        button = button[0].upper()

        mouse_code = "U" if self.event_type == EventType.CLICK_UP else "D"
        return f"M{mouse_code}{button}:{x,y}"

if __name__ == '__main__':
    me = MacroEvent(EventType.KEY_DOWN, "a")
    print(f"me str = {str(me)}")
    print(f"data={me.data()}")
    print(f"abv={me.abv()}")

    me = MacroEvent(EventType.CLICK_DOWN, ("left",10,20))
    print(f"me str = {str(me)}")
    print(f"data={me.data()}")
    print(f"abv={me.abv()}")

    me = MacroEvent(EventType.DELAY, 100)
    print(f"me str = {str(me)}")
    print(f"data={me.data()}")
    print(f"abv={me.abv()}")
