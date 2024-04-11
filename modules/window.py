import subprocess
from modules.platform import Platform, PlatformEnum

def get_windows(type):
    return (
        _get_linux_windows(type)
        if Platform().get_platform() == PlatformEnum.LINUX
        else _get_windows(type)
    )

def _get_linux_windows(type):
    if type == 'BOMB':
        stdout = (
            subprocess.Popen(
                "xdotool search --name Bomber Land", shell=True, stdout=subprocess.PIPE
            )
            .communicate()[0]
            .decode("utf-8")
            .strip()
        )
    windows = stdout.split("\n")
    return [LinuxWindow(w) for w in windows]

def _get_windows(type):
    import pygetwindow
    if type == 'BOMB':
        return [DefaultWindow(w) for w in pygetwindow.getWindowsWithTitle("Bomber Land")]

class LinuxWindow:
    def __init__(self, window_id) -> None:
        self.window = window_id
    def activate(self):        
        subprocess.Popen(f"xdotool windowactivate {self.window}", shell=True)

class DefaultWindow:
    def __init__(self, window) -> None:
        self.window = window
    def activate(self):
        self.window.activate()
