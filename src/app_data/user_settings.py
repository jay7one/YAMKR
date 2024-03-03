from app_data.settings import Settings

class UserSettings(Settings):

    def __init__(self, initial_values=None):
        super().__init__("UserSettings", True, initial_values)

    def initial_settings(self):
        return  {
            "Playback": {
                "Speed": 1,
                "Repeat": {
                    "Times": 1,
                    "For": 0,
                    "Interval": 0,
                    "Delay": 0
                }
            },

            "Recordings": {
                "Mouse_Move": True,
                "Mouse_Click": True,
                "Keyboard": True,
            },

            "Hotkeys": {
                "Record_Start": [],
                "Record_Stop": [],
                "Playback_Start": [],
                "Playback_Stop": [
                    "Key.f3"
                ],
            },

            "Minimization": {
                "When_Playing": False,
                "When_Recording": False,
            },

            "Run_On_StartUp": False,

            "After_Playback": {
                "Mode": "Idle"
                # Quit, Lock Computer, Lof off computer, Turn off computer, Restart Computer, Standby, Hibernate
            },

            "Others": {
                "Check_update": True,
                "Fixed_timestamp": 0
            }
        }

if __name__ == "__main__":
    UserSettings().uninstall_settings()
