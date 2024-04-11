import sys
from enum import Enum

class PlatformEnum(Enum):
    LINUX = 1
    WINDOWS = 2

class Platform:
    def get_platform(self):
        is_linux = sys.platform == "linux" or sys.platform == "linux2"
        if is_linux:
            return PlatformEnum.LINUX
        else:
            return PlatformEnum.WINDOWS
