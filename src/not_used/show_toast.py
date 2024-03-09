from sys import platform
import subprocess
from app_data.resources import Resources

def show_notification_minim():
    if platform == "win32":
        from win10toast import ToastNotifier    # pylint: disable=import-outside-toplevel

        toast = ToastNotifier()
        try:
            toast.show_toast(
                title="PyMouseMacro minimized",
                msg="PyMouseMacro has been minimized",
                duration=3,
                icon_path=Resources.get_asset("logo.ico")
            )
        except:     # pylint: disable=bare-except
            pass

    elif "linux" in platform.lower():
        subprocess.call("""notify-send -u normal "PyMouseMacro" "PyMouseMacro has been minimized" """, shell=False)
    elif "darwin" in platform.lower():
        subprocess.call("""display notification "PyMouseMacro has been minimized" with title "PyMouseMacro""", shell=False)
