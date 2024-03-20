import os
import subprocess
from abc import ABC

class FileExplorer(ABC):    # pylint: disable=too-few-public-methods
    @staticmethod
    def open( path, filename=None):
        if not os.path.exists(path) :
            raise FileNotFoundError(f"The path '{path}' does not exist.")

        if filename:
            file_path = os.path.join(path, filename)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file '{filename}' does not exist in the given path.")
            file_path=str.replace(file_path,'/','\\')
            subprocess.Popen(["explorer", "/select,", file_path])
        else:
            path=str.replace(path,'/','\\')
            subprocess.Popen(["explorer", path])

# Example usage:
if __name__ == "__main__":
    FileExplorer.open("C:/Users/xxx/AppData/Local/PyMouseMacro/macros")
