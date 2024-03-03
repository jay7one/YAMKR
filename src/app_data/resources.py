import sys
from os import path

class Resources:

    @classmethod
    def resource_path(cls,relative_path):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = getattr(sys,'_MEIPASS')
        else:
            base_path = path.abspath(".")

        return path.join(base_path, relative_path)

    @classmethod
    def get_asset(cls,asset_name):
        return cls.resource_path(path.join("assets", asset_name))

if __name__ == "__main__":
    print( f"{Resources.resource_path('test1')}")
