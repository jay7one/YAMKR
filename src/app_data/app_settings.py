from app_data.settings import Settings

class AppSettings(Settings):

    def __init__(self, initial_values=None):
        super().__init__("AppSettings", False, initial_values)

    def initial_settings(self):
        return  {
        }

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
