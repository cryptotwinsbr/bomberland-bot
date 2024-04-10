import time
from random import *
import pyautogui

def date_formatted(format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format, time.localtime())

def replace(string, strReplace):
    if strReplace and string.endswith(strReplace):
        return string[: -len(strReplace)]
    return string

def randomness_number(n, randomn_factor_size=None):
    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)

    return int(randomized_n)

def randomize(loc: float, width: float, safe_factor=0):
    if safe_factor > 0.5:
        raise ValueError("safe_factor must be between 0 and 0.5")
    safe_dist = width * safe_factor
    min_value = loc + safe_dist
    max_value = loc + width - safe_dist    
    return uniform(min_value, max_value)

def randomize_int(loc: float, width: float, safe_factor=0):
    return round(randomize(loc, width, safe_factor))

def refresh_page(delay:int = 5):  
    shortcut_config = 1
    if shortcut_config == 1:
        pyautogui.hotkey('ctrl', 'f5')
    else:
        with pyautogui.hold('ctrl'):
            with pyautogui.hold('shift'):
                pyautogui.press('r')
    
def do_with_timeout(function, args = [], kwargs = {}, time_beteween: float = 0.5, timeout: float = 20):
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            return None        
        result = function(*args, **kwargs)
        if result is not None:
            return result        
        time.sleep(time_beteween)

def now():
    return time.time()