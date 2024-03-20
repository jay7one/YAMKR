from sys import platform
import os
import shutil
from json import dumps, load
from abc import ABC, abstractmethod
from helpers.metaclasses import SingletonABCMeta

class Settings(ABC, metaclass=SingletonABCMeta):
    """Class to interact with user_settings.json"""
    def __init__(self, setting_type, check_new=False, initial_values=None, app_name = 'YAMKR'):

        self.setting_type = setting_type
        self.check_new = check_new
        self.dir_path = None        # Set below

        if platform == "win32":
            self.dir_path = os.path.join(os.getenv("LOCALAPPDATA"), app_name)
        elif "linux" in platform.lower():
            self.dir_path = os.path.join(os.path.expanduser("~"), ".config", app_name)
        elif "darwin" in platform.lower():
            self.dir_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", app_name)

        self.file_path = os.path.join(self.dir_path, f"{self.setting_type}.json")

        if not os.path.isdir(self.dir_path) or not os.path.isfile(self.file_path):
            if not initial_values:
                initial_values = self.initial_settings()
            self.init_settings(initial_values)

        if check_new:
            self.check_new_options()

    @abstractmethod
    def initial_settings(self):
        #print("Initial settings base")
        return {}

    def init_settings(self, default_values):
        """
        Init the settings in Appdata file in windows or user directory
        in Linux and mac_os if it doesn't exist.
        """
        if not os.path.isdir(self.dir_path):
            os.mkdir(self.dir_path)

        settings_json = dumps(default_values, indent=4)

        with open(self.file_path, "w", encoding='utf-8') as setting_file:
            setting_file.write(settings_json)

    def get_config(self):
        """Get settings of users"""
        with open(self.file_path, "r", encoding='utf-8') as setting_file:
            setting_file_json = load(setting_file)
        return setting_file_json

    def save_dict(self, updated_dict):
        self.save_settings(dumps(updated_dict, indent=4))

    def save_settings(self, updated_values):
        with open(self.file_path, "w", encoding='utf-8') as setting_file:
            setting_file.write(updated_values)

    def get_path(self):
        return self.file_path

    def get_setting(self,category, option_path=None):
        settings = self.get_config()

        if not category in settings:
            return None

        option_value = settings[category]
        if option_path :
            for option in option_path:
                option_value = option_value[option]

        return option_value

    def change_settings(self, category, option=None, option2=None, new_value=None):
        """Change settings of user"""
        settings = self.get_config()

        #print(f"Settings: {settings}")

        if not category in settings:
            settings[category] = ""
        if new_value is None:
            if option is None:
                settings[category] = not settings[category]
            elif option2 is not None:
                settings[category][option][option2] = not settings[category][option][option2]
            else:
                settings[category][option] = not settings[category][option]

        elif option is not None and new_value is not None:
            if option2 is not None:
                settings[category][option][option2] = new_value
            else:
                settings[category][option] = new_value
        self.save_settings(dumps(settings, indent=4))

    def check_new_options(self):
        user_settings = self.get_config()
        if "Others" not in user_settings:
            user_settings["Others"] = {"Check_update": True}
            self.save_settings(dumps(user_settings, indent=4))
        if "Fixed_timestamp" not in user_settings["Others"]:
            user_settings["Others"]["Fixed_timestamp"] = 0
            self.save_settings(dumps(user_settings, indent=4))
        if "Delay" not in user_settings["Playback"]["Repeat"]:
            user_settings["Playback"]["Repeat"]["Delay"] = 0
            self.save_settings(dumps(user_settings, indent=4))

    def reset_settings(self, initial_values=None):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        if not initial_values:
            initial_values = self.initial_settings()
        self.init_settings(initial_values)


    def uninstall_settings(self):
        try:
            if os.path.exists(self.dir_path):
                shutil.rmtree(self.dir_path)
        except Exception as e:      # pylint: disable=broad-exception-caught
            print(f"Error occurred while removing directory '{self.dir_path}': {e}")
