import os
import inspect
import urllib.request
from urllib.error import URLError, HTTPError

class Version:
    VERSION_FILE="version.txt"
    file_version=0
    github_version=0

    @classmethod
    def check_version(cls):
        if not cls.file_version:
            cls.get_from_file()
        cls.get_from_github()

        return cls.file_version == cls.github_version

    @classmethod
    def get_from_github(cls):
        ver_url = f'https://raw.githubusercontent.com/jay7one/PyMouseMacros/main/{cls.VERSION_FILE}'

        try:
            with urllib.request.urlopen(ver_url) as response:
                version_str = response.read().decode('utf-8').strip()
                cls.github_version = float(version_str)
                return
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except URLError as url_err:
            print(f"URL error occurred: {url_err}")
        except ValueError as val_err:
            print(f"Value error occurred: {val_err}")

        print("Version set to 0")
        cls.github_version = 0


    @classmethod
    def get_from_file(cls)->float:
        script_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        ver_file = os.path.join(os.path.dirname(os.path.dirname(script_path)),cls.VERSION_FILE)

        with open(ver_file, encoding='utf-8') as vfile:
            cls.file_version = float(vfile.readline().rstrip())
        return cls.file_version

if __name__ == '__main__':
    print(f"Ver from file : {Version.get_from_file()}")
    print(f"Ver in gh: {Version.get_from_github()}")
    print(f"{Version.check_version()=}")
