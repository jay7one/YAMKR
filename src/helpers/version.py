import os
import inspect
from urllib.request import urlopen
from requests.exceptions import RequestException

class Version:
    VERSION_FILE="version.txt"

    def __init__(self, userSettings):
        self.version = "1.1.11"
        self.new_version = ""
        if userSettings["Others"]["Check_update"]:
            self.update = self.checkVersion()
        else:
            self.update = "Check update disabled"

    @classmethod
    def from_github(cls):
        ver_url = f'https://raw.githubusercontent.com/jay7one/PyMouseMacros/main/{cls.VERSION_FILE}'

        print(f"Ver url :{ver_url}")
        try:
            data = urlopen(ver_url)
            print(f"{data=}")
            return float(data)

        except RequestException:
            return 0

    @classmethod
    def from_file(cls):
        script_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        ver_file = os.path.join(os.path.dirname(os.path.dirname(script_path)),cls.VERSION_FILE)

        with open(ver_file, encoding='utf-8') as vfile:
            version = float(vfile.readline().rstrip())

        return version

if __name__ == '__main__':
    print(f"Ver from file : {Version.from_file()}")
    print(f"Ver in gh: {Version.from_github()}")
