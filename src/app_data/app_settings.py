from app_data.settings import Settings

class AppSettings(Settings):
    MIN_ON_PLAY="play"
    MIN_ON_RECPORD="record"
    def __init__(self, initial_values=None):
        super().__init__("AppSettings", False, initial_values)

    def initial_settings(self):
        return  {

            "main_screen": {
                "geo": "+100+100" ,
                "When_Recording": False,
            },

            "Minimization": {
                self.MIN_ON_PLAY: False,
                self.MIN_ON_RECPORD: False,
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

    def set_min_on(self, min_setting, min_on):
        settings = self.get_config()
        settings["Minimization"][min_setting] = min_on
        self.save_dict(settings)

    def get_min_on(self, min_setting):
        is_on = self.get_config()["Minimization"][min_setting]
        #print(f"Debug is ok {min_setting=} : {is_on=}")
        return is_on

    def set_min_on_record(self,min_on): self.set_min_on(self.MIN_ON_RECPORD, min_on)
    def set_min_on_play(self,min_on):   self.set_min_on(self.MIN_ON_PLAY, min_on)

    def get_min_on_record(self): return self.get_min_on(self.MIN_ON_RECPORD)
    def get_min_on_play(self):   return self.get_min_on(self.MIN_ON_PLAY)

    def get_main_geo(self):
        settings = self.get_config()
        #print(f"Debug {settings}")
        return settings["main_screen"]["geo"]

    def set_main_geo(self, geo):
        settings = self.get_config()
        settings["main_screen"]["geo"] = geo
        self.save_dict(settings)

if __name__ == "__main__":

    AppSettings(initial_values=
        {
            "Testing1": "Level1",
            "Testing2": {'Level1': "Level1Value"},
            "Testing3": {'Level1': { 'Level2': 'Level2Value', 'Level2K2': 'L2K2Val'}}
        }
    )

    print(f"Testing 1: {AppSettings().get_setting('Testing1')}")
    print(f"Testing 2: {AppSettings().get_setting('Testing2', ['Level1'])}")
    print(f"Testing 3: {AppSettings().get_setting('Testing3', ['Level1', 'Level2'])}")
    print(f"Testing 3K2: {AppSettings().get_setting('Testing3', ['Level1', 'Level2K2'])}")


    AppSettings().uninstall_settings()
